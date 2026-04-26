# GOVERNANCE_INDEX.md

## 1. Purpose

本文件為本專案 Governance Layer 的總索引（Index）與建議閱讀順序（Reading Order），  
用於協助：

- 新對話初始化
- Governance / Production / Gemini / NotebookLM 快速對齊
- 降低 AI 語境污染
- 明確區分「先讀什麼」與「有需要再讀什麼」

本文件不取代任何 SSOT，僅作為 **Governance Navigation Layer** 使用。

---

## 2. Core Principle

> Read the minimum set first.  
> Escalate to full SSOT only when authority is required.

---

## 3. Governance Document Map

| File | Role | Purpose | Authority Level |
|------|------|---------|-----------------|
| `PROJECT_STRUCTURE.md` | Structure SSOT | 定義專案分層與結構邊界 | High |
| `PROJECT_STATE.json` | State SSOT | 定義當前版本、狀態、能力與治理映射 | High |
| `PROJECT_STATE_SNAPSHOT.md` | State Mirror | 提供人類 / AI 可讀狀態快照 | Medium |
| `AI_BOOTSTRAP.md` / `AI_BOOTSTRAP(節錄).md` | Bootstrap Entry | 提供初始化快照與硬性限制 | High / Medium |
| `design_decision_log.md` / `design_decision_log(節錄).md` | Decision History | 定義正式治理決策與演進脈絡 | High / Medium |
| `AI_COLLAB_WORKFLOW.md` | Workflow Rule | 定義 AI 協作角色與流程 | High |
| `GOVERNANCE_WRITE_MATRIX.md` | Write Authority | 定義誰可以修改哪些檔案 | High |
| `TASK_CONTRACT.md` | Task Flow Contract | 定義 Governance → Production → Gemini 任務格式 | High |
| `GEMINI_JIRA_PROMPT_STANDARD.md` | JIRA Prompt Standard | 定義 Gemini 任務橋接格式 | High |
| `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md` | Drift Validation Standard | 定義 NotebookLM Drift 檢查 Prompt | High |
| `AI_COLLAB_INIT_SOP.md` | Init SOP | 定義各 AI 角色新對話初始化檔案清單與策略 | High |

---

## Startup Layer (Token Optimized)

Purpose:
- Provide fast AI initialization context
- Reduce token usage during new conversations
- Avoid overloading Governance context

Primary File:
- PROJECT_STATE_SNAPSHOT.md

Characteristics:
- Contains AI Quick Context (startup summary)
- Human-readable mirror of PROJECT_STATE.json
- NOT a Source of Truth

Usage Rule:
- Use for initial orientation only
- Always resolve authority via:
  - PROJECT_STATE.json (State SSOT)
  - PROJECT_STRUCTURE.md (Structure SSOT)

---

## 4. Reading Order by Scenario

---

## 4.1 Universal Entry Order（所有新對話通用）

所有 AI / 新對話，建議優先依以下順序讀取：

1. `PROJECT_STRUCTURE.md`
2. `PROJECT_STATE_SNAPSHOT.md`
3. `AI_BOOTSTRAP(節錄).md`
4. `design_decision_log(節錄).md`

目的：
- 先掌握結構
- 再掌握狀態
- 再建立近期治理語境
- 最後確認當前硬性限制

---

## 4.2 Governance Reading Order

適用於：
- ChatGPT（Governance）
- 治理決策討論
- DD / State / Workflow / Structure 調整前

### Minimal Set
1. `PROJECT_STRUCTURE.md`
2. `PROJECT_STATE_SNAPSHOT.md`
3. `AI_BOOTSTRAP(節錄).md`
4. `design_decision_log(節錄).md`
5. `AI_COLLAB_WORKFLOW.md`
6. `GOVERNANCE_WRITE_MATRIX.md`

### Extended Set
若本次涉及正式決策或 authority 判定，追加讀取：
7. `PROJECT_STATE.json`
8. `design_decision_log.md`
9. `AI_BOOTSTRAP.md`
10. `AI_COLLAB_INIT_SOP.md`

---

## 4.3 Production Reading Order

適用於：
- ChatGPT（Production）
- code / JSON / debug / patch 任務

### Minimal Set
1. `PROJECT_STATE_SNAPSHOT.md`
2. `TASK_CONTRACT.md`
3. 任務相關 `02_specs/*.schema.json`
4. 任務相關 `03_data/` or `05_engine/` 檔案

### Optional Reference
若任務涉及行為語意：
5. `Effect_DSL_Behavior_Logic.md`

### Escalation Rule
若任務中出現以下情況，停止自行推進並回 Governance：
- schema contract mismatch
- need to update state
- need to change structure
- DSL naming conflict
- unclear task boundary

---

## 4.4 Gemini Reading Order

適用於：
- JIRA 建立
- JIRA comment / progress update
- 任務橋接

### Minimal Set
1. `GEMINI_JIRA_PROMPT_STANDARD.md`
2. `TASK_CONTRACT.md` 第 7 節
3. Governance 提供的 bridge payload

### Forbidden
Gemini 不應讀取：
- `PROJECT_STATE.json`
- `design_decision_log.md`
- `AI_BOOTSTRAP.md`
- 長篇 DSL / Schema 解釋
- audit / governance 全文

---

## 4.5 NotebookLM Reading Order

適用於：
- Drift Audit
- SSOT consistency review
- 結構 / 任務 / Prompt 格式審查

### Minimal Set
1. `PROJECT_STRUCTURE.md`
2. `PROJECT_STATE.json`
3. `GOVERNANCE_WRITE_MATRIX.md`
4. `AI_COLLAB_WORKFLOW.md`
5. `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md`

### Extended Set
若涉及最近治理決策或任務流：
6. `design_decision_log(節錄).md`
7. `TASK_CONTRACT.md`
8. `GEMINI_JIRA_PROMPT_STANDARD.md`
9. `AI_COLLAB_INIT_SOP.md`

---

## 5. Authority Priority

當多份文件同時出現時，請依以下權威順序判定：

### 5.1 Structure
1. `PROJECT_STRUCTURE.md`

### 5.2 State
1. `PROJECT_STATE.json`
2. `PROJECT_STATE_SNAPSHOT.md`（mirror only）

### 5.3 Governance Decision
1. `design_decision_log.md`
2. `design_decision_log(節錄).md`（orientation only）

### 5.4 Workflow / SOP
1. `AI_COLLAB_WORKFLOW.md`
2. `TASK_CONTRACT.md`
3. `GEMINI_JIRA_PROMPT_STANDARD.md`
4. `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md`
5. `AI_COLLAB_INIT_SOP.md`

### 5.5 Bootstrap
1. `AI_BOOTSTRAP.md`
2. `AI_BOOTSTRAP(節錄).md`

---

## 6. Excerpt Usage Strategy

### 6.1 Purpose of Excerpts
節錄版文件只用於：
- 快速初始化
- Token 優化
- 建立近期治理語境

### 6.2 Excerpts are NOT for
節錄版文件不得作為以下事項的最終依據：
- authority decision
- structure change approval
- state truth validation
- DD formal interpretation
- final drift audit

### 6.3 Rule
> Excerpt = orientation  
> Full document = authority

---

## 7. Recommended Startup Kits

---

### 7.1 Governance Startup Kit
- `PROJECT_STRUCTURE.md`
- `PROJECT_STATE_SNAPSHOT.md`
- `AI_BOOTSTRAP(節錄).md`
- `design_decision_log(節錄).md`
- `AI_COLLAB_WORKFLOW.md`
- `GOVERNANCE_WRITE_MATRIX.md`

---

### 7.2 Production Startup Kit
- `PROJECT_STATE_SNAPSHOT.md`
- `TASK_CONTRACT.md`
- relevant schema
- relevant engine / data files

---

### 7.3 Gemini Startup Kit
- `GEMINI_JIRA_PROMPT_STANDARD.md`
- bridge payload from Governance

---

### 7.4 NotebookLM Startup Kit
- `PROJECT_STRUCTURE.md`
- `PROJECT_STATE.json`
- `GOVERNANCE_WRITE_MATRIX.md`
- `AI_COLLAB_WORKFLOW.md`
- `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md`

---

## 8. Governance Navigation Rules

### Rule 1
先讀結構，再讀狀態，再讀近期治理。

### Rule 2
沒有 Task Contract，不進入 Production。

### Rule 3
沒有 Bridge Payload，不進入 Gemini。

### Rule 4
NotebookLM 先做 validator，不做 designer。

### Rule 5
若問題涉及 authority，必須回完整 SSOT。

---

## 9. Suggested Maintenance Rule

當新增治理文件時，應同步更新本索引中的：

- Governance Document Map
- Reading Order
- Startup Kit
- Authority Priority

避免索引失效。

---

## 10. Final Rule

> This file tells you what to read first.  
> It does not replace what those files actually mean.

---