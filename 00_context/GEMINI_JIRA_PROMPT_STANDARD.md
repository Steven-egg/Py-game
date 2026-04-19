# Gemini JIRA Prompt Standard

## 1. Purpose

本文件定義「提供給 Gemini 的標準 Prompt 格式」，  
確保：

- JIRA 任務可直接使用（不需再解釋）
- 避免 DSL / Schema 污染 JIRA
- 任務具備可驗證性（Acceptance Criteria）
- 完全符合 TASK_CONTRACT.md 規範

---

## 2. Core Rule

> Gemini is a task formatter, NOT a system designer.

---

## 3. Required Structure（強制欄位）

每個提供給 Gemini 的 Prompt 必須包含以下結構：

---

## 🧾 JIRA Prompt

```md
### Task Title
<動作導向標題，例如：Audit effect naming alignment>

### Task Type
- Epic / Task / Subtask

### Summary
<精簡描述（實作導向）>
❗不得包含 DSL 設計理念或長篇背景說明

---

### Acceptance Criteria
- [ ] 條件1（可驗證）
- [ ] 條件2（可驗證）
- [ ] 條件3（可驗證）

---

### Constraints（強制限制）
- 不得修改 Schema（02_specs）
- 不得修改 DSL 規則
- 不得修改 PROJECT_STATE.json
- 僅限於指定 Scope 內操作

---

### Forbidden Content（禁止事項）
- ❌ 不得解釋 DSL 規則
- ❌ 不得解釋 Schema 結構
- ❌ 不得產出設計決策
- ❌ 不得輸出長篇治理文件

---

### Deliverables
- <明確輸出，例如：audit report / patch / file list>

---

### Notes（可選）
- <簡短補充（不得超過3行）>
````

---

## 4. Enforcement Rules（內建 NotebookLM 建議）

以下條件為強制：

### ✔ 必須存在

* Task Title
* Task Type
* Summary（實作導向）
* Acceptance Criteria（條列式）
* Constraints（限制）
* Forbidden Content（負向約束）

---

### ❌ 禁止出現

* DSL 設計說明
* Schema 詳細描述
* DD 全文
* PROJECT_STATE.json 內容
* 長篇分析或 reasoning

---

## 5. Good vs Bad Example

---

### ✅ Good Prompt（正確）

```md
### Task Title
Audit effect dispatcher naming consistency

### Task Type
Task

### Summary
Verify that engine-side effect names match canonical schema naming.

### Acceptance Criteria
- [ ] 所有 effect 名稱與 schema 對齊
- [ ] mismatch 清單產出
- [ ] 影響檔案列出

### Constraints
- 不得修改 Schema
- 不得修改 DSL
- 僅檢查 engine dispatcher

### Forbidden Content
- ❌ 不得解釋 DSL
- ❌ 不得分析 Schema 設計

### Deliverables
- mismatch list
- audit summary
```

---

### ❌ Bad Prompt（錯誤）

```md
請分析目前 DSL 設計是否合理，並說明 flag.add_int 與 flag.int_add 的差異...
```

❌ 問題：

* 混入設計討論
* 無 Acceptance Criteria
* 無限制條件
* Gemini 會亂發揮

---

## 6. Mapping to TASK_CONTRACT

| TASK_CONTRACT | Gemini Prompt                |
| ------------- | ---------------------------- |
| Title         | Task Title                   |
| Objective     | Summary                      |
| Validation    | Acceptance Criteria          |
| Non-Scope     | Constraints                  |
| Escalation    | 不出現在 Gemini（由 Governance 控制） |

---

## 7. Final Rule

> If a prompt cannot be directly executed as a JIRA task, it is INVALID.
