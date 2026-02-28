import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # tools/ 的上一層 = repo root
DATA_DIR = ROOT / "03_data"

SCHEMA_MAP = {
    "quests": "02_specs/schema/quest.schema.json",
    "items": "02_specs/schema/item.schema.json",
    "monsters": "02_specs/schema/monster.schema.json",
}

def patch(folder_name: str):
    folder = DATA_DIR / folder_name
    if not folder.exists():
        print(f"[WARN] missing folder: {folder}")
        return 0

    schema_uri = SCHEMA_MAP[folder_name]
    changed = 0

    for fp in folder.rglob("*.json"):  # 保險：若你未來有子資料夾也會掃到
        # 跳過任何真的 schema 檔（一般不會在 03_data 內，但保險）
        if fp.name.endswith(".schema.json"):
            continue

        obj = json.loads(fp.read_text(encoding="utf-8"))

        # 只補缺的；不覆蓋你已有的 $schema
        if "$schema" not in obj:
            obj["$schema"] = schema_uri
            fp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
            print(f"[ADD] {fp} -> $schema={schema_uri}")

    return changed

total = 0
for k in ("quests", "items", "monsters"):
    total += patch(k)

print(f"DONE. Patched files: {total}")