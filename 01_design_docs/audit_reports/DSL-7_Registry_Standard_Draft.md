這是一個將**「設計規格 (Spec)」**與**「實作標準 (Standard)」**整合的過程。透過這次合併，我們能將「為什麼要這樣設計（治理原則）」與「具體要怎麼寫（條目規範）」統一，消除原本 Draft 文件過於空洞的問題。

以下是為你整合後的程式碼，你可以直接全選貼上並取代原有的 `DSL-7_Registry_Standard_Draft.md` 內容：

---

# DSL-7: Registry 註冊標準與治理規範 (Standard & Spec)

## 1. 目的
本文件定義 Registry 的結構設計規格與 `02_specs/schema/*.registry.json` 的條目規範。其核心目標是建立 **Schema–Data 映射層**，確保強型別對齊並落實 **SSOT (Single Source of Truth)** 治理，防止設計漂移。

## 2. 分層定位與核心原則
根據 **DD-020** 與 **DD-021** 治理規則，Registry 的定位如下：

*   **Canonical Authority**: DSL 命名權威 **永遠在 Schema**，Registry 僅作為輔助治理的「映射層」，不得創造或修改命名。
*   **Mapping-only**: Registry 僅負責「對齊、映射、標記」，不定義語義、邏輯或 Runtime 行為。
*   **Layer Position**:
    *   `02_specs/schema/`: DSL Contract（權威來源）。
    *   `03_data/registries/`: Registry Data（實作映射）。

## 3. 註冊條目結構規範 (Entry Schema)
所有註冊條目必須遵循以下邏輯，確保與數據結構對齊：

| 欄位 (Field) | 型別與格式 | 說明與約束 |
| :--- | :--- | :--- |
| `id` | `[a-z0-9_]+` | 唯一識別碼，嚴禁包含 `var.` 前綴。 |
| `canonical_name` | `string` | **[Spec]** 對應 Schema 定義的唯一合法名稱。 |
| `type` | `enum` | 僅限 `boolean` 或 `integer`。 |
| `scope` | `string` | 強制為 `content`。嚴禁出現 `engine` 或 `internal`。 |
| `initial_value` | `mixed` | 預設值必須與型別對齊 (False / 0)。 |
| `status` | `enum` | 治理狀態：`allowed` / `blocked` / `reserved`。 |

## 4. 治理規則 (Governance Rules)

### 4.1 命名與命名空間隔離 (Namespace Guard)
*   **R-701**: 若註冊條目偵測到 `var.` 起手式，該註冊視為無效且違反權限隔離原則。
*   **R-702 (Naming Drift)**: 所有非 Canonical 名稱必須放置於 `aliases` 欄位並標記為 `blocked`，嚴禁進入正式調用。

### 4.2 型別與行為映射 (Type Alignment)
*   **R-703**: Effect 指令必須與 Flag 型別嚴格映射。例如：`flag.add_int` 僅能指向 `type: integer` 的條目。
*   **R-704**: Registry 僅能透過 `coverage_gate` 標記驗證狀態，不具備執行層的決策權。

## 5. 審核檢查點 (Audit Checkpoints)
在 Phase D.4 掃描時，必須通過以下檢查：
*   [ ] 條目清單中完全不存在 `var.` 字眼（符合 DD-021）。
*   [ ] 所有的 `type` 僅存在於 `boolean` 與 `integer` 之中。
*   [ ] `canonical_name` 與 `02_specs/schema/` 下的定義完全一致。
*   [ ] 所有的 `status` 均有對應的治理理由（如對應 DD-020）。

## 6. 演進邊界 (Evolution Boundary)
以下變更 **必須** 經過 DD 判定並切換至 `Evolution Mode: OPEN`：
*   Registry 成為 DSL 命名權威。
*   Registry 參與 Runtime 邏輯決策（如：動態 Gating）。
*   Registry 驅動 Schema 自動生成。

---

### 合併要點說明：
1.  **整合治理原則**：將原本 `Registry Schema Spec` 中關於 `Canonical Authority` 與 `Governance-driven` 的核心設計概念併入第 2 節與第 4 節，這補足了原本 Draft 缺乏的「設計為什麼要這樣做」的理論基礎[cite: 4, 5]。
2.  **規格化欄位定義**：將 Spec 建議的 `status`, `canonical_name` 等治理欄位與原本 Standard 的 `id`, `type` 實作欄位整合進第 3 節的表格中[cite: 4, 5]。
3.  **落實治理規則 (R-7xx)**：保留並強化了對 `var.` 前綴的攔截（Namespace Guard），這與你的 **SSOT** 與 **權限隔離** 目標高度一致[cite: 5]。
4.  **Token 與層級優化**：合併後，原本散落在兩個文件的資訊（一個講設計方向，一個講欄位限制）現在合併為一個 **「從設計到落實」** 的完整規範。

這份文件現在可以作為 `DSL-7_Registry_Standard.md` 正式啟用了。