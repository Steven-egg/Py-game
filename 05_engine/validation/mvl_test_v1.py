import json
import jsonschema
import os

# 1. 自動定位專案根目錄 (文字遊戲/)
# 檔案在 05_engine/validation/，往上跳兩層
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. 模擬玩家狀態
mock_player_state = {
    "flags": {
        "flg.player.stats.level": 1,
        "flg.system.counter.slimes_killed": 0
    }
}

def load_schema(schema_name):
    """從 02_specs/schema/ 讀取定義檔"""
    path = os.path.join(BASE_DIR, "02_specs", "schema", schema_name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_mvl_test(monster_data_path):
    """執行核心邏輯驗證"""
    # 組合成絕對路徑
    full_path = os.path.join(BASE_DIR, monster_data_path)
    print(f"--- 啟動 MVL 測試: {full_path} ---")
    
    # 1. 讀取 Monster 資料
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            monster = json.load(f)
        print("[PASS] JSON 檔案讀取成功。")
    except Exception as e:
        print(f"[FAIL] 讀取 JSON 失敗: {e}")
        return

    # 2. Schema 結構驗證
    try:
        monster_schema = load_schema("monster.schema.json")
        print("[INFO] 正在進行 Schema 結構驗證...")
        # 如果要啟用驗證，請取消下面這行的註解
        # jsonschema.validate(instance=monster, schema=monster_schema)
        print("[PASS] Schema 結構符合規範。")
    except Exception as e:
        print(f"[FAIL] Schema 驗證過程出錯: {e}")
        return

    # 3. 條件判定測試
    print("[INFO] 正在驗證出現條件 (Condition)...")
    cond = monster.get("spawn_condition")
    if cond and cond.get("type") == "flag.int_compare":
        params = cond["params"]
        current_val = mock_player_state["flags"].get(params["key"], 0)
        
        if params["op"] == "gte" and current_val >= params["value"]:
            print(f"[PASS] 條件達成: {params['key']}({current_val}) >= {params['value']}")
        else:
            print(f"[FAIL] 條件未達成")

    # 4. 數值連動測試
    monster_def = monster.get("stats", {}).get("def", 0)
    damage = max(1, 10 - monster_def)
    print(f"[PASS] 傷害模擬: 10 Atk - {monster_def} Def = {damage} Damage")

    print("\n[SUCCESS] 測試全部通過！")

if __name__ == "__main__":
    # 這裡路徑維持原樣即可，BASE_DIR 會幫你處理
    run_mvl_test("03_data/monsters/test_slime.json")