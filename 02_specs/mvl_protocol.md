# MVL Protocol v1.0

Engine: 1.0.0  
Spec: 1.3.0  
Structure: 1.2.0

Status: Active\
Scope: Schema Layer + Minimal Behavior Loop + Persistent State Validation

------------------------------------------------------------------------

# 1. Purpose

本文件定義「最小可行垂直切片驗證流程（Minimum Viable Loop, MVL）」。

目的： - 驗證 Schema 是否可支撐資料 - 驗證資料是否可驅動最小行為循環 -
偵測結構漂移（Architecture Drift） - 作為每次 Schema
升級前的強制回歸測試

------------------------------------------------------------------------

# 2. 官方驗證樣本

使用固定測試規則：

- 03_data/monsters/test_*.json
- 03_data/items/test_*.json
- 03_data/quests/test_*.json

所有以 `test_` 開頭之 JSON 檔案均視為 Validation Fixture，
不屬於正式遊戲內容。

MVL v2 以上版本將自動掃描上述資料夾。

------------------------------------------------------------------------

# 3. 驗證流程

## Step 1 --- Schema Gate

執行： python mvl_test_v2.py

預期： ✅ \[PASS\] 規格驗證成功

------------------------------------------------------------------------

## Step 2 --- Behavior Gate

執行： python mvl_test_v1.py

預期： - Schema PASS - Condition PASS - Numeric PASS - SUCCESS 顯示

------------------------------------------------------------------------

# 4. Boundary Test

修改 mock_player_state 等級值：

  測試值   預期
  -------- ------
  0        FAIL
  1        PASS
  10       PASS

------------------------------------------------------------------------

# 5. Drift Sentinel Test

在 JSON 最外層新增： "foo": 1

執行： python mvl_test_v2.py

預期： ❌ Additional properties are not allowed

測試完成後立即移除。

------------------------------------------------------------------------

# 6. Pattern Gate Test

修改 name 前綴為 text.\*

執行： python mvl_test_v2.py

預期 FAIL（regex 不符）。

------------------------------------------------------------------------

# 7. Regression Policy

以下情況必須重新執行 MVL：

-   修改 monster.schema.json
-   修改 condition.schema.json
-   修改 effect.schema.json
-   修改 common.schema.json
-   升級 Spec Version
-   修改 quest.schema.json
-   修改 save.schema.json（state persistence layer）

# 7.1. Compare Operator Convention（Data Layer）

凡 condition / compare 類型使用 `op` 欄位時：

- 必須使用 enum code：`eq | gt | gte | lt | lte`
- 禁止使用符號：`= | > | >= | < | <=`

此規範屬於 Schema Gate 的一部分，任何 fixture 違反應視為 FAIL。

------------------------------------------------------------------------

# 8. PASS Criteria

MVL 通過條件：

-   Schema Gate PASS
-   Behavior Gate PASS
-   Boundary Test 正確
-   Drift Sentinel 正確

------------------------------------------------------------------------

# 9. MVL v3 升級觸發條件（Activation Criteria）

MVL v3 並非自動進化機制。

僅在出現以下任一情況時，才可考慮升級至 v3：

1. Schema Gate PASS，但實際執行時因跨 schema 引用問題導致 runtime 錯誤。
2. 現行 MVL 無法驗證 Entity ID 是否存在（monster / item / flag 等）。
3. Condition 或 Effect 在 schema 驗證通過後，仍產生錯誤或不合理的遊戲狀態（語意層錯誤）。
4. 出現跨 schema 依賴鏈（dependency chain）造成邏輯不一致，但 v2 無法偵測。
5. 開發過程中反覆需要人工檢查，顯示語意驗證覆蓋不足。

若上述條件均未發生，  
則 MVL v2 仍為專案的正式驗證層。

---

## v3 治理啟動規則

在啟動 MVL v3 之前，必須：

- 提供實際失敗案例（Failure Example）
- 明確指出 v2 的驗證缺口
- 定義最小必要擴充範圍
- 評估維護成本與複雜度影響
- 新增 Design Decision（DD-XXX）
- 明確宣告：Entering Evolution Mode

MVL 的目的是維持穩定與一致性，  
而非預測性地建構靜態分析引擎。

------------------------------------------------------------------------


End of MVL Protocol v1.0
