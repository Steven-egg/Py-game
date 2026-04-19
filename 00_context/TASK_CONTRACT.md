# Task Contract (Governance → Production → Gemini)

## 1. Purpose

本文件定義專案中「任務如何被建立、傳遞、執行與追蹤」的標準格式，  
確保以下目標：

- 防止 Governance / Production / JIRA 語境混用
- 建立可追溯的任務來源與決策鏈
- 確保 Gemini 僅接收可執行任務，而非設計規則本體
- 讓 Production 僅執行已批准之內容，不自行擴張規則

---

## 2. Core Principle

> Governance defines  
> Production implements  
> Gemini tracks  
> NotebookLM validates

---

## 3. Role Responsibility

### 3.1 Governance
負責：
- 定義任務
- 指定邊界
- 指定輸入 / 輸出
- 指定驗證條件
- 判斷是否需升級為 DD / State / Structure change

不得：
- 直接把未定義的模糊需求丟給 Gemini
- 讓 Production 自行解釋治理意圖

---

### 3.2 Production
負責：
- 根據已定義任務執行 code / JSON / patch / debug
- 回報實作問題、阻塞點、風險與驗證結果

不得：
- 自行修改治理規則
- 自行擴張任務範圍
- 直接將設計問題當作已批准規格落地

---

### 3.3 Gemini
負責：
- 將已拆解任務轉成 JIRA 卡片 / comment / status update
- 維護任務狀態與簡短進度紀錄

不得：
- 解釋 DSL / Schema / SSOT
- 產出設計決策
- 承載長篇治理文件

---

## 4. Standard Flow

Governance
↓
Task Definition
↓
Production Execution
↓
Execution Result / Blocker
↓
Gemini (JIRA Tracking)
↓
NotebookLM Validation (if required)
↓
Back to Governance


---

## 5. Governance → Production Task Contract

每一個正式任務都應至少包含以下欄位：

### 5.1 Required Fields

| Field           | Description                                          |
| --------------- | ---------------------------------------------------- |
| Task ID         | 任務唯一識別碼                                              |
| Title           | 任務名稱                                                 |
| Source          | 任務來源（DD / STATE / Blueprint / Audit / User Decision） |
| Objective       | 任務目標                                                 |
| Scope           | 本次允許修改的範圍                                            |
| Non-Scope       | 明確禁止修改的範圍                                            |
| Inputs          | Production 需要讀取的檔案                                   |
| Outputs         | 預期產出                                                 |
| Validation      | 驗證方式                                                 |
| Escalation Rule | 何種情況必須回 Governance                                   |
| JIRA Mode       | 是否需要 Gemini 建立 JIRA 任務                               |

---

### 5.2 Standard Template

## Task Definition

### Task ID
TASK-XXXX

### Title
<short task title>

### Source
- DD-XXX / PROJECT_STATE / Blueprint / Audit / Governance decision

### Objective
- Clearly state what must be achieved

### Scope
- Files / folders / modules allowed to change
- Exact boundaries of this task

### Non-Scope
- What must NOT be changed
- Explicit forbidden areas

### Inputs
- 00_context/...
- 02_specs/...
- 03_data/...
- 05_engine/...

### Outputs
- Expected files / patches / reports / comments

### Validation
- How completion is verified
- CLI / MVL / schema / manual inspection / regression

### Escalation Rule
Return to Governance if:
- schema contract mismatch found
- boundary conflict found
- DD required
- task ambiguity cannot be resolved within existing rules

### JIRA Mode
- Required / Optional / No


---

## 6. Production → Governance Return Contract

當 Production 無法直接完成任務時，必須使用以下格式回報，不得自行決策。

### Standard Template

## Production Return

### Task ID
TASK-XXXX

### Execution Status
- Completed / Blocked / Partial

### What Was Done
- concise implementation summary

### Blocker
- exact issue encountered

### Boundary Risk
- whether this issue touches DSL / Schema / State / Structure

### Recommendation
- what Governance should decide next

### Evidence
- file path / log / validation output / example payload

---

## 7. Governance → Gemini Task Bridge Contract

只有 Governance 能把任務下發給 Gemini。
Gemini 接收到的內容必須是「任務摘要」，不能是治理全文。

### Standard Template

## JIRA Bridge Payload

### Task Title
<short action-oriented title>

### Task Type
- Epic / Task / Subtask / Comment

### Summary
- short implementation-oriented description

### Acceptance Criteria
- bullet list of verifiable completion conditions

### Constraints
- concise boundaries for execution

### Deliverables
- file / patch / validation / report

### Notes
- optional short note

---

## 8. What MUST NOT be sent to Gemini

以下內容不得直接丟給 Gemini 作為 JIRA 輸入：

* DD 全文
* PROJECT_STATE.json 全文
* AI_BOOTSTRAP 全文
* 長篇 DSL 規則解釋
* Schema 詳細討論
* Governance audit 全文

Gemini 只接收：

* 已裁切完成之任務摘要
* 可執行的 acceptance criteria
* 簡短狀態更新

---

## 9. Task Classification

| Type            | Owner      | Description                                  |
| --------------- | ---------- | -------------------------------------------- |
| Governance Task | Governance | DD / State / Structure / Workflow 更新         |
| Production Task | Production | Code / JSON / runtime / validation execution |
| JIRA Task       | Gemini     | 任務建檔 / 狀態追蹤 / comment                        |
| Validation Task | NotebookLM | Drift check / SSOT alignment                 |

---

## 10. Escalation Triggers

以下情況不得由 Production 或 Gemini 自行處理，必須回 Governance：

* 需要修改 PROJECT_STATE.json
* 需要修改 design_decision_log.md
* 需要修改 PROJECT_STRUCTURE.md
* 發現 DSL canonical naming 衝突
* 發現 schema / engine contract mismatch
* 任務範圍超出原定義
* JIRA 任務內容涉及設計規則本體

---

## 11. Minimal Example

### Governance → Production

## Task Definition

### Task ID
TASK-D4-001

### Title
Audit effect registry naming alignment

### Source
- DD-020
- Phase D.4 Evolution Blueprint

### Objective
- verify engine-side effect names and registry naming against canonical schema naming

### Scope
- 02_specs
- 01_design_docs/audit_reports
- read-only inspection of 05_engine dispatcher

### Non-Scope
- no engine patch
- no schema modification
- no state update

### Inputs
- 00_context/PROJECT_STATE.json
- 00_project_management/design_decision_log.md
- 01_design_docs/audit_reports/DSL-7_Effect_Mapping_Logic.md
- 05_engine/effect_executor.py

### Outputs
- audit note
- mismatch list
- recommendation summary

### Validation
- manual audit
- naming comparison matrix

### Escalation Rule
Return to Governance if:
- contract mismatch requires DD
- canonical naming conflict confirmed

### JIRA Mode
- Optional

---

### Governance → Gemini

## JIRA Bridge Payload

### Task Title
Audit effect registry naming alignment

### Task Type
Task

### Summary
Review effect naming alignment between schema canonical names and engine dispatcher implementation.

### Acceptance Criteria
- mismatch list completed
- affected files identified
- recommendation summary documented

### Constraints
- no engine modification
- no schema modification

### Deliverables
- audit note
- mismatch summary

---

## 12. Final Rule

> No task may cross Governance / Production / Gemini boundaries without explicit contract.

