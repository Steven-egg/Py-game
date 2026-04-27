from pathlib import Path
import json
from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_DIR = PROJECT_ROOT / "02_specs" / "schema"
DATA_DIR = PROJECT_ROOT / "03_data"

REGISTRY_SCHEMA_PATH = SCHEMA_DIR / "registry.schema.json"
REGISTRY_DIR = DATA_DIR / "registries"


class SchemaValidationError(Exception):
    pass


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SchemaValidationError(f"File not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise SchemaValidationError(f"Invalid JSON: {path} ({exc})") from exc


def validate_json_file(data_path: Path, schema_path: Path) -> None:
    schema = load_json(schema_path)
    data = load_json(data_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda error: error.path)

    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            messages.append(f"{data_path}: {location}: {error.message}")

        raise SchemaValidationError("\n".join(messages))


def validate_registry_files() -> list[Path]:
    """
    Validate registry JSON files against registry.schema.json.

    Important:
    - This function performs validation only.
    - It does not execute registry content.
    - It does not bind registry metadata to runtime behavior.
    - It does not modify DSL authority or existing schemas.
    """

    if not REGISTRY_DIR.exists():
        return []

    registry_files = sorted(REGISTRY_DIR.glob("*.json"))

    validated_files = []

    for registry_file in registry_files:
        validate_json_file(
            data_path=registry_file,
            schema_path=REGISTRY_SCHEMA_PATH,
        )
        validated_files.append(registry_file)

    return validated_files


def run_registry_validation() -> bool:
    validated_files = validate_registry_files()

    if not validated_files:
        print("[registry] SKIP: no registry JSON files found")
        return True

    for file_path in validated_files:
        print(f"[registry] PASS: {file_path}")

    return True


if __name__ == "__main__":
    try:
        run_registry_validation()
    except SchemaValidationError as exc:
        print("[registry] FAIL")
        print(exc)
        raise SystemExit(1)