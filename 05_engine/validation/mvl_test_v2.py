import json
import os
import warnings
from jsonschema import validate, RefResolver
from jsonschema.exceptions import ValidationError

# 關閉 RefResolver deprecation 警告（不影響功能）
warnings.filterwarnings("ignore", category=DeprecationWarning)


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _print_validation_error(schema_name: str, filename: str, e: ValidationError) -> None:
    instance_path = ".".join(str(p) for p in e.path) if e.path else "(root)"
    schema_path = ".".join(str(p) for p in e.schema_path) if e.schema_path else "(schema root)"

    print(f"❌ [FAIL] {schema_name} → {filename}")
    print(f"    - instance path: {instance_path}")
    print(f"    - schema path:   {schema_path}")
    print(f"    - message:       {e.message}")


def _validate_folder(schema_name, schema, resolver, folder_path):
    results = {"pass": 0, "fail": 0}

    if not os.path.isdir(folder_path):
        print(f"⚠️ [SKIP] 找不到資料夾：{folder_path}")
        return results

    files = sorted(
        fn for fn in os.listdir(folder_path)
        if fn.lower().startswith("test_") and fn.lower().endswith(".json")
    )

    if not files:
        print(f"⚠️ [SKIP] {folder_path} 無 test_*.json 檔案")
        return results

    for fn in files:
        path = os.path.join(folder_path, fn)
        try:
            with open(path, "r", encoding="utf-8") as f:
                instance = json.load(f)

            validate(instance=instance, schema=schema, resolver=resolver)

            print(f"✅ [PASS] {schema_name} → {fn}")
            results["pass"] += 1

        except ValidationError as e:
            _print_validation_error(schema_name, fn, e)
            results["fail"] += 1

        except Exception as e:
            print(f"❌ [ERROR] {schema_name} → {fn}")
            print(f"    - {str(e)}")
            results["fail"] += 1

    return results


def run_secure_validation():
    print("準備執行最小可行性循環測試...\n")

    root = _project_root()
    schema_dir = os.path.join(root, "02_specs", "schema")

    monster_schema_path = os.path.join(schema_dir, "monster.schema.json")
    item_schema_path = os.path.join(schema_dir, "item.schema.json")
    registry_schema_path = os.path.join(schema_dir, "registry.schema.json")
    
    # 載入 registry schema
    with open(registry_schema_path, "r", encoding="utf-8") as f:
        registry_schema = json.load(f)
    # 載入 monster schema
    with open(monster_schema_path, "r", encoding="utf-8") as f:
        monster_schema = json.load(f)

    # 建立 resolver（讓 $ref 找到 common.schema.json）
    schema_base_uri = "file:///" + schema_dir.replace("\\", "/") + "/"
    resolver = RefResolver(base_uri=schema_base_uri, referrer=monster_schema)

    total_pass = 0
    total_fail = 0

    # -----------------------------
    # Monster
    # -----------------------------
    monster_dir = os.path.join(root, "03_data", "monsters")
    monster_result = _validate_folder(
        "monster@1.x",
        monster_schema,
        resolver,
        monster_dir
    )

    total_pass += monster_result["pass"]
    total_fail += monster_result["fail"]

    # -----------------------------
    # Item
    # -----------------------------
    with open(item_schema_path, "r", encoding="utf-8") as f:
        item_schema = json.load(f)

    item_dir = os.path.join(root, "03_data", "items")
    item_result = _validate_folder(
        "item@1.0",
        item_schema,
        resolver,
        item_dir
    )

    total_pass += item_result["pass"]
    total_fail += item_result["fail"]

    # -----------------------------
    # Quest
    # -----------------------------
    quest_schema_path = os.path.join(schema_dir, "quest.schema.json")
    with open(quest_schema_path, "r", encoding="utf-8") as f:
        quest_schema = json.load(f)

    quest_dir = os.path.join(root, "03_data", "quests")
    quest_result = _validate_folder(
        "quest@1.0",
        quest_schema,
        resolver,
        quest_dir
    )

    total_pass += quest_result["pass"]
    total_fail += quest_result["fail"]

    # -----------------------------
    # Registry (NEW - REG-002)
    # -----------------------------
    registry_dir = os.path.join(root, "03_data", "registries")

    def _validate_registry_folder(schema, folder_path):
        results = {"pass": 0, "fail": 0}

        if not os.path.isdir(folder_path):
            print(f"⚠️ [SKIP] registry 資料夾不存在：{folder_path}")
            return results

        files = sorted(
            fn for fn in os.listdir(folder_path)
            if fn.lower().endswith(".json")
        )

        if not files:
            print(f"⚠️ [SKIP] registry 無 JSON 檔案")
            return results

        for fn in files:
            path = os.path.join(folder_path, fn)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    instance = json.load(f)

                validate(instance=instance, schema=schema)

                print(f"✅ [PASS] registry@1.4 → {fn}")
                results["pass"] += 1

            except ValidationError as e:
                _print_validation_error("registry@1.4", fn, e)
                results["fail"] += 1

            except Exception as e:
                print(f"❌ [ERROR] registry@1.4 → {fn}")
                print(f"    - {str(e)}")
                results["fail"] += 1

        return results

    registry_result = _validate_registry_folder(
        registry_schema,
        registry_dir
    )

    total_pass += registry_result["pass"]
    total_fail += registry_result["fail"]


    # -----------------------------
    # Summary
    # -----------------------------
    print("\n==============================")
    print("📊 驗證總結")
    print("==============================")
    print(f"PASS : {total_pass}")
    print(f"FAIL : {total_fail}")

    if total_fail == 0:
        print("\n🎉 所有測試通過！")
    else:
        print("\n⚠️ 存在驗證失敗項目，請檢查上方錯誤。")


if __name__ == "__main__":
    run_secure_validation()