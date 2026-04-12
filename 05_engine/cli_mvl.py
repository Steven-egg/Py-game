from __future__ import annotations

import argparse
import shlex
from typing import Any, Dict, Optional

from content_loader import ContentLoader
from effect_executor import EffectExecutor
from location_runtime import (
    build_runtime_context,
    get_current_location,
    get_location_label,
    list_locations,
    set_current_location,
)
from quest_runtime import ActiveQuest, QuestRuntime
from save_manager import SaveBlob, SaveManager


FATAL_KINDS = ("io", "json", "shape")
DEFAULT_LOCATION = "start_village"


HELP_TEXT = """
Commands:
  help
  load
  list
  accept <quest_id>
  progress <kind> <key> [value]
    - kind: item | kill | flag | var
  check
  complete
  show
  questdump <quest_id>

  where
  locations
  move <location_id>

  save
  reload
  exit
""".strip()


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


def _save_slot(
    sm: SaveManager,
    slot: str,
    active: Optional[ActiveQuest],
    game_state: Dict[str, Any],
    completed_ids: list[str],
) -> str:
    blob = SaveBlob(
        save_schema="save@1.0",
        engine_version="1.0.0",
        content_manifest_hash="dev_local",
        active_quest=active,
        game_state=game_state,
        completed_ids=completed_ids,
    )
    return sm.save(blob, slot)


def _questdump(rt: QuestRuntime, quest_id: str) -> None:
    q = rt.get_quest(quest_id)
    print(f"quest_id: {quest_id}")
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


def _ensure_game_state_current_location(game_state: Dict[str, Any]) -> str:
    raw = game_state.get("current_location")

    if not isinstance(raw, str) or not raw.strip():
        game_state["current_location"] = DEFAULT_LOCATION
        return DEFAULT_LOCATION

    return raw.strip()


def _build_runtime_context_from_game_state(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase D.2 rule:
    - game_state['current_location'] is the persistent SSOT
    - runtime_context mirrors the persisted value for session use
    """
    runtime_context = build_runtime_context()

    location_id = _ensure_game_state_current_location(game_state)
    ok, _ = set_current_location(runtime_context, location_id)

    if not ok:
        game_state["current_location"] = DEFAULT_LOCATION
        set_current_location(runtime_context, DEFAULT_LOCATION)

    return runtime_context


def main() -> int:
    parser = argparse.ArgumentParser(description="Engine Phase D.2 Interactive MVL CLI")
    parser.add_argument("--slot", default="slot_1", help="save slot name (default: slot_1)")
    args = parser.parse_args()

    # -----------------------------
    # Load content once at startup
    # -----------------------------
    loader = ContentLoader()
    pack = loader.load_all(pattern="test_*.json")

    fatal = [it for it in pack.issues if it.kind in FATAL_KINDS]
    if fatal:
        _print_pack_summary(pack)
        return 2

    rt = QuestRuntime(pack.quests)
    ex = EffectExecutor()
    sm = SaveManager()

    save = sm.load(args.slot)
    active: Optional[ActiveQuest] = save.active_quest
    game_state: Dict[str, Any] = save.game_state
    completed_ids = list(save.completed_ids)

    # -----------------------------
    # Phase D.2 persistent location sync
    # game_state is SSOT; runtime_context mirrors it
    # -----------------------------
    runtime_context: Dict[str, Any] = _build_runtime_context_from_game_state(game_state)

    print("=== Engine Phase D.2 Interactive MVL CLI ===")
    print(f"slot: {args.slot}")
    print(f"current_location: {get_current_location(runtime_context)} ({get_location_label(get_current_location(runtime_context))})")
    print("Type 'help' for commands.")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0

        if not raw:
            continue

        try:
            parts = shlex.split(raw)
        except ValueError as exc:
            print(f"Parse error: {exc}")
            continue

        cmd = parts[0].lower()
        rest = parts[1:]

        # -----------------------------
        # Help / Exit
        # -----------------------------
        if cmd in ("help", "?"):
            print(HELP_TEXT)
            continue

        if cmd in ("exit", "quit"):
            print("Bye.")
            return 0

        # -----------------------------
        # Location commands
        # -----------------------------
        if cmd == "where":
            current = get_current_location(runtime_context)
            print(f"current_location: {current} ({get_location_label(current)})")
            continue

        if cmd == "locations":
            print("Available locations:")
            for loc in list_locations():
                print(f"- {loc} ({get_location_label(loc)})")
            continue

        if cmd == "move":
            if len(rest) != 1:
                print("Usage: move <location_id>")
                continue

            target_location = rest[0]
            ok, message = set_current_location(runtime_context, target_location)

            if ok:
                game_state["current_location"] = get_current_location(runtime_context)

            print(message)
            continue

        # -----------------------------
        # Content / save inspection
        # -----------------------------
        if cmd == "load":
            _print_pack_summary(pack)
            print("\n=== save ===")
            print(f"slot: {args.slot}")
            print(f"active_quest: {active.quest_id if active else None}")
            print(f"completed_ids.len: {len(completed_ids)}")
            print(f"game_state keys: {sorted(game_state.keys())}")
            print(f"current_location: {get_current_location(runtime_context)} ({get_location_label(get_current_location(runtime_context))})")
            continue

        if cmd == "show":
            print(f"slot: {args.slot}")
            print(f"active_quest: {active.to_dict() if active else None}")
            print(f"completed_ids: {completed_ids}")
            print(f"game_state: {game_state}")
            print(f"runtime_context: {runtime_context}")
            continue

        if cmd == "save":
            fp = _save_slot(sm, args.slot, active, game_state, completed_ids)
            print(f"Saved: {fp}")
            continue

        if cmd == "reload":
            save = sm.load(args.slot)
            active = save.active_quest
            game_state = save.game_state
            completed_ids = list(save.completed_ids)
            runtime_context = _build_runtime_context_from_game_state(game_state)

            print(f"Reloaded slot: {args.slot}")
            print("Runtime location restored from save.game_state.")
            print(f"current_location: {get_current_location(runtime_context)} ({get_location_label(get_current_location(runtime_context))})")
            continue

        # -----------------------------
        # Quest Lobby
        # -----------------------------
        if cmd == "list":
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
                    print(f"[LOCKED] {qid} :: {reason}")
            continue

        if cmd == "questdump":
            if len(rest) != 1:
                print("Usage: questdump <quest_id>")
                continue
            try:
                _questdump(rt, rest[0])
            except Exception as exc:
                print(f"questdump failed: {exc}")
            continue

        # -----------------------------
        # Quest accept
        # -----------------------------
        if cmd == "accept":
            if len(rest) != 1:
                print("Usage: accept <quest_id>")
                continue

            quest_id = rest[0]

            if active is not None and active.completed_at is None:
                print("Cannot accept quest: another quest is already active")
                print(f"- active_quest: {active.quest_id} (not completed)")
                print("Tip: complete it first, or use another save slot")
                continue

            if quest_id in completed_ids:
                print(f"Cannot accept quest: {quest_id}")
                print("- already completed (completed_ids)")
                continue

            try:
                ok, reason = rt.check_acceptable(quest_id, game_state)
            except Exception as exc:
                print(f"Cannot accept quest: {exc}")
                continue

            if not ok:
                print(f"Cannot accept quest: {quest_id}")
                print(f"- {reason}")
                continue

            try:
                active = rt.accept(quest_id)
            except Exception as exc:
                print(f"Accept failed: {exc}")
                continue

            fp = _save_slot(sm, args.slot, active, game_state, completed_ids)
            print(f"Accepted quest: {active.quest_id}")
            print(f"Saved: {fp}")
            continue

        # -----------------------------
        # Progress
        # -----------------------------
        if cmd == "progress":
            if len(rest) < 2:
                print("Usage: progress <kind> <key> [value]")
                print("Kinds: item | kill | flag | var")
                continue

            kind = rest[0]
            key = rest[1]
            value = rest[2] if len(rest) >= 3 else "1"

            if not active and kind in ("item", "kill"):
                print("No active quest. Use: accept <quest_id>")
                continue

            if kind == "item":
                try:
                    n = int(value)
                except Exception:
                    n = 1

                assert active is not None
                rt.report_item_gained(active, key, n)

                inv = game_state.setdefault("inventory", {})
                if not isinstance(inv, dict):
                    game_state["inventory"] = {}
                    inv = game_state["inventory"]
                inv[key] = int(inv.get(key, 0)) + int(n)
                print(f"progress: item {key} +{n}")

            elif kind == "kill":
                try:
                    n = int(value)
                except Exception:
                    n = 1

                assert active is not None
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
                vraw = value
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
                vraw = value
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

            else:
                print(f"Unsupported progress kind: {kind}")
                continue

            fp = _save_slot(sm, args.slot, active, game_state, completed_ids)
            print(f"Saved: {fp}")
            continue

        # -----------------------------
        # Completion check
        # -----------------------------
        if cmd == "check":
            if not active:
                print("No active quest.")
                continue

            try:
                ok, reasons = rt.check_complete(active, game_state, runtime_context)
            except TypeError:
                print("QuestRuntime.check_complete() does not accept runtime_context yet.")
                print("Please confirm quest_runtime.py has been updated for Phase D.1.")
                continue
            except Exception as exc:
                print(f"Check failed: {exc}")
                continue

            print(f"active_quest: {active.quest_id}")
            print(f"complete: {ok}")
            if not ok:
                for r in reasons:
                    print(f"- {r}")
            continue

        # -----------------------------
        # Complete quest
        # -----------------------------
        if cmd == "complete":
            if not active:
                print("No active quest.")
                continue

            try:
                ok, reasons = rt.check_complete(active, game_state, runtime_context)
            except TypeError:
                print("QuestRuntime.check_complete() does not accept runtime_context yet.")
                print("Please confirm quest_runtime.py has been updated for Phase D.1.")
                continue
            except Exception as exc:
                print(f"Complete check failed: {exc}")
                continue

            if not ok:
                print("Quest not complete.")
                for r in reasons:
                    print(f"- {r}")
                continue

            try:
                quest = rt.get_quest(active.quest_id)
                logs = ex.apply_quest_complete_effects(quest, game_state)
                rt.mark_completed(active)
            except Exception as exc:
                print(f"Completion failed: {exc}")
                continue

            qid = active.quest_id
            if qid and qid not in completed_ids:
                completed_ids.append(qid)
            active = None

            fp = _save_slot(sm, args.slot, active, game_state, completed_ids)

            print("Quest COMPLETE. Effects applied:")
            for lg in logs:
                print(f"[{lg.kind}] {lg.message}")
            print(f"Saved: {fp}")
            continue

        print(f"Unknown command: {cmd}")
        print("Type 'help' for commands.")


if __name__ == "__main__":
    raise SystemExit(main())