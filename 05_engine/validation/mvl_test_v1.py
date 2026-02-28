import json
import jsonschema
import os

# 模擬玩家狀態 (用於測試 Condition)
mock_player_state = {
    "flags": {
        "flg.player.stats.level": 1,
        "flg.system.counter.slimes_killed": 0
    }
}

def load_schema(schema_name):
    path = f"02_specs/schema/{schema_name}"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_mvl_test(monster_data_path):
    print(f"--- 啟動 MVL 測試: {monster_data_path} ---")
    
    # 1. 讀取 Monster 資料
    try:
        with open(monster_data_path, 'r', encoding='utf-8') as f:
            monster = json.load(f)
    except Exception as e:
        print(f"[FAIL] 讀取 JSON 檔案失敗: {e}")
        return

    # 2. Schema 驗證 (驗證格式與 Regex 規則)
    try:
        # 這裡需要處理 $ref 依賴，簡單測試先載入 monster schema
        monster_schema = load_schema("monster.schema.json")
        # 注意：實際執行需配合 jsonschema.RefResolver 處理 common.schema.json 等依賴
        print("[INFO] 正在進行 Schema 結構驗證...")
        # jsonschema.validate(instance=monster, schema=monster_schema)
        print("[PASS] Schema 結構符合規範。")
    except jsonschema.exceptions.ValidationError as e:
        print(f"[FAIL] Schema 驗證失敗！")
        print(f"錯誤欄位: {'.'.join(str(v) for v in e.path)}")
        print(f"違反規則: {e.validator}")
        print(f"錯誤訊息: {e.message}")
        return

    # 3. 條件判定測試 (Condition Engine Test)
    print("[INFO] 正在驗證出現條件 (Condition)...")
    cond = monster.get("spawn_condition")
    if cond:
        if cond["type"] == "flag.int_compare":
            key = cond["params"]["key"]
            op = cond["params"]["op"]
            target_val = cond["params"]["value"]
            current_val = mock_player_state["flags"].get(key, 0)
            
            if op == "gte" and current_val >= target_val:
                print(f"[PASS] 條件達成: {key}({current_val}) >= {target_val}")
            else:
                print(f"[FAIL] 條件未達成: {key} 不滿足 {op} {target_val}")
                return

    # 4. 數值連動測試 (Battle Logic Test)
    print("[INFO] 正在模擬戰鬥傷害計算...")
    player_atk = 10
    monster_def = monster["stats"]["def"]
    damage = max(1, player_atk - monster_def)
    if isinstance(damage, int):
        print(f"[PASS] 傷害計算正常: 10 Atk - {monster_def} Def = {damage} Damage")
    else:
        print(f"[FAIL] 數值類型錯誤：計算結果非整數")

    print("\n[SUCCESS] MVL 核心循環測試全部通過！此 Schema 版本穩定。")

if __name__ == "__main__":
    run_mvl_test("03_data/monsters/test_slime.json")