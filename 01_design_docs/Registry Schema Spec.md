# 📄 Registry Schema Spec（Design Layer）

## 1. Purpose（目的）

本文件定義 **Registry 的結構設計規格（Schema Blueprint）**，用於：

* 支援 **DSL 命名對齊（canonical alignment）**
* 提供 **Schema–Data 映射層（mapping layer）**
* 為 Phase D.4 的 **Registry–Schema 同步機制**建立設計基礎

---

## 2. Scope（範圍）

### In Scope

* Registry 作為 **cross-entity mapping layer**
* canonical naming 對齊資料結構
* DSL / schema 對齊輔助資訊
* governance metadata（狀態 / 限制 /來源）

---

### Out of Scope（強制）

* ❌ 不定義 DSL（由 schema 負責）
* ❌ 不定義 effect / condition 行為
* ❌ 不包含 runtime 規則
* ❌ 不涉及 engine 使用方式
* ❌ 不修改既有 schema（Spec 1.3.0）

---

## 3. Layer Position（分層定位）

| Layer              | Responsibility               |
| ------------------ | ---------------------------- |
| 02_specs/schema    | DSL contract（唯一命名權威）         |
| 03_data/registries | Registry data（mapping layer） |
| 05_engine          | runtime 消費（不在本文件範圍）          |

---

## 4. Core Design Principle（核心原則）

### 4.1 Canonical Authority

* DSL 命名權威 **永遠在 schema**
* registry **不得創造或修改 canonical naming**

---

### 4.2 Mapping-only Layer

Registry 僅能：

* 對齊（alignment）
* 映射（mapping）
* 標記（annotation）

不得：

* 定義語義
* 定義邏輯

---

### 4.3 Governance-driven

所有欄位設計必須可對應：

* DD-020（DSL Governance）
* DD-021（Workflow Boundary）
* DD-004 / DD-022（Structure）

---

## 5. Proposed Schema Fields（設計欄位）

> ⚠️ 以下全部為 **proposed schema fields（尚未存在）**

---

### 5.1 Top-level Structure

* `registry_type`
* `registry_version`
* `entries`

---

### 5.2 Entry Structure

每個 entry：

* `id`
* `canonical_name`
* `domain`

---

### 5.3 Governance Metadata

* `status`

  * allowed / blocked / reserved

* `reason`

  * non-canonical
  * engine-only
  * uncovered

* `authority`

  * 對應 schema 或 governance rule（例：DD-020）

* `notes`

  * 說明用途（非邏輯）

---

### 5.4 Optional Mapping Fields

* `aliases`

  * 非 canonical 名稱對照（不可用）

* `replaced_by`

  * canonical 替代項

* `coverage_gate`

  * 標記是否通過使用門檻（僅標記，不決策）

---

## 6. Field Semantics（欄位語意）

| Field          | 語意                       |
| -------------- | ------------------------ |
| canonical_name | schema 定義的唯一合法名稱         |
| aliases        | 歷史或錯誤命名（禁止使用）            |
| status         | 是否允許進入 content           |
| reason         | 被限制原因（對應 DSL governance） |
| authority      | 規則來源（schema / DD）        |
| coverage_gate  | coverage 狀態標記（非執行）       |

---

## 7. Constraint Mapping（對應治理規則）

### 對應 DD-020（DSL Governance）

* canonical_name → schema authority
* aliases → naming drift 封存
* status / reason → boundary enforcement
* coverage_gate → coverage visibility（非 enforcement）

---

### 對應 DD-021（Workflow）

* registry 不得：

  * 被 JIRA 使用為設計來源
  * 被 Production 修改為 DSL 定義
* 僅屬 Governance 設計輸出

---

### 對應 DD-004 / DD-022（Structure）

* registry 僅存在於：

  * `03_data/registries/`
* schema 僅存在於：

  * `02_specs/schema/`

---

## 8. Non-Goals（明確排除）

以下能力**不屬於 registry**：

* ❌ effect dispatcher 行為
* ❌ condition evaluation
* ❌ runtime gating（location / quest 等）
* ❌ DSL contract 定義
* ❌ schema validation 規則

---

## 9. Evolution Boundary（演進邊界）

以下變更 **Requires DD + Evolution Mode**：

* registry 成為 DSL 命名權威
* registry 決定 coverage 可用性
* registry 驅動 schema 自動生成
* registry 參與 runtime 決策

---

## 10. Readiness for Next Phase（D.4）

本設計完成後，可進入：

### D.4-2（需 DD 判定）

* registry.schema.json 定義（02_specs）
* registry–schema contract 建立
* coverage integration（如需要）

---

## 11. Summary（一句話）

> Registry 是「Schema 的對齊與治理輔助層」，而不是 DSL 或 Runtime 的來源。

---

（End of Document）
