# Effect DSL 核心解析行為驗證矩陣 (Behavior Logic)

## 1. 目的
本文件定義 Effect DSL 在 Engine 執行層的預期邏輯行為。本規範不涉及 Python 實作細節，僅定義邏輯輸入與輸出的邊界。

## 2. [AC 1] 邏輯行為矩陣 (Behavior Matrix)

| 指令 (DSL) | 正常參數 | 執行層預期行為 (Logic Level) | 備註 |
| :--- | :--- | :--- | :--- |
| `gold.add` | 500 | `save.gold` = `current + 500` | 數值增加邏輯 |
| `flag.set` | true/false | 修改 `save.flags` 對應 ID 之布林值 | 狀態開關邏輯 |
| `flag.add_int`| 1 | `save.flags` 對應 ID 之整數值 +1 | 計數累加邏輯 |

## 3. [AC 2] 錯誤邊界與攔截定義 (Error Boundaries)

| 異常情境 | 傳入數值範例 | 預期錯誤類型 (Error Type) | 處理原則 |
| :--- | :--- | :--- | :--- |
| **數值溢出** | `gold.add` 導致超過 999k | `VAL_OVERFLOW` | 封鎖變更或強制錨定最大值 |
| **負數輸入** | `gold.add: -100` | `INVALID_OPERAND` | 攔截，要求改用減法指令 |
| **型別不對稱** | 對 Boolean 執行 `add_int` | `TYPE_CLASH_ERROR` | 拒絕執行，拋出型別衝突警告 |
| **未註冊調用** | 調用不在 Registry 的 ID | `REGISTRY_MISSING` | 拒絕執行，視為無效標記 |

## 4. [AC 3] 跨層級依賴清單
* **依賴 A**: 必須讀取 `02_specs/schema/flags.registry.json` 的 `initial_value` 作為運算基準。
* **依賴 B**: 必須讀取 `common.schema.json` 獲取各項數值之 `max/min` 硬性限制。
* **依賴 C**: 執行前必須通過 `DSL-7_Effect_Mapping_Logic.md` 的靜態語法檢核。