from __future__ import annotations

import argparse
from typing import Any, Dict, Optional

from content_loader import ContentLoader
from effect_executor import EffectExecutor
from quest_runtime import ActiveQuest, QuestRuntime
from save_manager import SaveBlob, SaveManager


FATAL_KINDS = ("io", "json", "shape")


def _print_pack_summary(pack) -> None:
    print("=== content ===")
    print(f"quests:   {len(pack.quests)}")
    print(f"items:    {len(pack.items)}")
    print(f"monsters: {len(pack.monsters)}")
    print(f"issues:   {len(pack.issues)}")
    if pack.issues:
        print("\n--- issues ---")
        for it in pack.issues:
            print(f"[{it.kind}] {it.category} :: {it.file} :: {it.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Engine Phase B MVL CLI")
    parser.add_argument("--slot", default="slot_1", help="save slot name (default: slot_1)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("load", help="load content + show save snapshot")
    sub.add_parser("list", help="quest lobby list (READY/LOCKED/ACTIVE/DONE)")

    p_accept = sub.add_parser("accept", help="accept a quest")
    p_accept.add_argument("quest_id")

    p_progress = sub.add_parser("progress", help="report progress event")
    p_progress.add_argument("kind", choices=["item", "kill", "flag", "var"])
    p_progress.add_argument("key")
    p_progress.add_argument("value", nargs="?", default="1")

    sub.add_parser("check", help="check if active quest is complete")
    sub.add_parser("complete", help="check + apply effects + save (if complete) then clear active")
    sub.add_parser("show", help="show current save (active quest + game_state + completed_ids)")

    p_qdump = sub.add_parser("questdump", help="dump quest keys & likely objective/effect fields")
    p_qdump.add_argument("quest_id")

    args = parser.parse_args()

    # -----------------------------
    # Load content (always)
    # -----------------------------
    loader = ContentLoader()
    pack = loader.load_all(pattern="test_*.json")

    fatal = [it for it in pack.issues if it.kind in FATAL_KINDS]
    if fatal:
        _print_pack_summary(pack)
        return 2

    if args.cmd == "load":
        _print_pack_summary(pack)

    rt = QuestRuntime(pack.quests)
    ex = EffectExecutor()
    sm = SaveManager()

    save = sm.load(args.slot)
    active: Optional[ActiveQuest] = save.active_quest
    game_state: Dict[str, Any] = save.game_state
    completed_ids = list(save.completed_ids)

    # -----------------------------
    # Commands
    # -----------------------------
    if args.cmd == "load":
        print("\n=== save ===")
        print(f"slot: {args.slot}")
        print(f"active_quest: {active.quest_id if active else None}")
        print(f"completed_ids.len: {len(completed_ids)}")
        print(f"game_state keys: {sorted(game_state.keys())}")
        return 0

    if args.cmd == "list":
        # Quest Lobby
        # Status priority: DONE > ACTIVE > READY/LOCKED
        active_id = active.quest_id if (active is not None and active.completed_at is None) else None

        for qid in rt.list_quest_ids():
            if qid in completed_ids:
                print(f"[DONE]   {qid}")
                continue

            if active_id == qid:
                print(f"[ACTIVE] {qid}")
                continue

            ok, reason = rt.check_acceptable(qid, game_state)
            if ok:
                print(f"[READY]  {qid}")
            else:
                # show short reason (already human-readable)
                print(f"[LOCKED] {qid} :: {reason}")
        return 0

    if args.cmd == "questdump":
        q = rt.get_quest(args.quest_id)
        print(f"quest_id: {args.quest_id}")
        print("top-level keys:", sorted(list(q.keys())))

        def show_path(label: str, obj: Any) -> None:
            if isinstance(obj, dict):
                keys = sorted(list(obj.keys()))
                print(f"{label}: dict keys -> {keys}")

                if label.endswith("complete_condition") or ("type" in obj and "params" in obj):
                    ctype = obj.get("type")
                    params = obj.get("params")
                    if ctype is not None:
                        print(f"{label}.type: {ctype!r}")
                    if isinstance(params, dict):
                        conds = params.get("conditions")
                        if isinstance(conds, list):
                            preview = []
                            for c in conds[:3]:
                                if isinstance(c, dict):
                                    preview.append(c.get("type"))
                                else:
                                    preview.append(type(c).__name__)
                            print(f"{label}.params.conditions.len: {len(conds)}")
                            print(f"{label}.params.conditions.preview_types: {preview}")
                        else:
                            preview = {
                                "flag_key": params.get("flag_key") or params.get("key"),
                                "op": params.get("op"),
                                "value": params.get("value"),
                                "item_id": params.get("item_id"),
                                "qty": params.get("qty"),
                            }
                            preview = {k: v for k, v in preview.items() if v is not None}
                            if preview:
                                print(f"{label}.params.preview: {preview}")
                    return

                if label.endswith("rewards"):
                    effects = obj.get("effects")
                    if isinstance(effects, list):
                        print(f"{label}.effects.len: {len(effects)}")
                        if effects and isinstance(effects[0], dict):
                            e0 = effects[0]
                            print(f"{label}.effects[0].type: {e0.get('type')!r}")
                            print(f"{label}.effects[0] keys: {sorted(list(e0.keys()))}")
                    return

            elif isinstance(obj, list):
                first = obj[0] if obj else None
                print(f"{label}: list len -> {len(obj)}; first -> {type(first).__name__}")
            else:
                print(f"{label}: {type(obj).__name__} -> {obj!r}")

        suspects = (
            "objectives", "requirements",
            "complete_condition",
            "effects", "rewards",
            "on_complete", "completion",
            "reward", "reward_effects", "on_complete_effects",
        )

        for k in suspects:
            if k in q:
                show_path(k, q.get(k))

        if isinstance(q.get("completion"), dict):
            comp = q["completion"]
            for k in suspects:
                if k in comp:
                    show_path(f"completion.{k}", comp.get(k))

        if isinstance(q.get("on_complete"), dict):
            oc = q["on_complete"]
            for k in suspects:
                if k in oc:
                    show_path(f"on_complete.{k}", oc.get(k))

        return 0

    if args.cmd == "accept":
        # Guard: do not allow accepting a new quest while another is active (and not completed)
        if active is not None and active.completed_at is None:
            print("Cannot accept quest: another quest is already active")
            print(f"- active_quest: {active.quest_id} (not completed)")
            print("Tip: complete it first, or use --slot slot_2")
            return 1

        # Optional: prevent re-accepting completed quest (one-shot semantics)
        if args.quest_id in completed_ids:
            print(f"Cannot accept quest: {args.quest_id}")
            print("- already completed (completed_ids)")
            return 1

        # Enforce accept_condition if present
        ok, reason = rt.check_acceptable(args.quest_id, game_state)
        if not ok:
            print(f"Cannot accept quest: {args.quest_id}")
            print(f"- {reason}")
            return 1

        active = rt.accept(args.quest_id)
        blob = SaveBlob(
            version="engine_phase_b_mvl_1",
            active_quest=active,
            game_state=game_state,
            completed_ids=completed_ids,
        )
        fp = sm.save(blob, args.slot)
        print(f"Accepted quest: {active.quest_id}")
        print(f"Saved: {fp}")
        return 0

    if args.cmd == "progress":
        kind = args.kind
        key = args.key

        # Allow world-state injection for hall testing when no active quest
        # - item/kill require active quest (quest progress semantics)
        # - flag/var can write to save.game_state without active quest (SSOT semantics)
        if not active and kind in ("item", "kill"):
            print("No active quest. Use: accept <quest_id>")
            return 1

        kind = args.kind
        key = args.key

        if kind == "item":
            try:
                n = int(args.value)
            except Exception:
                n = 1
            rt.report_item_gained(active, key, n)
            inv = game_state.setdefault("inventory", {})
            if not isinstance(inv, dict):
                game_state["inventory"] = {}
                inv = game_state["inventory"]
            inv[key] = int(inv.get(key, 0)) + int(n)
            print(f"progress: item {key} +{n}")

        elif kind == "kill":
            try:
                n = int(args.value)
            except Exception:
                n = 1
            rt.report_monster_killed(active, key, n)

            flags = game_state.setdefault("flags", {})
            if not isinstance(flags, dict):
                game_state["flags"] = {}
                flags = game_state["flags"]

            kill_flag = f"flg.kill.{key}.count"
            try:
                cur = int(flags.get(kill_flag, 0))
            except Exception:
                cur = 0
            flags[kill_flag] = cur + int(n)

            print(f"progress: kill {key} +{n}")

        elif kind == "flag":
            vraw = args.value
            v: Any = True
            if isinstance(vraw, str):
                s = vraw.strip().lower()
                if s in ("true", "1", "yes", "y", "on"):
                    v = True
                elif s in ("false", "0", "no", "n", "off"):
                    v = False
                else:
                    v = vraw
            if active:
                rt.report_flag_set(active, key, v)
            flags = game_state.setdefault("flags", {})
            if not isinstance(flags, dict):
                game_state["flags"] = {}
                flags = game_state["flags"]
            flags[key] = v
            print(f"progress: flag {key}={v!r}")

        elif kind == "var":
            vraw = args.value
            v: Any = vraw
            if isinstance(vraw, str):
                try:
                    v = int(vraw)
                except Exception:
                    try:
                        v = float(vraw)
                    except Exception:
                        v = vraw
            if active:
                rt.report_var_set(active, key, v)
            vars_ = game_state.setdefault("vars", {})
            if not isinstance(vars_, dict):
                game_state["vars"] = {}
                vars_ = game_state["vars"]
            vars_[key] = v
            print(f"progress: var {key}={v!r}")

        blob = SaveBlob(
            version="engine_phase_b_mvl_1",
            active_quest=active,
            game_state=game_state,
            completed_ids=completed_ids,
        )
        fp = sm.save(blob, args.slot)
        print(f"Saved: {fp}")
        return 0

    if args.cmd == "check":
        if not active:
            print("No active quest.")
            return 1
        ok, reasons = rt.check_complete(active, game_state)
        print(f"active_quest: {active.quest_id}")
        print(f"complete: {ok}")
        if not ok:
            for r in reasons:
                print(f"- {r}")
        return 0

    if args.cmd == "complete":
        if not active:
            print("No active quest.")
            return 1

        ok, reasons = rt.check_complete(active, game_state)
        if not ok:
            print("Quest not complete.")
            for r in reasons:
                print(f"- {r}")
            return 1

        quest = rt.get_quest(active.quest_id)
        logs = ex.apply_quest_complete_effects(quest, game_state)
        rt.mark_completed(active)

        # A) record completion + clear active quest slot
        qid = active.quest_id
        if qid and qid not in completed_ids:
            completed_ids.append(qid)
        active = None

        blob = SaveBlob(
            version="engine_phase_b_mvl_1",
            active_quest=active,
            game_state=game_state,
            completed_ids=completed_ids,
        )
        fp = sm.save(blob, args.slot)

        print("Quest COMPLETE. Effects applied:")
        for lg in logs:
            print(f"[{lg.kind}] {lg.message}")
        print(f"Saved: {fp}")
        return 0

    if args.cmd == "show":
        print(f"slot: {args.slot}")
        print(f"version: {save.version}")
        print(f"active_quest: {active.to_dict() if active else None}")
        print(f"completed_ids: {completed_ids}")
        print(f"game_state: {game_state}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())