import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "03_data"
REGISTRY_DIR = DATA_DIR / "registries"

SCHEMA_MAP = {
    "quests": "02_specs/schema/quest.schema.json",
    "items": "02_specs/schema/item.schema.json",
    "monsters": "02_specs/schema/monster.schema.json",
}

FORBIDDEN_DSL = {
    "flag.int_add",
    "var.add",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"[ERROR] JSON parse failed: {path} ({exc})")


def load_registry_entries(path: Path) -> List[Dict[str, Any]]:
    obj = load_json(path)

    if not isinstance(obj, dict):
        raise ValidationError(f"[ERROR] invalid registry format: {path}")

    entries = obj.get("entries")
    if not isinstance(entries, list):
        raise ValidationError(f"[ERROR] invalid registry entries: {path}")

    return entries


def load_allowed_keys() -> Tuple[Set[str], Set[str]]:
    flag_registry = REGISTRY_DIR / "flags.registry.json"
    var_registry = REGISTRY_DIR / "vars.registry.json"

    if not flag_registry.exists():
        raise ValidationError(f"[ERROR] missing registry: {flag_registry}")

    if not var_registry.exists():
        raise ValidationError(f"[ERROR] missing registry: {var_registry}")

    flag_keys = {
        entry["canonical_name"]
        for entry in load_registry_entries(flag_registry)
        if entry.get("status") == "allowed" and "canonical_name" in entry
    }

    var_keys = {
        entry["canonical_name"]
        for entry in load_registry_entries(var_registry)
        if entry.get("status") == "allowed" and "canonical_name" in entry
    }

    return flag_keys, var_keys


def iter_json_files() -> List[Tuple[str, Path]]:
    files: List[Tuple[str, Path]] = []

    for folder_name in SCHEMA_MAP:
        folder = DATA_DIR / folder_name

        if not folder.exists():
            print(f"[WARN] missing folder: {folder}")
            continue

        for path in folder.rglob("*.json"):
            if path.name.endswith(".schema.json"):
                continue

            files.append((folder_name, path))

    return files


def scan_node(
    node: Any,
    path: Path,
    flag_keys: Set[str],
    var_keys: Set[str],
) -> None:
    if isinstance(node, dict):
        dsl_type = node.get("type")

        if isinstance(dsl_type, str):
            if dsl_type in FORBIDDEN_DSL:
                raise ValidationError(f"[ERROR] DSL violation: {dsl_type} ({path})")

            params = node.get("params")
            if isinstance(params, dict):
                key = params.get("key")

                if isinstance(key, str):
                    if key.startswith("flg.") and key not in flag_keys:
                        raise ValidationError(
                            f"[ERROR] registry mismatch: flag key not found: {key} ({path})"
                        )

                    if key.startswith("var.") and key not in var_keys:
                        raise ValidationError(
                            f"[ERROR] registry mismatch: var key not found: {key} ({path})"
                        )

        for value in node.values():
            scan_node(value, path, flag_keys, var_keys)

    elif isinstance(node, list):
        for item in node:
            scan_node(item, path, flag_keys, var_keys)


def validate_file(path: Path, flag_keys: Set[str], var_keys: Set[str]) -> Dict[str, Any]:
    obj = load_json(path)

    if not isinstance(obj, dict):
        raise ValidationError(f"[ERROR] invalid data format: {path}")

    if "id" not in obj:
        raise ValidationError(f"[ERROR] missing data id: {path}")

    scan_node(obj, path, flag_keys, var_keys)

    return obj


def write_schema_if_missing(folder_name: str, path: Path, obj: Dict[str, Any]) -> bool:
    if "$schema" in obj:
        print(f"[SKIP] already has $schema: {path}")
        return False

    obj["$schema"] = SCHEMA_MAP[folder_name]
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] file patched: {path}")
    return True


def main() -> int:
    try:
        flag_keys, var_keys = load_allowed_keys()
        files = iter_json_files()

        validated: List[Tuple[str, Path, Dict[str, Any]]] = []

        # Phase 1: full validation, no writes
        for folder_name, path in files:
            obj = validate_file(path, flag_keys, var_keys)
            validated.append((folder_name, path, obj))

        # Phase 2: write only after all files pass
        patched = 0
        for folder_name, path, obj in validated:
            if write_schema_if_missing(folder_name, path, obj):
                patched += 1

        print(f"DONE. Patched files: {patched}")
        return 0

    except ValidationError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())