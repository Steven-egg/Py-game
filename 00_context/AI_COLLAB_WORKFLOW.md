# 📄 AI_COLLAB_WORKFLOW.md

# AI Collaboration Workflow (Draft)

## 1. Purpose（目的）

本文件定義本專案中 ChatGPT、Gemini、JIRA 與 NotebookLM 之協作模式，  
目的在於：

- 防止 AI 語境混用（Context Leakage）
- 維持 DSL / Schema / Data / Engine 的分層邊界
- 建立穩定的任務 → 實作 → 驗證 → 回饋流程
- 確保所有產出符合 SSOT（Single Source of Truth）

---

## 2. System Context（系統背景）

本專案採用以下分層架構：

- 00_context → Governance（AI 協作與狀態控制）
- 01_design_docs → 設計文件（DSL / Blueprint / Audit）
- 02_specs → 技術契約（Schema）
- 03_data → 內容資料（JSON）
- 05_engine → 執行層（Python）

本文件屬於 **Governance Layer（00_context）**。

---

## 3. AI Role Definition（AI 角色分工）

### 3.1 ChatGPT – Governance / Production

#### Governance 模式（設計層）
負責：
- DSL 設計與修改
- audit_reports 文件（DSL-4 / DSL-7 等）
- Blueprint（如 Phase D.4）
- SOP 文件
- 任務拆解（由設計轉為可執行步驟）

禁止：
- 不直接操作 JIRA
- 不輸出 JIRA 結案格式
- 不混入任務追蹤語言

---

#### Production 模式（實作層）
負責：
- Python 程式碼（05_engine）
- JSON 內容（03_data）
- Debug / 測試

限制：
- 不主動修改 DSL / Schema 規範
- 若發現問題，需回報 Governance 層決策

---

### 3.2 Gemini – JIRA Bridge

負責：
- 指導 JIRA 操作（建立 Epic / Task / Subtask）
- 將任務拆解轉為 JIRA 卡片格式
- 協助撰寫簡短 JIRA 留言（Done / Progress）

限制：
- 不參與 DSL 設計
- 不產出 audit_reports
- 不解釋 Schema / DSL 規則

---

### 3.3 JIRA – Task Tracking System

用途：
- 任務管理（To Do / In Progress / Done）
- 工作分配與進度追蹤
- 完成紀錄（簡短）

限制：
- 不存放 DSL 規範內容
- 不存放長篇設計文件
- 不作為 SSOT

---

### 3.4 NotebookLM – SSOT Validator

負責：
- 比對文件與專案 SSOT 是否一致
- 檢查是否發生：
  - DSL Naming Drift
  - Boundary Violation
  - Schema / Data 不一致
- 判斷新文件應落在哪一層（Structure Alignment）

限制：
- 不產生任務
- 不產生設計決策
- 不直接修改內容

---

### 3.5 Role Matrix（Enforcement）

| Component     | Can（負責） | Cannot（禁止） |
|--------------|------------|----------------|
| ChatGPT (Governance) | DSL / Blueprint / audit_reports / 任務拆解 | 寫 JIRA 卡片 / 寫結案留言 |
| ChatGPT (Production) | code / JSON / Debug | 修改 DSL / Schema |
| Gemini        | JIRA 建立 / 操作 / 簡短留言 | 設計 DSL / 解釋 Schema |
| JIRA          | 任務狀態 / 完成紀錄 | 存放設計文件 / DSL 規範 |
| NotebookLM    | SSOT 比對 / drift 檢查 | 產出任務 / 修改內容 |

違反上述規則視為 **Context Drift（語境漂移）**，需回 Governance 層修正。

---

## 4. Workflow（工作流程）

### 4.1 基本流程



Governance（ChatGPT）
↓
任務拆解（ChatGPT）
↓
JIRA 建立（Gemini + User）
↓
任務執行（ChatGPT / Production）
↓
JIRA 結案（Gemini）
↓
SSOT 驗證（NotebookLM）



---

### 4.2 回饋機制（Critical）



Production 發現問題
↓
回報 Governance
↓
更新 DSL / Blueprint / SOP
↓
重新拆解任務



---

## 5. JIRA Usage Policy（JIRA 使用規範）

JIRA 僅允許以下內容：

- 任務標題（做什麼）
- 任務描述（簡要）
- 完成紀錄（Done）
- 驗證方式（簡要）

### 5.1 標準結案格式



[Done]

交付物：

* xxx.md / xxx.py

完成內容：

* 做了什麼

驗證：

* 如何確認完成

備註：

* commit / 下一步



---

### 5.2 禁止事項

- ❌ DSL 規範解釋
- ❌ Gate / Audit 詳細內容
- ❌ 長篇設計說明
- ❌ Schema 細節

---

### 5.3 Enforcement（強制規則）

若 JIRA 出現以下內容，視為違規：

- DSL 規範說明
- Gate 判讀內容
- Schema 詳細設計
- 長篇 audit 分析

處理方式：

1. 該內容應移至 `01_design_docs/audit_reports`
2. JIRA 僅保留：
   - 任務結果
   - 驗證方式
   - commit 記錄

違規內容不得作為 SSOT 依據。

---

## 6. Boundary Rules（邊界規則）

### 6.1 層級隔離

- DSL / Blueprint → 僅存在 01_design_docs
- Schema → 僅存在 02_specs
- Data → 僅存在 03_data
- Engine → 僅存在 05_engine

---

### 6.2 AI 跨層限制

- Production 不得修改 DSL
- JIRA 不得承載設計文件
- Governance 不直接操作 runtime

---

## 7. SSOT Alignment（SSOT 對齊）

所有產出必須符合：

- PROJECT_STRUCTURE.md（結構 SSOT）
- PROJECT_STATE.json（狀態 SSOT）
- DSL 規範文件（設計 SSOT）

### 7.1 SSOT Source Priority

NotebookLM 之檢查基準如下：

1. 00_context（Governance 規則）
2. 01_design_docs（設計 SSOT）
3. 02_specs（Schema）
4. 03_data（內容）

JIRA 不屬於 SSOT，不作為任何規則或設計依據。


---

## 8. Update Protocol（更新流程）

本協作模式更新順序：



1. 更新本文件（AI Workflow）
2. NotebookLM 判斷是否符合 SSOT
3. 必要時新增或更新 Design Decision（DD）
4. 更新 PROJECT_STATE.json
5. 才允許影響實作（code / data）



---

## 9. Status（狀態）

- 狀態：Draft
- 適用階段：Pre D.4 Activation
- 待確認：是否納入正式 Governance（DD）

---


---