# DSL-7: Registry 註冊標準規範 (Draft)

## 1. 目的
本文件定義 `02_specs/schema/flags.registry.json` 的條目規範，確保強型別對齊並建立權限邊界，防止設計漂移。

## 2. 註冊條目結構規範
所有 Flag 註冊條目必須嚴格遵循以下 JSON Schema 邏輯：
* **id**: 唯一識別碼，格式 `[a-z0-9_]+`。嚴禁包含 `var.` 前綴。
* **type**: 僅限 `boolean` 或 `integer`。
* **scope**: 強制為 `content`。嚴禁出現 `engine` 或 `internal` 級別。
* **initial_value**: 預設值必須與型別對齊（Boolean: false / Integer: 0）。

## 3. 治理規則
* **R-701 (Namespace Guard)**: 若註冊條目偵測到 `var.` 起手式，該註冊視為無效且違反權限隔離原則。
* **R-702 (Type Alignment)**: Effect 指令必須與 Flag 型別嚴格映射（如 `flag.add_int` 僅能指向 `type: integer` 的 Flag）。

## 4. 審核檢查點 (Audit Checkpoints)
* [ ] 條目清單中完全不存在 `var.` 字眼。
* [ ] 所有的 `type` 僅存在於 `boolean` 與 `integer` 之中。