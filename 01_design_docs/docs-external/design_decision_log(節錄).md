# Design Decision Log


## DD-020

Date: 2026-04-15
Title: Effect DSL Governance Charter（Naming / Boundary / Coverage 統一治理）

Impact: High
Scope: 02_specs（contract interpretation）、03_data（authoring constraint）、05_engine（behavior alignment policy）

---

### Reason

於 Phase D.2 regression 收斂過程中，發現 Effect DSL 存在三類跨層不一致問題：

1. **Naming Drift**

   * Schema 使用 `flag.add_int`
   * Engine（DD-016）使用 `flag.int_add`

2. **Contract Boundary Violation**

   * Engine 支援 `var.add`
   * Schema 未定義，content 使用將被 schema gate 阻擋 

3. **Coverage Gap**

   * 多數 effect 僅存在於 schema enum，未經 engine 行為驗證（如 `flag.unset`, `stat.modify`, `quest.*` 等）

上述問題本質為：

> **Schema（contract）、Engine（capability）、Content（usage）三層脫節**

需建立統一治理原則，以避免 DSL 長期漂移與不可預測行為。

---

### Decision

建立 **Effect DSL Governance Charter**，包含三項強制性治理規則：

---

#### 1. Canonical Naming（命名權威）

* `flag.add_int` 為唯一 canonical DSL 名稱（schema authority）
* `flag.int_add` 為 non-canonical（engine-side naming）

**Enforcement:**

* 禁止 `03_data` 使用 `flag.int_add`
* 違反視為 **Naming Drift Violation**

---

#### 2. Contract Boundary（var.add 邊界封閉）

* `var.add` 定義為 **Engine-only Capability**
* 不屬於 schema contract，不得進入 content 層

**Enforcement:**

* `03_data` 出現 `var.add` → **Contract Violation**
* 專用 effect（如 `gold.add`）優先，不得以通用指令替代

---

#### 3. Coverage Validation（覆蓋驗證機制）

所有 effect 必須通過：

* Schema Coverage（規格合法）
* Behavior Coverage（engine 可執行）

**分類：**

* Fully Covered（雙通過）
* Schema Only（未驗證 engine）
* Not Covered（未驗證）

**Enforcement:**

* 未通過 Behavior Coverage 的 effect：

  * 不得標記為 Ready
  * 不得用於正式 content

---

### Result

建立 Effect DSL 的治理閉環：

1. **Definition**：Schema 為唯一 DSL contract
2. **Constraint**：Naming + Boundary 限制
3. **Validation**：Schema + Behavior 雙層驗證
4. **Enforcement**：Negative Enforcement（違規即攔截）
5. **Evolution**：未對齊項目遞延至 D.4

確保：

* DSL 命名單一來源（消除 drift）
* Content 不再誤用 engine capability
* DSL 可用性由測試覆蓋決定，而非存在性

---

### Deferred (Phase D.4 – Requires Evolution Mode)

以下項目明確遞延：

1. **Engine–Schema Naming Alignment**

   * `flag.int_add` → canonical 對齊

2. **`var.add` DSL 升格**

   * contract 定義（target / params）
   * 與 registry 綁定策略

3. **Registry–Schema 自動同步**

   * 建立 registry 驅動的 schema 注入機制

4. **Extended Effect Coverage**

   * `quest.*`, `battle.*`, `ui.*`, `scene.*` 等行為驗證

---

### Constraints

* 不修改 schema（Spec 1.3.0 維持不變）
* 不修改 engine dispatcher（DD-016 保持有效）
* 不改變專案結構（Structure 1.2.0 鎖定）

所有實質行為或 contract 變更：

> **This requires DD + Evolution Mode**

---

### Version Anchor

* Spec Version: **1.3.0**
* Engine Version: **1.0.0**
* Phase: **D.3 Evaluation → Governance Formalization**

---

### Conclusion

DD-020 將 Effect DSL 從「實作導向能力集合」提升為：

> **受 Schema、Coverage、Boundary 約束的正式語言系統**

並在不破壞現有 Lock 狀態下，完成：

* 命名權威確立
* 邊界封閉（技術債隔離）
* 覆蓋驗證制度建立
* 演進路徑（D.4）預埋


---


# DD-021 – AI Collaboration Workflow Governance

## Status
Accepted

## Date
2026-04-18

## Context

隨著專案進入 Phase D.4（Evolution Blueprint 準備階段），  
系統開發流程已同時涉及：

- DSL 設計（01_design_docs）
- 任務管理（JIRA）
- 實作（05_engine / 03_data）
- SSOT 驗證（NotebookLM）

在單一 AI 對話中同時處理上述層級，已觀察到以下問題：

1. Context Leakage（語境混用）  
   - JIRA 任務內容混入 DSL / Audit 規範  
   - AI 角色混淆（Spec Auditor vs Task Executor）

2. Boundary Violation（邊界破壞）  
   - JIRA 被用作設計文件承載  
   - Production 嘗試修改 DSL / Schema

3. Traceability Degradation（可追溯性下降）  
   - 任務紀錄無法區分「執行」與「設計決策」

為確保系統維持 SSOT、一致性與可演進性，需建立正式之 AI 協作治理機制。

---

## Decision

採用「AI Collaboration Workflow」作為專案之正式治理規則，並定義如下分工與邊界：

### 1. Role Separation（角色分離）

#### ChatGPT（Governance）
- 負責 DSL / Blueprint / audit_reports / SOP
- 負責任務拆解（設計 → 任務）

#### ChatGPT（Production）
- 負責 code / JSON / Debug
- 不得主動修改 DSL / Schema

#### Gemini（JIRA Bridge）
- 負責 JIRA 操作與轉換（Task / Comment）
- 不得參與 DSL / Schema 設計

#### JIRA
- 僅作為任務追蹤系統
- 不得承載設計文件或 DSL 規範

#### NotebookLM
- 作為 SSOT Validator
- 檢查 DSL / Schema / Data 是否發生 Drift

---

### 2. Boundary Enforcement（邊界強制）

以下規則為強制：

- JIRA 不得存放：
  - DSL 規範
  - Gate 判讀
  - Schema 設計
- Production 不得修改 DSL / Schema
- Governance 不直接進行 runtime 實作
- NotebookLM 不以 JIRA 作為 SSOT 判斷依據

違反上述規則視為 **Context Drift / Boundary Violation**。

---

### 3. Workflow Definition（流程定義）

標準流程如下：


Governance（DSL / Blueprint）
↓
Task Decomposition
↓
JIRA（任務建立與追蹤）
↓
Production（實作）
↓
NotebookLM（SSOT 驗證）
↓
Feedback → Governance（必要時修正）


---

### 4. SSOT Alignment（單一真實來源）

SSOT 判斷優先順序：

1. 00_context（Governance 規則）
2. 01_design_docs（DSL / Audit）
3. 02_specs（Schema）
4. 03_data（內容）

JIRA 不屬於 SSOT。

---

### 5. Governance Artifact

本決策對應治理文件：

- `00_context/AI_COLLAB_WORKFLOW.md`

該文件作為：

- AI 協作規則定義
- 分層邊界控制依據
- Drift Prevention 規範

---

## Consequences

### Positive

- 明確隔離設計 / 任務 / 實作三層
- 降低 AI 語境污染（Context Leakage）
- 提升 JIRA 可讀性與可維護性
- 強化 SSOT 一致性與驗證能力

---

### Negative / Trade-offs

- 增加初期操作複雜度（多對話 / 多工具）
- 需要維持跨層溝通（Feedback Loop）

---

### Risk Mitigation

- 使用 NotebookLM 作為統一 SSOT Validator
- 透過 JIRA 僅追蹤任務，不承載設計
- Governance 層統一管理 DSL 與規範

---

## Notes

本決策不改變既有 DSL / Schema / Engine 設計，  
僅針對「AI 協作流程」與「任務治理模式」進行規範化。

本決策為 Phase D.4 啟動前之治理基礎，  
後續 Evolution Mode 啟動須遵循本規則執行。


---

好，這一步我直接幫你做到**可落地、可寫入、可執行**的正式版本。
以下內容你可以**直接貼進 `design_decision_log.md`**。

---

# 📄 DD-022 – Governance Layer Normalization & Structure Alignment

## Status

Accepted

## Date

2026-04-20

## Impact

High

## Scope

* 00_context（Governance Layer）
* 03_data（Structure Extension – registries）
* GOVERNANCE_INDEX.md（Navigation Alignment）

---

## 1. Context（背景）

在 Phase D.3 完成後，專案進入 D.4 準備階段，
透過 NotebookLM Drift Audit 發現以下問題：

---

### 1.1 Naming Drift（命名不一致）

* `PROJECT_STATE.json` 採 Canonical Uppercase
* `Project_Context_v1_bootstrap.json` 採 mixed naming + version suffix
* `Project_Soul.json` 採 PascalCase

👉 導致：

* AI 難以辨識 authority file
* 增加跨對話 context drift 風險

---

### 1.2 Structure Drift（結構未對齊）

* `03_data/registries/` 已實際存在
* 但未被 `PROJECT_STRUCTURE.md` 定義

👉 屬於：


Structure SSOT 與實體結構不一致


---

### 1.3 Navigation 不一致（讀取層優化需求）

* Snapshot 已加入 `AI Quick Context`
* 但 GOVERNANCE_INDEX 尚未反映「快速初始化層」

👉 導致：

* INIT_SOP 與實際使用模式略有偏差

---

## 2. Decision（決策）

本 DD 定義三項治理演進：

---

## 2.1 Governance Naming Normalization（命名標準化）

### Decision

將 Governance Layer JSON 檔案統一為：


CANONICAL UPPERCASE + snake_case


---

### Rename Mapping


Project_Context_v1_bootstrap.json → PROJECT_CONTEXT.json
Project_Soul.json                → PROJECT_SOUL.json


---

### Rules

1. ❌ 禁止 version suffix（如 v1, v2）
2. ❌ 禁止 PascalCase / mixedCase
3. ✔ 統一使用：

   * `PROJECT_*`
   * `UPPERCASE_WITH_UNDERSCORE`

---

### Rationale

* 強化 AI 對「authority file」辨識
* 降低 naming drift
* 對齊 `PROJECT_STATE.json`

---

## 2.2 Structure Extension（registries 正式納入）

### Decision

正式將以下目錄納入 Structure SSOT：


03_data/
  registries/


---

### Definition


registries = cross-entity mapping / lookup layer


用途：

* DSL registry
* effect mapping
* future schema-driven injection

---

### Constraint

* 不改變既有 content contract
* 不影響 loader 行為
* 不影響 engine runtime

---

### Rationale

* registry 已在 Phase D.3 實際使用
* 屬於 Schema–Data 中介層
* 為 D.4（Registry–Schema Sync）預備

---

## 2.3 Navigation Layer Alignment（讀取層對齊）

### Decision

將以下概念正式納入治理：


AI Quick Context = Startup Layer


---

### Classification Update

| Layer               | Files                                       |
| ------------------- | ------------------------------------------- |
| Core Governance     | PROJECT_STATE.json / PROJECT_STRUCTURE.md   |
| Decision History    | design_decision_log.md                      |
| Navigation Layer    | GOVERNANCE_INDEX.md / AI_COLLAB_INIT_SOP.md |
| Startup Layer (NEW) | PROJECT_STATE_SNAPSHOT.md (Quick Context)   |

---

### Rule


Startup Layer = 快速初始化（非 authority）


---

### Rationale

* 對齊 INIT_SOP 的 minimal startup strategy
* 降低 token 成本
* 提高 AI 初始化穩定性

---

## 3. Implementation（實作步驟）

---

### Step 1 – 檔名調整

git mv 00_context/Project_Context_v1_bootstrap.json 00_context/PROJECT_CONTEXT.json
git mv 00_context/Project_Soul.json 00_context/PROJECT_SOUL.json

---

### Step 2 – 更新 PROJECT_STRUCTURE.md

新增：

03_data/
  registries/

---

### Step 3 – 更新 GOVERNANCE_INDEX.md

新增：

Startup Layer:
- PROJECT_STATE_SNAPSHOT.md (AI Quick Context)

---

### Step 4 – 更新 PROJECT_STATE.json

在 `notes` 或 `governance_extensions` 補：

"DD-022 established: Governance Naming + Structure Alignment + Startup Layer introduction"

---

### Step 5 – Drift Audit（驗證）

使用 NotebookLM 檢查：

* structure alignment
* naming consistency
* SSOT integrity

---

## 4. Constraints（限制）

* ❌ 不修改 schema（Spec 1.3.0 保持）
* ❌ 不修改 engine
* ❌ 不修改 content JSON
* ❌ 不改變 workflow（DD-021）

---

## 5. Consequences（影響）

---

### Positive

* 消除 naming drift
* 修復 structure SSOT 不一致
* 強化 AI 初始化穩定性
* 為 Phase D.4 建立基礎

---

### Trade-off

* 需要一次性檔名遷移（git history 變更）
* GOVERNANCE_INDEX 需同步維護

---

## 6. Final State（完成後狀態）

✔ Naming fully canonical
✔ Structure fully aligned
✔ Startup layer established
✔ Ready for Phase D.4

### Approval

Approved by: Governance (User)
Effective Date: 2026-04-20

---

# 📄 DD-023 – Registry Schema Introduction (Contractization Decision)

## Status

Accepted

## Date

2026-04-22

## Impact

High

## Scope

* 02_specs/schema（新增 registry schema）
* 03_data/registries（正式 contract 對齊）
* DSL Governance（DD-020）
* Validation Layer（MVL extension）

---

## 1. Context（背景）

在 Phase D.3 完成後，系統已建立：

* DSL Governance（DD-020）
* AI Workflow Governance（DD-021）
* Structure Alignment（DD-022）

並完成：

> Registry Schema Spec（Design Layer）

該設計已明確：

* registry 為 **cross-entity mapping layer**
* 僅負責 **canonical naming alignment / governance annotation**
* 不涉及 DSL 定義 / runtime 行為

---

## 2. Decision（最終決策）

選擇：

> ✅ **Option A – Adopt**

---

## 3. Contract Introduction

正式決定：

### 3.1 新增 Schema Contract

在以下位置新增：

02_specs/schema/registry.schema.json

---

### 3.2 Registry 定位（固定）

Registry 被正式定義為：

> **Schema-aligned mapping layer（非語義層 / 非執行層）**

---

### 3.3 DSL Governance 對齊（強制）

* ❌ registry 不得定義 DSL
* ❌ registry 不得成為 naming authority
* ✔ schema（02_specs）仍為唯一 DSL contract

---

### 3.4 Coverage Role（限制）

registry：

* ✔ 可標記 coverage 狀態
* ❌ 不得決定可用性（仍由 schema + behavior 決定）

---

## 4. 🔴 Evolution Mode 啟動（強制）

Entering Evolution Mode (Spec Version 1.3.0 → 1.4.0)

---

## 5. Evolution Scope（演進範圍）

本次演進僅包含：

### ✔ Schema 層

* 新增 `registry.schema.json`

---

### ✔ Contract 層

* registry 正式納入 schema contract
* 可被 validation pipeline 使用

---

### ❌ 不包含

* 不修改既有 schema（effect / condition / quest 等）
* 不修改 engine
* 不修改 content JSON

---

## 6. Constraints（限制）

---

### DSL（DD-020）

* canonical naming → schema authority
* flag.int_add → forbidden
* var.add → engine-only（禁止進 content）
* 必須通過 schema + behavior coverage

---

### Structure（DD-004 / DD-022）

* schema 僅能存在於 `02_specs/schema`
* registry 僅存在於 `03_data/registries`
* 不得新增其他結構

---

### Workflow（DD-021）

* Governance 不實作 runtime
* Production 不得修改 DSL / schema 定義
* JIRA 不得承載 schema / DSL

---

## 7. Implementation Plan（高層）

（仍屬 Governance 指導，不是實作）

### Step 1

定義 `registry.schema.json`（依 Registry Schema Spec）

### Step 2

建立最小 registry fixture（測試用）

### Step 3

擴充 MVL validation：

* registry schema validation
* 基本結構驗證

---

## 8. Consequences（影響）

### Positive

* ✔ DSL 對齊集中化
* ✔ registry 可進入 validation pipeline
* ✔ D.4「registry–schema sync」正式落地

---

### Trade-off

* ⚠️ 增加 schema complexity
* ⚠️ 增加 validation 維護成本

---

## 9. Version Anchor

* Previous Spec Version: **1.3.0**
* New Spec Version: **1.4.0**
* Structure Version: **1.2.0（unchanged）**
* Engine Version: **1.0.0（unchanged）**

---

## 10. Final State

✔ registry 成為 schema contract 一部分
✔ Evolution Mode 已啟動
✔ 可進入 Production Schema 實作階段

---

## Approval

* Approved by: Governance (User)
* Effective Date: 2026-04-22

---
