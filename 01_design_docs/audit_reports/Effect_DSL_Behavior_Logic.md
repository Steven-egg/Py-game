# Effect DSL 核心解析行為驗證矩陣 (Behavior Logic)

## 1. 目的
本文件定義 Effect DSL 在 Engine 執行層的預期邏輯行為。本規範確立 **SSOT (Single Source of Truth)**，定義邏輯輸入與輸出的邊界，並整合 **E1 Coverage Matrix** 驗證規格。
*   **Evolution Mode:** `CLOSED`
*   **Verified DSLs:** `gold.add`, `flag.set`, `flag.add_int`, `inventory.add`, `inventory.remove`
*   **Prohibited (Naming Drift):** `flag.int_add`, `inventory.plus`, `inventory.delete`, `var.add` (engine-only)

## 2. [AC 1] 邏輯行為矩陣 (Behavior Matrix)

| 指令 (DSL) | 正常參數 | 執行層預期行為 (Logic Level) | 備註 |
| :--- | :--- | :--- | :--- |
| `gold.add` | `int` | `save.gold` = `current + delta` | 數值增加邏輯 |
| `flag.set` | `bool` | 修改 `save.flags[ID]` 之布林值 | 狀態開關 (覆寫語意) |
| `flag.add_int`| `int` | `save.flags[ID]` 之整數值 `+delta` | 計數累加 (支援負數) |
| `inventory.add`| `id, qty`| `save.inventory[ID]` 數量增加 | 累加既有物品或新增 Key |
| `inventory.remove`| `id, qty`| `save.inventory[ID]` 數量扣減 | 扣減量不得導致負數 |

## 3. [AC 2] 錯誤邊界與攔截定義 (Error Boundaries)

| 異常情境 | 預期錯誤類型 (Error Type) | 處理原則 |
| :--- | :--- | :--- |
| **數值溢出** | `VAL_OVERFLOW` | 封鎖變更或強制錨定最大值 (依 `common.schema` 定義) |
| **負數輸入** | `INVALID_OPERAND` | 在 `gold.add` 等非位移指令中攔截，要求改用減法指令 |
| **型別不對稱** | `TYPE_CLASH_ERROR` | 拒絕執行，如：對 Boolean 執行 `add_int` |
| **未註冊調用** | `REGISTRY_MISSING` | 拒絕執行，視為無效標記 |
| **下溢 (Underflow)**| `UNDERFLOW_ERROR` | 針對 `inventory.remove`，若扣除後 < 0 則明確報錯 |

## 4. [AC 3] 驗證清單 (E1 Coverage Matrix)
*本小節整合自 E1 驗證規範，作為設計級驗證基準。*

### 4.1 核心貨幣 (Gold)
| ID | 類別 | 驗證目標 | 預期結果 |
| :--- | :--- | :--- | :--- |
| E1-001 | Schema | 驗證名稱為合法 canonical DSL | 通過 schema gate |
| E1-004 | Behavior | 驗證執行後 state 寫入成功 | 金幣值增加，狀態由 `save.game_state` 讀寫一致 |
| E1-008 | Negative | 參數型別錯誤 (如傳入 `"10"`) | 拒絕執行，不得 silent cast |

### 4.2 旗標狀態 (Flags)
| ID | 類別 | 驗證目標 | 預期結果 |
| :--- | :--- | :--- | :--- |
| E1-015 | Behavior | 驗證覆寫更新 | 先設為 `false` 再設為 `true`，最終值為 `true` |
| E1-020 | Negative | 使用 non-canonical (`flag.int_add`) | Validation 失敗，阻止進 content |
| E1-025 | Behavior | 驗證初始缺值處理 | **[待實測]** 依 Engine 合約決定報錯或初始化 |

### 4.3 物品清單 (Inventory)
| ID | 類別 | 驗證目標 | 預期結果 |
| :--- | :--- | :--- | :--- |
| E1-037 | Behavior | 驗證累加既有物品 | 數量加總而非覆寫 |
| E1-047 | Behavior | 驗證扣到 0 的處理 | **[待實測]** 確認保留 Key 或移除 Key |
| E1-051 | Negative | 移除數量超過現有數量 | 明確報錯，阻止狀態進入非法負值 |

## 5. [AC 4] 治理與共用規則
* **SSOT 基準**: 所有 Behavior 測試均以 `save.game_state` 為最終比對面。
* **命名攔截**: 嚴格禁止 `naming drift`。任何非 `Verified DSLs` 表列之名稱一律攔截。
* **跨層級依賴**:
    1. 必須讀取 `02_specs/schema/flags.registry.json` 的 `initial_value`。
    2. 必須符合 `common.schema.json` 的 `max/min` 硬性限制。
    3. 執行前須通過 `DSL-7_Effect_Mapping_Logic.md` 靜態檢核。

---
