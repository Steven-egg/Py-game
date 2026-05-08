# Design Decision Log


# DD-020

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

# 📄 DD-024 – Registry Metadata Governance Contract

## Status

Accepted

## Date

2026-05-01

## Impact

High

## Scope

* 02_specs/schema（registry metadata contract）
* 03_data/registries（metadata 使用限制）
* Validation Layer（metadata interpretation）
* Governance Layer（authority boundary definition）

---

## Reason

在 Phase D.4（Registry Schema Evolution）中，

* registry 已納入 schema contract（DD-023）
* 並允許包含 metadata / coverage 標記

但 REG-004 Audit 發現：

1. registry metadata 雖為合法存在，但缺乏分類與語義定義
2. metadata 與 DSL / validation / runtime 的權限邊界未明確
3. coverage_gate 等欄位具有潛在 authority 誤用風險
4. passive annotation 與 decision source 未被制度性區分

上述問題本質為：

> **metadata 已存在，但尚未形成可治理的 contract**

需建立統一規則，以防止 metadata 從描述性資訊漂移為決策來源（authority drift）。

---

## Decision

建立 **Registry Metadata Governance Contract**，定義 metadata 的：

* 類型（Type Classification）
* 使用邊界（Authority Boundary）
* 合法用途（Allow List）
* 違規觸發條件（Violation Trigger）

---

### 1. Metadata 定位（強制）

Registry metadata 定義為：

> **Passive Descriptive Annotation（被動描述性註記）**

---

### 2. Metadata 分類（強制）

所有 metadata 必須屬於以下三類：

#### (A) Descriptive Metadata

用途：說明語義或來源
範例：`reason`, `source_layer`

---

#### (B) Classification Metadata

用途：分類與分群
範例：`domain`, `status`

---

#### (C) Validation Annotation

用途：記錄驗證狀態（非權威）
範例：`coverage_gate`

---

#### 禁止類型

不得存在：

* Execution metadata（影響 runtime）
* Decision metadata（影響 DSL / validation 判定）

---

### 3. Authority Boundary（強制）

Registry metadata 不得用於：

---

#### ❌ DSL Authority

* 定義 DSL
* 修改 canonical naming

👉 DSL authority 僅來自 schema（DD-020）

---

#### ❌ Behavior Coverage 判定

* 不得用於判定 effect 是否可用
* 不得作為 Behavior Gate

👉 coverage authority 來自 validation / engine

---

#### ❌ Runtime Input

* 不得進入 engine
* 不得影響 dispatch / condition

---

#### ❌ Content Decision

* 不得影響 content_manifest
* 不得作為內容生成或驗證依據

---

### 4. Allow List（唯一允許用途）

Registry metadata 僅允許：

* Documentation（說明 / trace）
* Tooling（filter / display / visualization）
* Debug / Audit context（非決策）

---

### 5. Violation Trigger（違規觸發條件）

以下情況視為 Boundary Violation：

1. metadata 被用於 DSL 可用性判定
2. coverage_gate 被用於 behavior gate
3. metadata 被 runtime 使用
4. metadata 影響 content / validation decision

---

### 6. Schema Contract Extension（落地）

registry.schema.json 必須支援 metadata 結構：

* metadata 類型標記（descriptive / classification / validation_annotation）
* status enum（allowed / deprecated / experimental）
* coverage_gate 僅作為 annotation（非 gate）

---

### 7. Validation Rule（強制）

Validation layer 必須：

* 忽略 metadata 對決策的影響
* 不使用 metadata 作為 gate
* 僅驗證其結構合法性

---

## Result

建立 metadata 的治理閉環：

1. **Definition**：metadata 為描述層（非決策層）
2. **Classification**：三種類型強制分類
3. **Constraint**：禁止 authority 使用
4. **Validation**：metadata 僅結構驗證
5. **Enforcement**：違規使用即升級為 Boundary Violation

確保：

* metadata 不會影響 DSL / engine / validation 決策
* registry 可安全承載 annotation
* 防止 passive → authority drift

---

## Constraints

* 不修改既有 DSL contract（DD-020）
* 不修改 registry core role（DD-023）
* 不改變 AI Workflow 分層（DD-021）
* 不引入 runtime 行為

所有 metadata 若需升級為決策來源：

> **必須透過 DD + Evolution Mode**

---

## Version Anchor

* Spec Version: **1.4.0**
* Engine Version: **1.0.0**
* Structure Version: **1.2.0（unchanged）**
* Phase: **D.4 – Registry Schema Evolution**

---

## Conclusion

DD-024 將 registry metadata 從：

> **允許存在的描述資訊**

正式提升為：

> **受分類、邊界與驗證約束的治理物件**

並建立：

* passive annotation 與 authority 的明確分界
* metadata 的可控使用範圍
* 違規升級機制（Violation Trigger）

確保 registry 在 D.4 階段：

> **維持 mapping layer 定位，不演變為決策層**

---
