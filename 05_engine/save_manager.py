from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from quest_runtime import ActiveQuest


class SaveManagerError(Exception):
    pass


DEFAULT_SAVE_SCHEMA = "save@1.0"
DEFAULT_ENGINE_VERSION = "1.0.0"
DEFAULT_CONTENT_MANIFEST_HASH = "dev_local"
DEFAULT_LOCATION = "start_village"


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


def _ensure_nonempty_str(v: Any, default: str) -> str:
    if isinstance(v, str) and v.strip():
        return v.strip()
    return default


def _normalize_game_state(gs: Any) -> Dict[str, Any]:
    """
    Phase D.2 baseline state (persistent SSOT for runtime condition/effect + location):
      game_state = {
        "flags": {...},
        "inventory": {...},
        "vars": {...},
        "current_location": "start_village",
      }

    Tolerant:
    - if save file is missing buckets or has wrong types, fix them
    - if current_location is missing / invalid type, restore default
    """
    out = _ensure_dict(gs)

    flags = out.get("flags")
    inv = out.get("inventory")
    vars_ = out.get("vars")
    loc = out.get("current_location")

    out["flags"] = flags if isinstance(flags, dict) else {}
    out["inventory"] = inv if isinstance(inv, dict) else {}
    out["vars"] = vars_ if isinstance(vars_, dict) else {}
    out["current_location"] = loc.strip() if isinstance(loc, str) and loc.strip() else DEFAULT_LOCATION

    return out


@dataclass
class SaveBlob:
    """
    Save format aligned to save.schema.json:

      {
        "save_schema": "save@1.0",
        "engine_version": "1.0.0",
        "content_manifest_hash": "dev_local",
        "active_quest": {...} | null,
        "game_state": {...},
        "completed_ids": ["q.x", ...]
      }

    Backward compatibility:
    - old save files may still contain "version"
    - missing metadata fields are auto-filled with defaults
    """
    save_schema: str
    engine_version: str
    content_manifest_hash: str
    active_quest: Optional[ActiveQuest]
    game_state: Dict[str, Any]
    completed_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "save_schema": self.save_schema,
            "engine_version": self.engine_version,
            "content_manifest_hash": self.content_manifest_hash,
            "active_quest": self.active_quest.to_dict() if self.active_quest else None,
            "game_state": self.game_state,
            "completed_ids": list(self.completed_ids),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SaveBlob":
        if not isinstance(d, dict):
            d = {}

        aq = d.get("active_quest")
        active = ActiveQuest.from_dict(aq) if isinstance(aq, dict) else None

        gs = _normalize_game_state(d.get("game_state"))
        completed_ids = _ensure_list_str(d.get("completed_ids"))

        # New metadata fields (Phase D.2 / Spec 1.3.0)
        save_schema = _ensure_nonempty_str(d.get("save_schema"), DEFAULT_SAVE_SCHEMA)
        engine_version = _ensure_nonempty_str(d.get("engine_version"), DEFAULT_ENGINE_VERSION)
        content_manifest_hash = _ensure_nonempty_str(
            d.get("content_manifest_hash"),
            DEFAULT_CONTENT_MANIFEST_HASH,
        )

        # Backward compatibility note:
        # old save files may still have "version", but it is no longer part of schema output.
        # We intentionally ignore it after load normalization.

        return SaveBlob(
            save_schema=save_schema,
            engine_version=engine_version,
            content_manifest_hash=content_manifest_hash,
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
            return SaveBlob(
                save_schema=DEFAULT_SAVE_SCHEMA,
                engine_version=DEFAULT_ENGINE_VERSION,
                content_manifest_hash=DEFAULT_CONTENT_MANIFEST_HASH,
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

        # Self-healing write-back:
        # normalize old / incomplete save files into current schema-aligned format.
        try:
            normalized = blob.to_dict()
            if normalized != raw:
                fp.write_text(
                    json.dumps(normalized, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
        except Exception:
            # Never fail load due to normalization write-back
            pass

        return blob

    def save(self, blob: SaveBlob, slot: str = "slot_1") -> Path:
        fp = self.slot_path(slot)

        # Defensive normalize before save
        blob.save_schema = _ensure_nonempty_str(blob.save_schema, DEFAULT_SAVE_SCHEMA)
        blob.engine_version = _ensure_nonempty_str(blob.engine_version, DEFAULT_ENGINE_VERSION)
        blob.content_manifest_hash = _ensure_nonempty_str(
            blob.content_manifest_hash,
            DEFAULT_CONTENT_MANIFEST_HASH,
        )
        blob.game_state = _normalize_game_state(blob.game_state)
        blob.completed_ids = _ensure_list_str(blob.completed_ids)

        try:
            fp.write_text(
                json.dumps(blob.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            raise SaveManagerError(f"Failed to write save file: {fp} ({e})")

        return fp