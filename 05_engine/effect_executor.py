# 05_engine/effect_executor.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# -----------------------------
# Errors / logs
# -----------------------------
class EffectExecutorError(Exception):
    pass


@dataclass
class EffectLog:
    kind: str      # "applied" | "skipped" | "error"
    message: str
    effect: Optional[Dict[str, Any]] = None


# -----------------------------
# Executor
# -----------------------------
class EffectExecutor:
    """
    MVL Effect Executor:
    - Apply completion effects to a generic game_state dict.
    - Effects are dict objects, tolerant to different shapes.

    game_state MVL shape (all optional):
      {
        "inventory": { "item_id": count, . },
        "flags": { "key": value, . },
        "vars": { "key": number/str/bool, . },
      }
    """

    def __init__(self) -> None:
        pass

    # ---------
    # Public API
    # ---------
    def apply_quest_complete_effects(
        self,
        quest: Dict[str, Any],
        game_state: Dict[str, Any],
    ) -> List[EffectLog]:
        effects = self._extract_effects(quest)
        if not effects:
            return [EffectLog(kind="skipped", message="No effects found on quest")]

        logs: List[EffectLog] = []
        for ef in effects:
            if not isinstance(ef, dict):
                logs.append(EffectLog(kind="error", message="Effect is not an object/dict", effect=None))
                continue

            try:
                logs.extend(self._apply_one(ef, game_state))
            except Exception as e:
                logs.append(EffectLog(kind="error", message=f"Exception applying effect: {e}", effect=ef))

        return logs

    # ---------
    # Internals
    # ---------
    def _extract_effects(self, quest: Dict[str, Any]) -> List[Any]:
        """
        Tolerant extractor:
        Try common places in order, return a list if found.

        Supported containers:
          - quest["effects"]
          - quest["rewards"] (list) OR quest["rewards"]["effects"] (dict)
          - quest["on_complete"]["effects"]
          - quest["completion"]["effects"]
          - quest["completion"]["rewards"] (list) OR quest["completion"]["rewards"]["effects"] (dict)
        """
        candidates: List[Any] = []

        if isinstance(quest.get("effects"), list):
            candidates = quest["effects"]
        elif isinstance(quest.get("rewards"), dict) and isinstance(quest["rewards"].get("effects"), list):
            candidates = quest["rewards"]["effects"]
        elif isinstance(quest.get("rewards"), list):
            candidates = quest["rewards"]
        elif isinstance(quest.get("on_complete"), dict) and isinstance(quest["on_complete"].get("effects"), list):
            candidates = quest["on_complete"]["effects"]
        elif isinstance(quest.get("completion"), dict):
            comp = quest["completion"]
            if isinstance(comp.get("effects"), list):
                candidates = comp["effects"]
            elif isinstance(comp.get("rewards"), dict) and isinstance(comp["rewards"].get("effects"), list):
                candidates = comp["rewards"]["effects"]
            elif isinstance(comp.get("rewards"), list):
                candidates = comp["rewards"]

        return list(candidates) if candidates else []

    # -----------------------------
    # Small helpers (tolerant)
    # -----------------------------
    def _params(self, ef: Dict[str, Any]) -> Dict[str, Any]:
        return ef.get("params") if isinstance(ef.get("params"), dict) else {}

    def _ensure_bucket(self, game_state: Dict[str, Any], name: str) -> Dict[str, Any]:
        b = game_state.setdefault(name, {})
        if not isinstance(b, dict):
            game_state[name] = {}
            b = game_state[name]
        return b

    def _to_int(self, v: Any, default: int = 0) -> int:
        try:
            # allow "10", 10, 10.0, "10.0"
            if isinstance(v, bool):
                return int(v)
            if isinstance(v, (int,)):
                return int(v)
            if isinstance(v, float):
                return int(v)
            if isinstance(v, str):
                s = v.strip()
                if s == "":
                    return default
                # try int first, then float->int
                try:
                    return int(s)
                except Exception:
                    return int(float(s))
            return int(v)  # last resort
        except Exception:
            return default

    def _to_float(self, v: Any, default: float = 0.0) -> float:
        try:
            if isinstance(v, bool):
                return float(int(v))
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                s = v.strip()
                if s == "":
                    return default
                return float(s)
            return float(v)
        except Exception:
            return default

    def _keep_int_if_possible(self, x: float) -> Any:
        if abs(x - int(x)) < 1e-9:
            return int(x)
        return x

    # -----------------------------
    # Dispatcher
    # -----------------------------
    def _apply_one(self, ef: Dict[str, Any], game_state: Dict[str, Any]) -> List[EffectLog]:
        """
        Supported MVL effect types (tolerant):

        Existing Phase B:
        - give_item (aliases: grant_item/add_item/item)
        - set_flag / flag.set (aliases: flag)
        - set_var (aliases: var/set)
        - add_var (aliases: inc_var/add/inc)
        - gold.add (MVP) -> vars["gold"] += amount

        Phase C expansion (Engine-only):
        - inventory.add
        - inventory.remove
        - flag.int_add
        - var.add
        """
        logs: List[EffectLog] = []

        typ = ef.get("type")
        if not isinstance(typ, str) or not typ.strip():
            return [EffectLog(kind="error", message="Missing effect.type", effect=ef)]

        t = typ.strip().lower()
        params = self._params(ef)

        # -----------------------------
        # Phase C: inventory.add / inventory.remove
        # -----------------------------
        if t in ("inventory.add", "inv.add"):
            item_id = (
                ef.get("item_id")
                or ef.get("id")
                or params.get("item_id")
                or params.get("id")
                or params.get("item")
            )
            # tolerate count/qty/amount/delta/value
            raw_n = (
                ef.get("count")
                if "count" in ef
                else ef.get("qty")
                if "qty" in ef
                else ef.get("amount")
                if "amount" in ef
                else ef.get("delta")
                if "delta" in ef
                else ef.get("value")
                if "value" in ef
                else params.get("count", params.get("qty", params.get("amount", params.get("delta", params.get("value", 1)))))
            )
            if not isinstance(item_id, str) or not item_id.strip():
                return [EffectLog(kind="error", message="inventory.add missing item_id", effect=ef)]
            n = self._to_int(raw_n, default=1)
            inv = self._ensure_bucket(game_state, "inventory")
            inv[item_id] = self._to_int(inv.get(item_id, 0), default=0) + n
            logs.append(EffectLog(kind="applied", message=f"inventory.add: {item_id} +{n}", effect=ef))
            return logs

        if t in ("inventory.remove", "inv.remove"):
            item_id = (
                ef.get("item_id")
                or ef.get("id")
                or params.get("item_id")
                or params.get("id")
                or params.get("item")
            )
            raw_n = (
                ef.get("count")
                if "count" in ef
                else ef.get("qty")
                if "qty" in ef
                else ef.get("amount")
                if "amount" in ef
                else ef.get("delta")
                if "delta" in ef
                else ef.get("value")
                if "value" in ef
                else params.get("count", params.get("qty", params.get("amount", params.get("delta", params.get("value", 1)))))
            )
            if not isinstance(item_id, str) or not item_id.strip():
                return [EffectLog(kind="error", message="inventory.remove missing item_id", effect=ef)]
            n = self._to_int(raw_n, default=1)
            inv = self._ensure_bucket(game_state, "inventory")
            cur = self._to_int(inv.get(item_id, 0), default=0)
            new_v = cur - n
            if new_v <= 0:
                # clamp to 0 and remove key for cleanliness
                if item_id in inv:
                    inv.pop(item_id, None)
                logs.append(EffectLog(kind="applied", message=f"inventory.remove: {item_id} -{n} (now 0)", effect=ef))
            else:
                inv[item_id] = new_v
                logs.append(EffectLog(kind="applied", message=f"inventory.remove: {item_id} -{n} (now {new_v})", effect=ef))
            return logs

        # -----------------------------
        # Phase C: flag.int_add
        # -----------------------------
        if t in ("flag.int_add", "flag.add_int", "flag.inc_int"):
            key = (
                ef.get("key")
                or ef.get("flag")
                or params.get("flag_key")
                or params.get("key")
                or params.get("flag")
            )
            raw_d = (
                ef.get("delta")
                if "delta" in ef
                else ef.get("amount")
                if "amount" in ef
                else ef.get("value")
                if "value" in ef
                else params.get("delta", params.get("amount", params.get("value", 1)))
            )
            if not isinstance(key, str) or not key.strip():
                return [EffectLog(kind="error", message="flag.int_add missing key", effect=ef)]

            d = self._to_int(raw_d, default=1)
            flags = self._ensure_bucket(game_state, "flags")
            cur = self._to_int(flags.get(key, 0), default=0)
            flags[key] = cur + d
            logs.append(EffectLog(kind="applied", message=f"flag.int_add: {key}+={d} (now {flags[key]})", effect=ef))
            return logs

        # -----------------------------
        # Phase C: var.add (numeric only)
        # -----------------------------
        if t in ("var.add", "vars.add"):
            key = ef.get("key") or params.get("key")
            raw_d = (
                ef.get("delta")
                if "delta" in ef
                else ef.get("amount")
                if "amount" in ef
                else ef.get("value")
                if "value" in ef
                else params.get("delta", params.get("amount", params.get("value", 0)))
            )
            if not isinstance(key, str) or not key.strip():
                return [EffectLog(kind="error", message="var.add missing key", effect=ef)]

            d = self._to_float(raw_d, default=0.0)
            vars_ = self._ensure_bucket(game_state, "vars")
            cur = self._to_float(vars_.get(key, 0), default=0.0)
            new_v = cur + d
            vars_[key] = self._keep_int_if_possible(new_v)
            logs.append(EffectLog(kind="applied", message=f"var.add: {key}+={d}", effect=ef))
            return logs

        # -----------------------------
        # Phase B existing behaviors (unchanged)
        # -----------------------------
        if t in ("give_item", "grant_item", "add_item", "item"):
            item_id = ef.get("item_id") or ef.get("id")
            count = ef.get("count", 1)
            if not isinstance(item_id, str) or not item_id.strip():
                return [EffectLog(kind="error", message="give_item missing item_id", effect=ef)]
            try:
                n = int(count)
            except Exception:
                return [EffectLog(kind="error", message="give_item count is not int", effect=ef)]

            inv = game_state.setdefault("inventory", {})
            if not isinstance(inv, dict):
                game_state["inventory"] = {}
                inv = game_state["inventory"]

            inv[item_id] = int(inv.get(item_id, 0)) + n
            logs.append(EffectLog(kind="applied", message=f"give_item: {item_id} x{n}", effect=ef))
            return logs

        if t in ("set_flag", "flag", "flag.set"):
            params = ef.get("params") if isinstance(ef.get("params"), dict) else {}
            key = ef.get("key") or ef.get("flag") or params.get("flag_key") or params.get("key")
            value = ef.get("value", True)
            if "value" in params:
                value = params.get("value")
            if not isinstance(key, str) or not key.strip():
                return [EffectLog(kind="error", message="set_flag missing key", effect=ef)]

            flags = game_state.setdefault("flags", {})
            if not isinstance(flags, dict):
                game_state["flags"] = {}
                flags = game_state["flags"]

            flags[key] = value
            logs.append(EffectLog(kind="applied", message=f"set_flag: {key}={value!r}", effect=ef))
            return logs

        # MVP alias: gold.add -> vars["gold"] += amount
        if t == "gold.add":
            params = ef.get("params") if isinstance(ef.get("params"), dict) else {}
            amount = params.get("amount", params.get("delta", params.get("value", ef.get("amount", ef.get("delta", ef.get("value", 0))))))

            try:
                d = float(amount)
            except Exception:
                return [EffectLog(kind="error", message="gold.add amount is not numeric", effect=ef)]

            vars_ = game_state.setdefault("vars", {})
            if not isinstance(vars_, dict):
                game_state["vars"] = {}
                vars_ = game_state["vars"]

            cur = vars_.get("gold", 0)
            try:
                cur_n = float(cur)
            except Exception:
                cur_n = 0.0

            new_v = cur_n + d
            if abs(new_v - int(new_v)) < 1e-9:
                new_v = int(new_v)

            vars_["gold"] = new_v
            logs.append(EffectLog(kind="applied", message=f"gold.add: gold+={d}", effect=ef))
            return logs

        if t in ("set_var", "var", "set"):
            key = ef.get("key")
            if not isinstance(key, str) or not key.strip():
                return [EffectLog(kind="error", message="set_var missing key", effect=ef)]
            value = ef.get("value")
            vars_ = game_state.setdefault("vars", {})
            if not isinstance(vars_, dict):
                game_state["vars"] = {}
                vars_ = game_state["vars"]

            vars_[key] = value
            logs.append(EffectLog(kind="applied", message=f"set_var: {key}={value!r}", effect=ef))
            return logs

        if t in ("add_var", "inc_var", "add", "inc"):
            key = ef.get("key")
            delta = ef.get("delta", ef.get("value", 0))
            if not isinstance(key, str) or not key.strip():
                return [EffectLog(kind="error", message="add_var missing key", effect=ef)]
            try:
                d = float(delta)
            except Exception:
                return [EffectLog(kind="error", message="add_var delta is not numeric", effect=ef)]

            vars_ = game_state.setdefault("vars", {})
            if not isinstance(vars_, dict):
                game_state["vars"] = {}
                vars_ = game_state["vars"]

            cur = vars_.get(key, 0)
            try:
                cur_n = float(cur)
            except Exception:
                cur_n = 0.0

            new_v = cur_n + d
            # keep int if possible
            if abs(new_v - int(new_v)) < 1e-9:
                new_v = int(new_v)

            vars_[key] = new_v
            logs.append(EffectLog(kind="applied", message=f"add_var: {key}+={d}", effect=ef))
            return logs

        return [EffectLog(kind="skipped", message=f"Unsupported effect.type: {t}", effect=ef)]