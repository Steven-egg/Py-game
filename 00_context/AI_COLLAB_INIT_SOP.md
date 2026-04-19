# AI_COLLAB_INIT_SOP.md

## 1. Purpose

本文件定義各 AI 角色於「新對話初始化」時所需的必要檔案清單與讀取策略，  
目的是在維持 SSOT 一致性的前提下，兼顧：

- Token 優化
- 對話彈性
- 邊界清晰
- Drift Prevention

本文件屬於 **DD-021 協作流程治理** 的具體 SOP。

---

## 2. Core Principle

> Give each AI only the files required for its role.  
> Do not over-share governance context into execution tools.

---

## 3. AI Role Initialization Matrix

| AI Role | Core Objective | Required Files | Forbidden / Not Recommended |
|------|------|------|------|
| ChatGPT (Governance) | 決策 / 任務下發 / 邊界控制 | State Snapshot、Structure、DD 節錄、Bootstrap 節錄、Workflow、Write Matrix | 不需預先給大量 engine/debug 細節 |
| ChatGPT (Production) | 程式 / JSON / Debug / Patch | State Snapshot、Task Contract、相關 Schema、行為邏輯文件 | 不應預載完整治理文件 |
| Gemini (JIRA Bridge) | 任務轉化 / 進度追蹤 | Gemini Prompt Standard、Task Contract 橋接格式 | 嚴禁給 DD 全文 / PROJECT_STATE.json / DSL 長文 |
| NotebookLM (SSOT Validator) | Drift 檢查 / 一致性審查 | Structure、State、Workflow、Write Matrix、DD、必要時 Schema | 不需 JIRA 操作指令、不中斷接管設計 |

---

## 4. ChatGPT (Governance) 新對話初始化 SOP

### 4.1 核心目標
用最少 Token 快速建立：

- 當前 phase / state awareness
- 結構邊界
- 最近治理決策
- 硬性限制（Hard Constraints）

### 4.2 必要檔案（Token 優化組合）
優先提供：

1. `PROJECT_STATE_SNAPSHOT.md`
2. `PROJECT_STRUCTURE.md`
3. `design_decision_log(節錄).md`
4. `AI_BOOTSTRAP(節錄).md`
5. `GOVERNANCE_WRITE_MATRIX.md`
6. `AI_COLLAB_WORKFLOW.md`

### 4.3 何時回查完整版
若本次對話涉及下列事項，需補讀完整文件：

- DD 追溯或版本衝突
- 結構變更提案
- STATE 權威判定
- Evolution Mode 啟動
- 規則是否已正式批准

### 4.4 初始化指令建議
新對話一開始，先要求 Governance AI：

1. 複述目前 Phase
2. 複述 Hard Constraints
3. 說明本次角色是 Governance 還是 Production
4. 說明哪些檔案是 authority、哪些只是 excerpt

---

## 5. ChatGPT (Production) 新對話初始化 SOP

### 5.1 核心目標
讓 Production 只拿到足夠完成任務的檔案，避免治理污染。

### 5.2 必要檔案
優先提供：

1. `PROJECT_STATE_SNAPSHOT.md`
2. `TASK_CONTRACT.md`
3. 本次任務相關的 `02_specs/*.schema.json`
4. 任務相關的 engine / data 檔案
5. `Effect_DSL_Behavior_Logic.md`（若任務涉及 DSL 行為）

### 5.3 不建議預先提供
原則上不要先給：

- `design_decision_log.md` 全文
- `AI_BOOTSTRAP.md` 全文
- `PROJECT_STATE.json` 全文
- `AI_COLLAB_WORKFLOW.md` 全文

除非：
- Governance 明確授權 Production 執行治理層修改
- 任務本身明確要求 cross-layer analysis

### 5.4 初始化檢查
Production 新對話開始時，應先確認：

- Task ID
- Scope
- Non-Scope
- Validation
- 是否允許改動 Schema / Governance（通常不允許）

---

## 6. Gemini (JIRA Bridge) 新對話初始化 SOP

### 6.1 核心目標
讓 Gemini 僅接收可轉成 JIRA 的任務摘要，不承接設計與治理語境。

### 6.2 必要檔案
僅提供：

1. `GEMINI_JIRA_PROMPT_STANDARD.md`
2. `TASK_CONTRACT.md` 第 7 節或由 Governance 整理好的 bridge payload

### 6.3 嚴禁提供
不得提供：

- `PROJECT_STATE.json`
- `design_decision_log.md`
- `AI_BOOTSTRAP.md`
- 長篇 DSL / Schema 解釋
- 治理審查全文
- audit report 全文（除非已被 Governance 壓縮成任務摘要）

### 6.4 初始化檢查
Gemini 任務開始前，應明確確認：

- Task Title
- Task Type
- Summary
- Acceptance Criteria
- Constraints
- Forbidden Content

若缺任一核心欄位，應視為 bridge payload 不完整。

---

## 7. NotebookLM 新對話初始化 SOP

### 7.1 核心目標
建立最小但足夠的 SSOT 驗證上下文。

### 7.2 必要檔案（建議順序）
優先提供：

1. `PROJECT_STRUCTURE.md`
2. `PROJECT_STATE.json`
   - 若僅需快速導入，可先給 `PROJECT_STATE_SNAPSHOT.md`
3. `GOVERNANCE_WRITE_MATRIX.md`
4. `AI_COLLAB_WORKFLOW.md`
5. `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md`
6. `design_decision_log(節錄).md`
7. 必要時再補 `02_specs/` 相關 schema

### 7.3 驗證時的權威原則
NotebookLM 可先用 excerpt 建立語境，  
但最終 drift 判定若涉及 authority，必須回查完整版：

- `PROJECT_STATE.json`
- `PROJECT_STRUCTURE.md`
- 完整 DD
- Schema contract

---

## 8. Excerpt Strategy（Token Optimized）

### 8.1 原則
節錄版文件的用途是：

- 快速建立語境
- 降低初始化 Token
- 提高新對話彈性

不是用來取代完整 SSOT。

### 8.2 適合使用節錄版的情境
可優先用 excerpt：

- 新對話初始化
- 快速對齊 phase / constraints
- 確認最近 3～5 個關鍵決策
- 判斷目前任務屬於 Governance 或 Production

### 8.3 不可只用節錄版的情境
以下情況不得只依 excerpt 判定：

- Structure authority
- State authority
- 是否允許修改 Governance 檔案
- DD 正式批准內容
- Schema / Contract 細節
- 最終 Drift Audit

---

## 9. Memory Anchor Strategy

為避免跨對話記憶漂移，每個新對話建議先完成以下三步：

### Step 1
優先讀取：
- `AI_BOOTSTRAP(節錄).md`
- `design_decision_log(節錄).md`

### Step 2
確認結構 SSOT：
- `PROJECT_STRUCTURE.md`

### Step 3
要求 AI 複述當前 Hard Constraints，例如：
- 不得修改 Schema
- 不得使用 `var.add` 於 content
- Production 不得修改 Governance 檔案
- JIRA 不得承載設計規則本體

若 AI 無法正確複述，表示初始化未完成。

---

## 10. Minimal Startup Sets

### Governance Minimal Set
- `PROJECT_STATE_SNAPSHOT.md`
- `PROJECT_STRUCTURE.md`
- `design_decision_log(節錄).md`
- `AI_BOOTSTRAP(節錄).md`
- `GOVERNANCE_WRITE_MATRIX.md`
- `AI_COLLAB_WORKFLOW.md`

### Production Minimal Set
- `PROJECT_STATE_SNAPSHOT.md`
- `TASK_CONTRACT.md`
- relevant schema
- relevant engine / data files

### Gemini Minimal Set
- `GEMINI_JIRA_PROMPT_STANDARD.md`
- bridge payload from Governance

### NotebookLM Minimal Set
- `PROJECT_STRUCTURE.md`
- `PROJECT_STATE.json`
- `GOVERNANCE_WRITE_MATRIX.md`
- `AI_COLLAB_WORKFLOW.md`
- `NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md`

---

## 11. Final Rule

> Excerpts are for orientation.  
> Full SSOT is for authority.

---