# NOTEBOOKLM_DRIFT_PROMPT_STANDARD.md

## 1. Purpose

本文件定義 NotebookLM 在本專案中的「Drift 檢查 Prompt 標準格式」，  
使其能穩定扮演 **SSOT Validator**，針對提交、更新或新文件進行一致性審查。

目的包括：

- 偵測 Naming Drift
- 偵測 Boundary Violation
- 偵測 Context Leakage
- 偵測 Structure Alignment 問題
- 以統一格式輸出風險與修正建議

---

## 2. Role Definition

NotebookLM 在本專案中的角色為：

> SSOT Validator

可做：
- 比對文件與 SSOT 是否一致
- 檢查 drift / violation / misplacement
- 提供修正導引

不可做：
- 不產出設計決策
- 不直接修改內容
- 不作為任務分派者
- 不取代 Governance 判斷

---

## 3. Core Principle

> NotebookLM validates against SSOT.  
> It does not define SSOT.

---

## 4. Standard Prompt Format

以下為 NotebookLM 專用標準 Drift 檢查 Prompt。

---

## 🤖 NotebookLM SSOT 驗證指令（Drift Audit）

### 【驗證目標】
請針對本次提交 / 更新 / 新增的檔案進行「漂移檢查」，  
確認其是否符合本專案 `00_context`、`01_design_docs`、`02_specs` 與既有治理規則。

---

### 【檢查範圍】
請審查以下檔案：

- <列出本次提交或本次要檢查的檔案>

---

### 【檢查基準（SSOT Priority）】
請依以下優先順序進行比對：

1. **結構基準**：`PROJECT_STRUCTURE.md`
2. **狀態基準**：`PROJECT_STATE.json`
   - 若僅需快速判讀，可輔助參考 `PROJECT_STATE_SNAPSHOT.md`
3. **治理基準**：
   - `GOVERNANCE_WRITE_MATRIX.md`
   - `AI_COLLAB_WORKFLOW.md`
   - `TASK_CONTRACT.md`
   - `GEMINI_JIRA_PROMPT_STANDARD.md`（若檢查 JIRA 任務格式）
4. **決策基準**：`design_decision_log.md`
5. **技術基準**：`02_specs/` 下相關 Schema 與 Contract 文件

---

### 【核心檢查項】

#### 1. Naming Drift
檢查是否存在非 Canonical 命名或與既有契約不一致的名稱。

例：
- 應使用 `flag.add_int`，卻使用 `flag.int_add`

---

#### 2. Boundary Violation
檢查是否發生跨層違規。

包括但不限於：
- `03_data` 出現 `var.add` 等 engine-only capability
- Production 修改 Governance 檔案
- Gemini 任務內容混入治理規則本體
- NotebookLM 驗證內容超出 validator 邊界

---

#### 3. Context Leakage
檢查任務描述、JIRA 內容、執行輸出中，是否混入不應出現的治理內容。

包括但不限於：
- 長篇 DSL 解釋
- DD 全文
- Schema 詳細設計
- 將設計文件內容直接塞進 JIRA

---

#### 4. Structure Alignment
檢查檔案位置與結構是否符合 `PROJECT_STRUCTURE.md`。

包括但不限於：
- 新檔案是否放在正確層級
- 是否未經 DD 授權新增頂層目錄
- 是否將 Governance / Specs / Data / Engine 混放

---

#### 5. State / Snapshot Consistency
若本次變更涉及 `PROJECT_STATE.json` 或 `PROJECT_STATE_SNAPSHOT.md`，請檢查：

- Snapshot 是否正確作為 mirror
- Snapshot 是否錯誤取代 JSON authority
- STATE 與 SNAPSHOT 是否存在語意不同步

---

#### 6. Workflow Alignment
若本次變更涉及 AI 協作、任務下發、JIRA bridge、驗證流程，請檢查：

- 是否符合 `AI_COLLAB_WORKFLOW.md`
- 是否符合 `TASK_CONTRACT.md`
- 是否符合 `GEMINI_JIRA_PROMPT_STANDARD.md`

---

### 【輸出格式】
請以條列方式列出所有發現項，並使用以下格式：

- **Issue Type**：Naming Drift / Boundary Violation / Context Leakage / Structure Alignment / State Drift / Workflow Misalignment
- **Risk Level**：Warning / Critical / Fail
- **File(s)**：受影響檔案
- **Finding**：問題描述
- **Suggested Fix**：修正建議

---

### 【結尾判定】
最後請補一段總結，明確回答：

1. 本次提交是否 **SSOT Aligned**
2. 是否存在 **必須退回 Governance 處理** 的項目
3. 是否可進入下一步（如：commit / JIRA / implementation）

---

## 5. Minimal Usage Example

### Example Prompt

請針對以下檔案進行 Drift 檢查：

- `00_context/TASK_CONTRACT.md`
- `00_context/GEMINI_JIRA_PROMPT_STANDARD.md`

請依以下 SSOT Priority 比對：

1. `PROJECT_STRUCTURE.md`
2. `PROJECT_STATE.json`
3. `GOVERNANCE_WRITE_MATRIX.md`
4. `AI_COLLAB_WORKFLOW.md`
5. `design_decision_log.md`

重點檢查：
- 是否有跨層邊界違規
- 是否有任務格式與 JIRA bridge 格式不一致
- 是否有將治理規則全文不當壓入 Gemini prompt 的風險

請以：
- Issue Type
- Risk Level
- File(s)
- Finding
- Suggested Fix

的格式輸出。

---

## 6. Excerpt Strategy

為節省 Token，NotebookLM 初始化時建議優先讀取：

- `PROJECT_STATE_SNAPSHOT.md`
- `AI_BOOTSTRAP(節錄).md`
- `design_decision_log(節錄).md`

但若審查對象涉及：
- 狀態權威
- 結構權威
- 寫入權限
- Schema / Contract

則必須回查完整 SSOT 文件，不得僅依節錄版做最終判定。

---

## 7. Final Rule

> If the review requires authority, use the full SSOT.  
> If the review only requires orientation, excerpt files are allowed.

---