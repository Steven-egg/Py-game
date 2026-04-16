# 01_design_docs/audit_reports/DSL-4_Consistency_Matrix.md

## 1. 審核元數據 (Audit Metadata)
* **報告編號**：DSL-4-20260416
* **基準版本**：Engine 1.0.0 / Spec 1.3.0
* **治理狀態**：Lock (Evolution Closed)
* **審核目標**：比對 `02_specs` (契約層) 與 `03_data` (內容層) 的 DSL 一致性，並為 Phase D.4 的 Registry 同步做準備。

---

## 2. DSL 規範性一致性矩陣 (Consistency Matrix)

根據 **DD-020 (Effect DSL Governance Charter)**，針對目前 Engine 支援的 Effect 進行存續判定：

| DSL 指令 (Effect) | 規範狀態 (Canonical) | 內容層現狀 (03_data) | 審核判定 (Audit Result) | 修正導引 (Remediation) |
| :--- | :--- | :--- | :--- | :--- |
| `gold.add` | **PASS** | 已廣泛應用於 Quest 獎勵 | 標準備案 | 無需變動 |
| `flag.set` | **PASS** | 用於進程標記 | 標準備案 | 無需變動 |
| `flag.int_add` | **DEPRECATED** | 存在於舊版測試數據 | **WARNING** | 需手動更新為 `flag.add_int` |
| `flag.add_int` | **PASS** | 規劃導入 | **LOCKED** | Canonical 命名，D.4 正式啟用 |
| `var.add` | **FORBIDDEN** | 禁止出現在 JSON 內容 | **CRITICAL** | 屬於 Engine-only 變量，嚴禁洩漏至 Data 層 |
| `inventory.add`| **PASS** | 物品獲得邏輯核心 | 標準備案 | 無需變動 |

---

## 3. 跨層級校驗邏輯定義 (Ref: DSL-7)

根據 **DSL-7** 規範，未來校驗流程必須遵循以下邏輯邊界，禁止自動化代碼介入：

* **垂直一致性**：`03_data/*.json` 中的 Effect 欄位必須完全映射至 `02_specs/schema/effect.schema.json` 定義的列舉值。
* **動態存在性檢核**：若 Effect 涉及 `flag` 操作，其 Key 必須存在於 `02_specs/schema/flags.registry.json` 中。
* **權限隔離**：若在 `03_data` 中偵測到 `var.*` 家族指令，校驗應直接判定為 **FAIL**（防止內容層干涉引擎底層變數）。

---

## 4. 核心解析行為矩陣 (Ref: DSL-8)

定義解析引擎 (Parser) 在處理 DSL 時的原子行為：

1.  **Strict Tokenize**：解析器僅接受 `category.action` 格式，不支持多段式（如 `a.b.c`）除非有特殊定義。
2.  **Type Enforcement**：`add_int` 僅接受 Integer；`set` 接受 Boolean。
3.  **No-Side-Effect Validation**：靜態掃描時不得修改 `game_state`，僅進行格式與標記合法性比對。

---

## 5. 治理缺口與風險提示

* **DSL-6 手動更新風險**：由於禁止自動掃描與實作，`flag.int_add` 向 `flag.add_int` 的遷移需依賴人工逐一校對 `03_data` 目錄，存在漏改風險。
* **區域偏移**：目前 `current_location` 已在 Save 系統中實現持久化，但 DSL 尚未支援「強制傳送 (location.teleport)」，建議在 Phase D.4 評估是否納入。

---
