# DSL-7: Effect 欄位與 Schema 列舉映射邏輯 (Draft)

## 1. 映射架構
所有在 `03_data/*.json` 中出現的 Effect 指令，必須與 `02_specs/schema/effect.schema.json` 中的 `enum` 列表達成 1:1 精確映射。

## 2. 命名漂移 (Naming Drift) 攔截規則
* **R-703 (Canonical Only)**: 僅允許符合 Schema 列舉的字串通過校驗。
* **廢棄指令攔截**: 偵測到 `flag.int_add` 時，必須強制要求修正為 `flag.add_int`。
* **R-704 (Structure Check)**: 所有指令格式必須為 `[domain].[action]`，且嚴禁以 `var.` 開頭。

## 3. 映射矩陣基準
* **flag.set** -> 映射至 `boolean` 型別列舉。
* **flag.add_int** -> 映射至 `integer` 型別列舉。
* **gold.add** -> 映射至 `integer` (>=0)。

## 4. 靜態掃描流程
1. **Enum Existence**: 核對 Data 層指令是否存在於 Spec Enum 中。
2. **Negative Filtering**: 過濾任何 `DEPRECATED` 或 `FORBIDDEN` 關鍵字。
3. **Type Consistency**: 核對指令後的 Value 型別是否符合矩陣定義。