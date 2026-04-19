# Governance Write Permission Matrix

## 1. Purpose

本文件定義專案中各角色（AI / Tool / Project）對不同層級檔案的「寫入權限」，  
確保：

- 避免規則被實作層污染（Rule Contamination）
- 維持 SSOT 一致性
- 建立明確的責任與升級流程（Escalation Flow）

---

## 2. System Roles

| Role | Description |
|------|------------|
| ChatGPT (Governance) | 規則制定者（DSL / Workflow / Structure / State） |
| ChatGPT (Production) | 實作執行者（Code / JSON / Debug） |
| Gemini | 任務橋接（JIRA 操作） |
| NotebookLM | SSOT 驗證（Drift Detection） |

---

## 3. Write Permission Matrix

| File / Layer | Governance | Production | Gemini | NotebookLM |
|--------------|-----------|------------|--------|------------|
| PROJECT_STATE.json | ✅ | ❌ | ❌ | ❌ |
| PROJECT_STATE_SNAPSHOT.md | ✅ | ❌ | ❌ | ❌ |
| AI_COLLAB_WORKFLOW.md | ✅ | ❌ | ❌ | ❌ |
| design_decision_log.md | ✅ | ❌ | ❌ | ❌ |
| PROJECT_STRUCTURE.md | ✅ | ❌ | ❌ | ❌ |
| 01_design_docs (DSL / Blueprint / Audit) | ✅ | ❌ | ❌ | ❌ |
| 02_specs (Schema) | ✅ | ⚠（需授權） | ❌ | ❌ |
| 03_data (Content JSON) | ❌ | ✅ | ❌ | ❌ |
| 05_engine (Python) | ❌ | ✅ | ❌ | ❌ |
| JIRA Tasks | ❌ | ❌ | ✅ | ❌ |

---

## 4. Enforcement Rules (Hard Constraints)

### 4.1 Governance Authority

- 所有以下檔案為 **Governance SSOT**：
  - PROJECT_STATE.json
  - AI_COLLAB_WORKFLOW.md
  - design_decision_log.md
  - PROJECT_STRUCTURE.md

👉 僅允許 Governance 修改

---

### 4.2 Production Restrictions

Production 不得：

- 修改任何 DSL / Schema / Workflow / Structure
- 修改 PROJECT_STATE.json
- 修改 design_decision_log.md

👉 違反視為 **Boundary Violation**

---

### 4.3 Gemini Restrictions

Gemini 僅允許：

- 建立 / 更新 JIRA 任務
- 撰寫簡短任務紀錄

不得：

- 修改任何專案檔案
- 解釋 DSL / Schema

---

### 4.4 NotebookLM Restrictions

NotebookLM 僅允許：

- 檢查 SSOT 一致性
- 判斷 drift

不得：

- 修改任何檔案
- 產出設計或任務

---

## 5. Escalation Flow（升級流程）

當 Production 發現問題時：

Production（問題）
↓
Governance（判斷）
↓
Decision（是否修改）
↓
更新：
  - DD（必要時）
  - STATE / WORKFLOW / STRUCTURE
↓
重新下發任務給 Production

---

## 6. Authorized Exception（唯一例外）

Production 僅在以下條件下可修改 Governance 層：

* 明確收到 Governance 指令
* 指令包含：

  * 修改內容
  * 修改範圍
  * 修改原因

範例：

[Governance Instruction]
Update PROJECT_STATE.json:
- add governance_extensions.dsl_governance

👉 Production 僅執行，不得自行決策

---

## 7. Violation Classification

| Type               | Description                 |
| ------------------ | --------------------------- |
| Naming Drift       | 使用非 canonical DSL           |
| Boundary Violation | Production 修改 Governance 檔案 |
| Context Leakage    | 任務 / 設計混用                   |
| SSOT Drift         | STATE / SNAPSHOT 不一致        |

---

## 8. Core Principle

> ❗Rules are written ONLY by Governance
> ❗Execution is performed ONLY by Production

---

## 9. Relationship to Other Documents

* PROJECT_STATE.json → State SSOT
* PROJECT_STRUCTURE.md → Structure SSOT
* design_decision_log.md → Evolution History
* AI_COLLAB_WORKFLOW.md → AI Behavior Rules

本文件負責：

👉 **誰可以修改這些 SSOT**

---
