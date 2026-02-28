from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from quest_runtime import ActiveQuest


class SaveManagerError(Exception):
    pass


def _ensure_dict(v: Any) -> Dict[str, Any]:
    return v if isinstance(v, dict) else {}


def _ensure_list_str(v: Any) -> List[str]:
    if not isinstance(v, list):
        return []
    out: List[str] = []
    for x in v:
        if isinstance(x, str) and x.strip():
            out.append(x.strip())
    return out


def _normalize_game_state(gs: Any) -> Dict[str, Any]:
    """
    MVL baseline state (SSOT for runtime condition/effect):
      game_state = {
        "flags": {...},
        "inventory": {...},
        "vars": {...},
      }
    Tolerant: if save file is missing buckets or has wrong types, fix them.
    """
    out = _ensure_dict(gs)

    # Required buckets for Phase B
    flags = out.get("flags")
    inv = out.get("inventory")
    vars_ = out.get("vars")

    out["flags"] = flags if isinstance(flags, dict) else {}
    out["inventory"] = inv if isinstance(inv, dict) else {}
    out["vars"] = vars_ if isinstance(vars_, dict) else {}

    return out


@dataclass
class SaveBlob:
    """
    MVL save format (engine-owned, not schema-owned):
      {
        "version": "engine_phase_b_mvl_1",
        "active_quest": {...} | null,
        "completed_ids": [ "q.x", ... ],
        "game_state": {...}
      }
    """
    version: str
    active_quest: Optional[ActiveQuest]
    game_state: Dict[str, Any]
    completed_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "active_quest": self.active_quest.to_dict() if self.active_quest else None,
            "completed_ids": list(self.completed_ids),
            "game_state": self.game_state,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SaveBlob":
        if not isinstance(d, dict):
            d = {}

        aq = d.get("active_quest")
        active = ActiveQuest.from_dict(aq) if isinstance(aq, dict) else None

        # Normalize + ensure required buckets
        gs = _normalize_game_state(d.get("game_state"))

        # NEW: completed quest ids (backward compatible)
        completed_ids = _ensure_list_str(d.get("completed_ids"))

        ver = d.get("version")
        if not isinstance(ver, str) or not ver.strip():
            ver = "engine_phase_b_mvl_1"

        return SaveBlob(
            version=ver,
            active_quest=active,
            game_state=gs,
            completed_ids=completed_ids,
        )


class SaveManager:
    def __init__(self, project_root: Optional[Path] = None) -> None:
        # save_manager.py is under 05_engine/, so parents[1] should be repo root
        self.project_root = project_root or Path(__file__).resolve().parents[1]
        self.save_dir = self.project_root / "05_engine" / "save"
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def slot_path(self, slot: str = "slot_1") -> Path:
        safe = "".join(ch for ch in slot if ch.isalnum() or ch in ("_", "-", "."))
        if not safe:
            safe = "slot_1"
        return self.save_dir / f"{safe}.json"

    def load(self, slot: str = "slot_1") -> SaveBlob:
        fp = self.slot_path(slot)

        if not fp.exists():
            # MVL: if no save, return empty baseline with required buckets
            return SaveBlob(
                version="engine_phase_b_mvl_1",
                active_quest=None,
                game_state=_normalize_game_state({}),
                completed_ids=[],
            )

        try:
            raw = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            raise SaveManagerError(f"Failed to read save file: {fp} ({e})")

        if not isinstance(raw, dict):
            raise SaveManagerError(f"Save file must be a JSON object: {fp}")

        blob = SaveBlob.from_dict(raw)

        # Optional: keep save files "self-healing" (non-fatal). If the loaded file is missing
        # required buckets / fields, write back normalized format so future runs are clean.
        try:
            normalized = blob.to_dict()
            if (
                normalized.get("game_state") != raw.get("game_state")
                or normalized.get("version") != raw.get("version")
                or normalized.get("completed_ids") != raw.get("completed_ids")
            ):
                fp.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            # never fail load due to normalization write-back
            pass

        return blob

    def save(self, blob: SaveBlob, slot: str = "slot_1") -> Path:
        fp = self.slot_path(slot)

        # Defensive normalize before save
        blob.game_state = _normalize_game_state(blob.game_state)
        blob.completed_ids = _ensure_list_str(blob.completed_ids)

        try:
            fp.write_text(json.dumps(blob.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            raise SaveManagerError(f"Failed to write save file: {fp} ({e})")

        return fp