from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# Phase D.1 runtime-only location context
VALID_LOCATIONS: Dict[str, Dict[str, str]] = {
    "start_village": {"label": "織星村"},
    "forest_edge": {"label": "迷霧森林"},
    "town_gate": {"label": "王都大門"},
}

# Phase D.1 engine-side overlay gate
QUEST_LOCATION_GATES: Dict[str, str] = {
    "q.side.slime_hunt": "forest_edge",
}


def build_runtime_context() -> Dict[str, str]:
    return {
        "current_location": "start_village",
    }


def get_current_location(runtime_context: Dict[str, str]) -> str:
    return runtime_context.get("current_location", "start_village")


def get_location_label(location_id: str) -> str:
    meta = VALID_LOCATIONS.get(location_id)
    if not meta:
        return location_id
    return meta.get("label", location_id)


def list_locations() -> List[str]:
    return list(VALID_LOCATIONS.keys())


def is_valid_location(location_id: str) -> bool:
    return location_id in VALID_LOCATIONS


def set_current_location(runtime_context: Dict[str, str], location_id: str) -> Tuple[bool, str]:
    if not is_valid_location(location_id):
        return False, f"未知地點: {location_id}"

    runtime_context["current_location"] = location_id
    return True, f"已移動到 {location_id} ({get_location_label(location_id)})"


def get_required_location_for_quest(quest_id: str) -> Optional[str]:
    return QUEST_LOCATION_GATES.get(quest_id)


def check_location_gate(quest_id: str, runtime_context: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    required = get_required_location_for_quest(quest_id)
    if required is None:
        return True, None

    current = get_current_location(runtime_context)
    if current != required:
        return False, (
            "地點不對，無法完成任務。\n"
            f"需要地點: {required} ({get_location_label(required)})\n"
            f"目前地點: {current} ({get_location_label(current)})"
        )

    return True, None