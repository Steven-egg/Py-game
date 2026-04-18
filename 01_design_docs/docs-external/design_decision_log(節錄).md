## DD-016 – Effect Dispatcher Expansion
- Added: inventory.add/remove, flag.int_add, var.add
- Engine-only capability expansion (no schema change)

---
## DD-017
Date: 2026-04-11  
Title: AI Snapshot Mirror & Structure Readability Layer Introduction  

Impact: High  
Scope: AI Governance / Context Layer / Structure Readability / Drift Prevention  

---

### Reason

在 Phase C 完成後，專案進入 Phase D 準備階段。

過程中發現以下問題：

1. AI 工具（如 ChatGPT / NotebookLM）無法穩定解析：
   - `PROJECT_STATE.json`
   - `tree /f` 原始結構輸出

2. 多對話環境中，AI 容易產生：
   - State 解讀不一致
   - Structure 誤判
   - Architecture Drift（架構漂移）

3. 原有治理機制雖完整（AI_BOOTSTRAP / PROJECT_STATE / DD），
   但缺乏「AI 可穩定讀取的中介層（Readable Layer）」。

---

### Decision

正式引入「AI 可讀治理層（AI-Readable Governance Layer）」：

#### 1. PROJECT_STATE_SNAPSHOT.md（狀態鏡像）

- 作為 `PROJECT_STATE.json` 的 HUMAN / AI 可讀鏡像
- 僅用於閱讀與推理，不具 SSOT 地位
- 明確規定：
  - JSON 為唯一狀態來源
  - Snapshot 不可反向修改 JSON

---

#### 2. AI_BOOTSTRAP.md Snapshot 區段強化

- 在文件最前方加入：
  - Current Snapshot
  - Verified Runtime Scope
  - Structural Constraints
- 明確標示：
  - Snapshot 為 mirror
  - PROJECT_STATE.json 為唯一 authority

---

#### 3. PROJECT_STRUCTURE.md（AI 可讀強化）

- 明確定義為 Structure SSOT
- 新增：
  - Human + AI readable structure overview
  - Layer responsibility definition
  - AI reading protocol（禁止依賴 tree /f）
- 作為所有 AI 判斷結構的唯一依據

---

#### 4. Structure Reading Protocol 建立

AI 在分析專案結構時：

1. 必須優先讀取 `PROJECT_STRUCTURE.md`
2. 禁止依賴：
   - tree /f
   - raw filesystem dump
3. 發生衝突時：
   - 以 PROJECT_STRUCTURE.md 為準

---

#### 5. Governance Layer 明確化（00_context）

正式確認 `00_context` 為：

- AI 協作控制層
- 狀態錨點層
- Drift 防護層

包含：

- AI_BOOTSTRAP.md
- PROJECT_STATE.json
- PROJECT_STATE_SNAPSHOT.md

---

### Result

建立完整三層治理結構：

PROJECT_STATE.json ← State SSOT
↓
PROJECT_STATE_SNAPSHOT.md ← AI-readable mirror
↓
AI_BOOTSTRAP.md ← Governance entry


並與：

PROJECT_STRUCTURE.md ← Structure SSOT
design_decision_log.md ← Evolution history


形成完整治理閉環（Governance Loop）。

---

### Impact

- 消除 AI 無法解析 JSON / tree 結構問題
- 顯著降低 Architecture Drift 風險
- 建立 deterministic AI 協作行為
- 強化多對話一致性
- 不引入新的 SSOT（避免分裂）

---

### Constraints

- Snapshot 不得取代 JSON
- 不得新增獨立治理檔（如 AI_COLLAB_PROTOCOL.md）
- 所有結構變更仍需 DD 流程
- 不啟動 Evolution Mode（本決策屬治理優化）

---

## DD-018
Date: 2026-04-11
Title: Phase D.1 Runtime Location Context 與 Interactive CLI Loop 導入

Impact: Mid
Scope: 05_engine/cli_mvl.py、05_engine/quest_runtime.py、05_engine/location_runtime.py

Reason:
Phase D 的目標是先驗證 World / Location context layer 的最小可行形態，
且必須在不修改 Schema、不修改 Loader、不變更專案結構的前提下完成。

原本 CLI 採單次 subcommand 模式，
無法在同一個 session 內持續保留 runtime-only location state，
因此無法自然驗證：
- wrong location -> block
- correct location -> allow

同時，Quest 完成條件雖已由 Condition evaluator 驗證，
但尚未具備 context-aware action gating 能力。

Decision:
- 導入 interactive CLI loop，取代原本單次命令式操作
- 新增 runtime-only location context（session-scoped）
- 新增 location_runtime.py，提供：
  - valid locations scaffold
  - current_location runtime context
  - engine-side quest completion gate
- CLI 新增指令：
  - where
  - locations
  - move <location_id>
- QuestRuntime.check_complete(...) 擴充 runtime_context 參數
- 在 complete_condition / legacy objectives 通過後，統一接入 check_location_gate(...)
- location gate 採 engine-side overlay rule，不進 schema、不進 content JSON

Validation:
已驗證以下行為：
1. 完成條件未滿足時，仍由既有 condition system 優先阻擋
2. 完成條件滿足但位置錯誤時，completion 被 location gate 阻擋
3. 完成條件滿足且位置正確時，任務可正常完成並套用 effects
4. Save / completed_ids / reward dispatch 流程維持穩定
5. 未引入 schema change / loader change / structure change

Result:
- Phase D.1 完成
- Engine 開始具備最小世界位置語境（location-aware runtime）
- 為後續 D.2（location persistence / action gate expansion / world layer evaluation）建立基礎

---


## DD-019
Date: 2026-04-12
Title: Phase D.2 Location Persistence via save.game_state.current_location

Impact: Mid
Scope: 02_specs/schema/save.schema.json、05_engine/cli_mvl.py、05_engine/save_manager.py、05_engine/location_runtime.py

Reason:
Phase D.1 已完成 runtime-only location context 驗證，
確認 engine 已具備最小 location-aware behavior gate，
但 current_location 僅存在於 session runtime context，
重啟 CLI 或 reload 後會回到預設值，無法跨 session 持續保存位置狀態。

此限制造成以下問題：
1. 地理位置無法成為持久化存檔狀態的一部分。
2. location gate 雖可作用於 completion flow，但無法跨 session 延續。
3. 後續若擴張 accept gate / event gate / action gate，將持續依賴 runtime-only overlay，增加狀態漂移風險。

因此，Phase D.2 採用最小範圍演進策略，
將 current_location 從 runtime-only context 提升為 save-state 的持久化欄位，
但不引入正式 world/location schema，也不修改 content layer 或 loader contract。

Decision:
- 正式進入 Evolution Mode（Spec Version 1.2.0 → 1.3.0）
- 不新增 `location.schema.json`
- 不新增 `world.schema.json`
- 不修改 `03_data` 內容格式
- 不修改 ContentLoader 行為
- 僅於 `save.schema.json` 的 `game_state` 下新增：
  - `current_location: string`
- `current_location` 預設值定為 `start_village`
- `current_location` 不列入 `game_state.required`，以維持舊存檔向後相容
- `cli_mvl.py` 啟動與 reload 時，runtime_context 改由 `game_state["current_location"]` 回填
- `move <location_id>` 成功後，除更新 runtime_context 外，必須同步寫入 `game_state["current_location"]`
- `save_manager.py` 升級至與 `save.schema.json` 對齊的新 save payload 格式：
  - `save_schema`
  - `engine_version`
  - `content_manifest_hash`
  - `active_quest`
  - `game_state`
  - `completed_ids`
- 舊存檔若缺少 `current_location` 或新 metadata 欄位，load 時自動補預設值並允許 self-healing write-back

Single Writer Rule:
- `game_state["current_location"]` 為持久化 SSOT
- `runtime_context["current_location"]` 僅為 session mirror / cache
- engine 不得讓 runtime_context 成為獨立真實來源

Validation:
已完成以下驗證：
1. 啟動 CLI 時，runtime_context 可由 `game_state.current_location` 正確回填
2. `move forest_edge` 後，`game_state` 與 `runtime_context` 皆同步更新
3. `save` 後 `slot_d2_test.json` 內容符合新 save payload 格式
4. `reload` 後位置不再重置為預設值，而是正確回填存檔位置
5. 已驗證 `start_village ↔ forest_edge` 往返切換、存檔、重載後皆維持正確位置
6. 新 save 檔內容確認如下結構：
   - `save_schema`
   - `engine_version`
   - `content_manifest_hash`
   - `active_quest`
   - `game_state.current_location`
   - `completed_ids`

Result:
- Phase D.2 的核心位置持久化已完成
- location state 正式納入 save-state SSOT
- CLI 已具備跨 session 的位置連續性
- save payload 已與 `save.schema.json` 對齊
- 為後續 accept / event / action flow 的 location gating 擴張建立持久化基礎
- 未引入 structure change
- 未引入 loader change
- 未引入 content contract change

---

---

### Evolution Closure – Phase D.2

Status: Exiting Evolution Mode

Evolution Summary:
- Spec Version: 1.2.0 → 1.3.0
- Structure Version: 1.2.0 (UNCHANGED)
- Engine Version: 1.0.0 (UNCHANGED)

Scope of Evolution:
- save.schema.json extended (current_location added)
- cli_mvl.py updated (persistent location sync + reload restore)
- save_manager.py updated (new save payload alignment)
- runtime_context redefined as mirror of persistent state

Governance Compliance:
- No structure changes introduced
- No loader behavior modified
- No content layer contract changed
- All schema evolution executed via Design Decision (DD-019)
- No cross-layer contamination detected

Validation:
- CLI persistence loop verified (move → save → reload → restore)
- Bidirectional location switching validated (start_village ↔ forest_edge)
- Save payload verified against save.schema.json
- Backward compatibility verified via load-time normalization
- MVL Protocol regression completed under Spec 1.3.0

Final State:
- Location persistence integrated into State SSOT
- runtime_context downgraded to session mirror
- Single Writer Rule enforced (game_state as source of truth)

Conclusion:
Phase D.2 is COMPLETE.
Evolution Mode is now CLOSED.
System returns to Lock + Controlled Evolution baseline.

---

以下為可直接寫入 `design_decision_log.md` 的正式版本（精簡且符合既有 DD 格式）：

---

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

# 📄 DD-021 – AI Collaboration Workflow Governance

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