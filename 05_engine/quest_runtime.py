# 05_engine/quest_runtime.py
from __future__ import annotations
from location_runtime import check_location_gate

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Errors
# -----------------------------
class QuestRuntimeError(Exception):
    pass


# -----------------------------
# Active Quest State (save-able)
# -----------------------------
@dataclass
class ActiveQuest:
    quest_id: str
    accepted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")
    # progress is intentionally generic to avoid coupling to schema
    progress: Dict[str, Any] = field(default_factory=dict)
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "quest_id": self.quest_id,
            "accepted_at": self.accepted_at,
            "progress": self.progress,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ActiveQuest":
        return ActiveQuest(
            quest_id=str(d.get("quest_id", "")),
            accepted_at=str(d.get("accepted_at", "")) or datetime.utcnow().isoformat(timespec="seconds") + "Z",
            progress=dict(d.get("progress", {}) or {}),
            completed_at=d.get("completed_at"),
        )


# -----------------------------
# Runtime
# -----------------------------
class QuestRuntime:
    """
    MVL Quest Runtime:
    - Index quests loaded from content_loader (raw dicts)
    - accept quest -> create ActiveQuest state
    - report events -> update progress (generic)
    - check_complete -> evaluate complete_condition (Condition schema) if present
    """

    def __init__(self, quests: List[Dict[str, Any]]) -> None:
        self._quests = quests
        self._by_id: Dict[str, Dict[str, Any]] = {}

        for q in quests:
            qid = self._get_quest_id(q)
            if qid:
                # first one wins (MVL); later we can enforce uniqueness
                self._by_id.setdefault(qid, q)

    # ---------
    # Core ops
    # ---------
    def list_quest_ids(self) -> List[str]:
        return sorted(self._by_id.keys())

    def get_quest(self, quest_id: str) -> Dict[str, Any]:
        if quest_id not in self._by_id:
            raise QuestRuntimeError(f"Quest not found: {quest_id}")
        return self._by_id[quest_id]

    def accept(self, quest_id: str) -> ActiveQuest:
        _ = self.get_quest(quest_id)  # validate exists
        # initialize progress buckets used by common objective types
        st = ActiveQuest(quest_id=quest_id)
        st.progress.setdefault("items", {})     # item_id -> count
        st.progress.setdefault("kills", {})     # monster_id -> count
        st.progress.setdefault("flags", {})     # key -> value
        st.progress.setdefault("vars", {})      # key -> number/string
        return st

    def mark_completed(self, st: ActiveQuest) -> None:
        if st.completed_at is None:
            st.completed_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    # ---------
    # Event reporting (for progress)
    # ---------
    def report_item_gained(self, st: ActiveQuest, item_id: str, count: int = 1) -> None:
        items = st.progress.setdefault("items", {})
        items[item_id] = int(items.get(item_id, 0)) + int(count)

    def report_monster_killed(self, st: ActiveQuest, monster_id: str, count: int = 1) -> None:
        kills = st.progress.setdefault("kills", {})
        kills[monster_id] = int(kills.get(monster_id, 0)) + int(count)

    def report_flag_set(self, st: ActiveQuest, key: str, value: Any = True) -> None:
        flags = st.progress.setdefault("flags", {})
        flags[key] = value

    def report_var_set(self, st: ActiveQuest, key: str, value: Any) -> None:
        vars_ = st.progress.setdefault("vars", {})
        vars_[key] = value

    # ---------
    # Completion check
    # ---------
    def check_complete(
        self,
        st: ActiveQuest,
        game_state: Optional[Dict[str, Any]] = None,
        runtime_context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, List[str]]:
        """
        Returns: (is_complete, reasons)
        - Prefer Condition schema (complete_condition) if present.
        - Otherwise, fall back to legacy objectives evaluation (tolerant).
        """
        quest = self.get_quest(st.quest_id)

        # Condition-first (Engine Phase B)
        cond = None
        if isinstance(quest.get("complete_condition"), dict):
            cond = quest.get("complete_condition")
        elif isinstance(quest.get("completion"), dict) and isinstance(quest["completion"].get("complete_condition"), dict):
            cond = quest["completion"]["complete_condition"]

        if isinstance(cond, dict):
            gs = game_state or {}
            ok, reason = self._eval_condition(cond, gs)
            if not ok:
                return False, [reason or "condition not met"]

            gate_ok, gate_reason = check_location_gate(st.quest_id, runtime_context or {})
            if not gate_ok:
                return False, [gate_reason or "location gate failed"]

            return True, []

        # Legacy objectives fallback
        objectives = None
        if isinstance(quest.get("objectives"), list):
            objectives = quest.get("objectives")
        elif isinstance(quest.get("requirements"), list):
            objectives = quest.get("requirements")
        elif isinstance(quest.get("completion"), dict) and isinstance(quest["completion"].get("objectives"), list):
            objectives = quest["completion"]["objectives"]

        if not objectives:
            gate_ok, gate_reason = check_location_gate(st.quest_id, runtime_context or {})
            if not gate_ok:
                return False, [gate_reason or "location gate failed"]
            return True, []

        reasons: List[str] = []
        all_ok = True

        for idx, obj in enumerate(objectives):
            ok, reason = self._eval_objective(obj, st)
            if not ok:
                all_ok = False
                reasons.append(f"objective[{idx}]: {reason}")

        if not all_ok:
            return False, reasons

        gate_ok, gate_reason = check_location_gate(st.quest_id, runtime_context or {})
        if not gate_ok:
            return False, [gate_reason or "location gate failed"]

        return True, []

    # ---------
    # Accept-condition check (NEW)
    # ---------
    def check_acceptable(self, quest_id: str, game_state: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Evaluate quest.accept_condition if exists.
        If missing -> acceptable.
        """
        quest = self.get_quest(quest_id)

        cond = None
        if isinstance(quest.get("accept_condition"), dict):
            cond = quest.get("accept_condition")
        elif isinstance(quest.get("acceptance"), dict) and isinstance(quest["acceptance"].get("accept_condition"), dict):
            cond = quest["acceptance"]["accept_condition"]

        if not isinstance(cond, dict):
            return True, ""

        gs = game_state or {}
        ok, reason = self._eval_condition(cond, gs)
        if ok:
            return True, ""
        return False, reason or "accept_condition not met"

    # -----------------------------
    # Condition evaluation (recursive)
    # -----------------------------
    def _eval_condition(self, node: Any, game_state: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(node, dict):
            return False, "condition is not an object/dict"

        typ = node.get("type")
        if not isinstance(typ, str) or not typ.strip():
            return False, "missing condition.type"
        t = typ.strip().lower()

        params = node.get("params")
        if params is None:
            params = {}
        if not isinstance(params, dict):
            return False, "condition.params is not an object/dict"

        # Composite nodes
        if t in ("and", "or"):
            conds = params.get("conditions")
            if not isinstance(conds, list):
                return False, f"{t} condition missing params.conditions (list)"

            if t == "and":
                for i, c in enumerate(conds):
                    ok, reason = self._eval_condition(c, game_state)
                    if not ok:
                        return False, f"and.conditions[{i}] failed: {reason}"
                return True, ""

            last_reason = ""
            for i, c in enumerate(conds):
                ok, reason = self._eval_condition(c, game_state)
                if ok:
                    return True, ""
                last_reason = f"or.conditions[{i}] failed: {reason}"
            return False, last_reason or "or: no condition matched"

        if t == "not":
            inner = params.get("condition")
            ok, _ = self._eval_condition(inner, game_state)
            if ok:
                return False, "not: inner condition was true"
            return True, ""

        # Leaf: flag.is_true / flag.is_false (NEW)
        if t in ("flag.is_true", "flag.is_false"):
            key = params.get("key") or params.get("flag_key")
            if not isinstance(key, str) or not key.strip():
                return False, f"{t} missing params.key"

            got = self._gs_get(game_state, "flags", key, False)

            # Normalize truthiness: treat True / "true" / 1 as true
            is_true = False
            if isinstance(got, bool):
                is_true = got
            elif isinstance(got, (int, float)):
                is_true = (got != 0)
            elif isinstance(got, str):
                is_true = got.strip().lower() in ("true", "1", "yes", "y", "on")

            if t == "flag.is_true":
                if is_true:
                    return True, ""
                return False, f"flag '{key}' must be true"
            else:
                # is_false: treat missing as false (default=False above)
                if not is_true:
                    return True, ""
                return False, f"flag '{key}' must be false"

        # Leaf: flag.int_compare
        if t == "flag.int_compare":
            flag_key = params.get("flag_key") or params.get("key")
            op = params.get("op")
            want = params.get("value")

            if not isinstance(flag_key, str) or not flag_key.strip():
                return False, "flag.int_compare missing params.key/flag_key"
            if not isinstance(op, str) or not op.strip():
                return False, "flag.int_compare missing params.op"
            try:
                want_n = int(want)
            except Exception:
                return False, "flag.int_compare params.value is not int"

            got_raw = self._gs_get(game_state, "flags", flag_key, 0)
            try:
                got_n = int(got_raw)
            except Exception:
                return False, f"flag '{flag_key}' is not int (got {got_raw!r})"

            op_norm = op.strip().lower()
            ok = self._compare_int(got_n, op_norm, want_n)
            if ok:
                return True, ""
            return False, f"flag '{flag_key}' must be {op_norm} {want_n}, got {got_n}"

        # Leaf: inventory.has
        if t == "inventory.has":
            item_id = params.get("item_id") or params.get("id")
            qty = params.get("qty", params.get("count", 1))
            if not isinstance(item_id, str) or not item_id.strip():
                return False, "inventory.has missing params.item_id"
            try:
                need_n = int(qty)
            except Exception:
                return False, "inventory.has params.qty is not int"

            have_raw = self._gs_get(game_state, "inventory", item_id, 0)
            try:
                have_n = int(have_raw)
            except Exception:
                have_n = 0

            if have_n >= need_n:
                return True, ""
            return False, f"need item '{item_id}' x{need_n}, have {have_n}"

        return False, f"unsupported condition.type: {t}"

    @staticmethod
    def _gs_get(game_state: Dict[str, Any], bucket: str, key: str, default: Any) -> Any:
        b = game_state.get(bucket)
        if isinstance(b, dict):
            return b.get(key, default)
        return default

    @staticmethod
    def _compare_int(left: int, op: str, right: int) -> bool:
        if op == "eq":
            return left == right
        if op == "gt":
            return left > right
        if op == "gte":
            return left >= right
        if op == "lt":
            return left < right
        if op == "lte":
            return left <= right
        # unknown op -> fail closed
        return False

    # -----------------------------
    # Internal helpers (legacy objectives)
    # -----------------------------
    def _get_quest_id(self, q: Dict[str, Any]) -> str:
        for key in ("id", "quest_id", "qid", "key"):
            v = q.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return ""

    def _eval_objective(self, obj: Any, st: ActiveQuest) -> Tuple[bool, str]:
        if not isinstance(obj, dict):
            return False, "objective is not an object/dict"

        # composite
        if isinstance(obj.get("all"), list) or isinstance(obj.get("and"), list):
            kids = obj.get("all") if isinstance(obj.get("all"), list) else obj.get("and")
            assert isinstance(kids, list)
            for kid in kids:
                ok, reason = self._eval_objective(kid, st)
                if not ok:
                    return False, f"composite failed: {reason}"
            return True, ""

        typ = obj.get("type")
        if not isinstance(typ, str) or not typ.strip():
            return False, "missing objective.type"

        typ = typ.strip().lower()

        if typ in ("collect_item", "collect", "item"):
            item_id = obj.get("item_id") or obj.get("id")
            need = obj.get("count", 1)
            if not isinstance(item_id, str) or not item_id.strip():
                return False, "collect_item missing item_id"
            try:
                need_n = int(need)
            except Exception:
                return False, "collect_item count is not an int"
            have = int(st.progress.get("items", {}).get(item_id, 0))
            if have >= need_n:
                return True, ""
            return False, f"need item '{item_id}' x{need_n}, have {have}"

        if typ in ("kill_monster", "kill", "monster"):
            monster_id = obj.get("monster_id") or obj.get("id")
            need = obj.get("count", 1)
            if not isinstance(monster_id, str) or not monster_id.strip():
                return False, "kill_monster missing monster_id"
            try:
                need_n = int(need)
            except Exception:
                return False, "kill_monster count is not an int"
            have = int(st.progress.get("kills", {}).get(monster_id, 0))
            if have >= need_n:
                return True, ""
            return False, f"need kill '{monster_id}' x{need_n}, have {have}"

        if typ in ("flag", "set_flag"):
            key = obj.get("key") or obj.get("flag")
            want = obj.get("value", True)
            if not isinstance(key, str) or not key.strip():
                return False, "flag missing key"
            got = st.progress.get("flags", {}).get(key, None)
            if got == want:
                return True, ""
            return False, f"flag '{key}' must be {want!r}, got {got!r}"

        if typ in ("var_gte", "gte", "min_var"):
            key = obj.get("key")
            want = obj.get("value")
            if not isinstance(key, str) or not key.strip():
                return False, "var_gte missing key"
            try:
                want_n = float(want)
            except Exception:
                return False, "var_gte value is not a number"
            got = st.progress.get("vars", {}).get(key, 0)
            try:
                got_n = float(got)
            except Exception:
                return False, f"var '{key}' is not numeric (got {got!r})"
            if got_n >= want_n:
                return True, ""
            return False, f"var '{key}' must be >= {want_n}, got {got_n}"

        return False, f"unsupported objective.type: {typ}"