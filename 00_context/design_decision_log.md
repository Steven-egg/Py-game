# Design Decision Log

---

## DD-001
Date: 2026-02-21  
Title: 資料夾分層架構定義  

決定採用三層架構：
- design_docs
- specs
- data

Impact: High  
Scope: 專案整體資料結構  

Reason:
避免系統設計與實際資料混淆。

---

## DD-002
Date: 2026-02-21  
Title: Flag 命名規則  

決定採用全小寫 snake_case。

Impact: High  
Scope: 所有 Flag 與條件判斷系統  

Reason:
避免大小寫混亂與 JSON 解析錯誤。

---

## DD-003
Date: 2026-02-21  
Title: JSON Schema 命名規則  

規範：
- event.schema.json
- item.schema.json
- monster.schema.json

禁止使用：
- EventSchemaV1Final2.json

Impact: High  
Scope: 所有 schema 檔案  

Reason:
確保命名一致性與可維護性。

## DD-004
Date: 2026-02-21  
Title: 資料夾預計 JSON Schema 資料生成結構 

Project_RPG/
│
├── 00_context/
│   ├── Project_Context_v1_bootstrap.json
│   └── Project_Soul.json
│
├── 01_design_docs/
│   ├── system_design/
│   │   ├── guild_system.txt
│   │   ├── crafting_system.txt
│   │   ├── shop_system.txt
│   │   ├── battle_system.txt
│   │   ├── dungeon_system.txt
│   │   ├── movement_system.txt
│   │   └── story_system.txt
│   │
│   └── worldbuilding/
│       └── base_setting.txt
│
├── 02_specs/
│   ├── schema/
│   │   └── *.schema.json
│   │
│   └── engine_contract.md
│
├── 03_data/
│   ├── monsters/
│   ├── items/
│   ├── quests/
│   ├── dungeons/
│   ├── events/
│   └── dialogues/
│
├── 04_assets/
│   ├── backgrounds/
│   ├── characters/
│   ├── monsters/
│   ├── ui/
│   └── audio/
│
└── 05_engine/
    ├── main.py
    ├── battle_manager.py
    ├── event_dispatcher.py
    └── ...

Note:
Schema file inventory is defined in PROJECT_STATE.json.
DD-004 defines folder hierarchy only.

Impact: High  
Scope: 專案整體資料夾結構、未來所有 AI 對話初始化流程、JSON 生成與規格書對齊機制  

Reason:
這是首次發現多對話產生架構漂移（Architecture Drift）的問題。
為避免未來在不同 AI 對話中產生多版本資料夾結構與規格不一致情況，
正式定義本專案的官方目錄標準，作為 Single Source of Truth (SSOT)。
未來任何新增對話或大型規格生成，必須以此結構為依據，不得自行重構目錄層級。

---

## DD-005
Date: 2026-02-21  
Title: 新對話架構遵循規則（AI Governance Rule）

規則：
所有新開啟之 AI 對話（ChatGPT / Gemini / Claude），
在進行規格生成、資料夾規劃或系統重構前，
必須先讀取 PROJECT_STRUCTURE.md 與 design_decision_log.md。

若 AI 產生與官方結構不一致之資料夾規劃，
應以 PROJECT_STRUCTURE.md 為唯一標準，
不得直接採納新生成之目錄層級。

Impact: High  
Scope: 所有未來 AI 協作流程、專案架構穩定性  

Reason:
為避免多對話產生架構漂移（Architecture Drift），
確保專案始終維持 Single Source of Truth (SSOT)，
並防止不同 AI 各自生成獨立結構導致版本分裂。


---

## DD-006
Date: 2026-02-22  
Title: Architecture Evolution Protocol 引入  

決定正式引入 Controlled Evolution Mode，
允許在不破壞 SSOT 前提下進行核心規格演進。

Impact: High  
Scope: AI 治理流程、Schema 演進機制、未來核心模組新增  

Reason:  
原 AI_BOOTSTRAP 為鎖定型治理（Lock Mode），
在核心規格成形階段已足夠。  

但隨著 Condition / Rule Engine / Monster Schema 等核心模組即將加入，
需要建立「如何改變規則的規則」，
避免凍結架構同時維持治理穩定性。  

本決策導入 Evolution Protocol，
確保所有結構性變動均經分析、記錄與版本控管。

---

## DD-007
Date: 2026-02-22  
Title: Condition Schema（cond@1.0）導入  

決定新增 `condition.schema.json` 作為「純條件判斷層」的統一規格，
供 Quest/Monster/Dungeon/Dialog 等內容層使用，避免各模組自行發明判斷格式。

Impact: High  
Scope: 內容層條件判斷、規則引擎介面、未來內容擴充  

Reason:
目前已有 Effect（結果）與 Flag Registry（狀態治理），
但缺少可重用、可巢狀組合的 Condition 描述格式。
導入 Condition 可維持 Single Writer Rule，同時提升資料驅動表達力。

---

## DD-008
Date: 2026-02-22  
Title: Monster Schema（monster@1.0）導入  

決定新增 `monster.schema.json` 作為內容層（Content Layer）的第一個正式 Schema，
用於定義怪物 ID、顯示文字、數值、掉落與 hooks（以 effects 表達）。

Impact: High  
Scope: 戰鬥/遭遇/掉落/任務擊殺等內容資料一致性  

Reason:
Monster 是內容層整合測試的最佳起點：
會同時觸及 stats、drops、condition、effects、TextKey 等既有治理要素，
可用於驗證 schema DAG 是否健康並避免後續 schema 飄移。

---

## DD-009: Effect/Event Schema 檔名正名（語意對齊）

**Date:** 2026-02-22  
**Impact:** Mid  
**Scope:** Schema Layer（effect/event + quest reward refs）  

### Reason
發現 `effect.schema.json` 與 `event.schema.json` 檔名與實際 `$id` 及語意內容互換。
為確保 SSOT 語意一致性、長期可維護性與 Engine Contract 清晰度，
執行檔名正名與 $ref 對齊修正。

### Decision
- 對調 `effect.schema.json` / `event.schema.json` 檔名，使其與 `$id` 與語意一致
- 修正 `quest.schema.json` rewards.effects 的 `$ref`
- 執行 MVL v2 驗證（PASS 4 / FAIL 0）

### Result
Schema 命名與語意一致：
- Effect = 可執行指令
- Event = Runtime Envelope
專案治理恢復語意健康狀態。

---

## DD-010
Date: 2026-02-22  
Title: Quest Fixture 擴充與 Condition Pattern 壓測  

Impact: Mid  
Scope: MVL Fixture（03_data/quests/test_*.json）、Condition 使用模式  

Reason:
在 quest.schema.json 完成後，為避免 Condition 表達力不足或命名規範不一致導致後續引擎落地卡關，
新增多樣化 Quest Fixture（Kill 模擬/Flag 驅動/複合條件）進行壓測，
並透過 MVL v2 驗證 pattern gate（flag key format、compare op enum 等）確實生效。

Decision:
新增以下 Quest Fixtures：
- test_kill_slime.json（以 flag.int_compare 模擬擊殺計數）
- test_story_gate.json（純 flag 驅動完成條件）
- test_complex_trial.json（and + nested conditions）

並統一遵循：
- flag key pattern：flg.<domain>.<subdomain>.<name>
- compare op enum：eq/gt/gte/lt/lte（禁止使用 >= <= 等符號）

Result:
MVL v2 驗證結果：PASS 7 / FAIL 0  
確認 Condition Schema 的 enum/pattern 約束可有效阻擋語意與命名錯誤，  
可進入 Engine Phase B（05_engine 最小閉環）開發。

---

## DD-011
Date: 2026-02-23  
Title: Engine Phase B MVL：Fixture `$schema` 缺失處理策略  

Impact: Mid  
Scope: 05_engine/content_loader、CLI MVL 行為、Fixture Schema 驗證策略  

Reason:
在 Engine Phase B 最小閉環（CLI MVL loop）實作過程中，
發現部分測試 fixture 未包含 `$schema` 欄位。

若於 runtime 階段將此視為 fatal，
將阻斷 MVL 行為驗證與引擎閉環測試。

同時，Schema Gate 已由 `05_engine/validation/mvl_test_v2.py` 負責嚴格驗證，
因此 runtime 不需再次阻擋 schema 缺失。

Decision:
Runtime 對 schema 缺失採 **Warning（非 Fatal）策略**

分類如下：

- io / json / shape → **Fatal**
- schema → **Warning（僅 load 顯示）**

Result:
- CLI MVL loop 可完整運行
- Schema Gate 與 Behavior Gate 分工明確
- 不影響 SSOT、Schema Discipline 或 MVL 驗證流程

---

## DD-012
Date: 2026-02-25
Title: CLI questdump 語意預覽輸出（Condition/Effect Debug Preview）

Impact: Low
Scope: 05_engine/cli_mvl.py（questdump command 輸出格式）

Reason:
現行 questdump 僅顯示 dict keys，無法快速驗證 Condition/Effect 的語意是否命中（例如：
q.side.slime_hunt 應為 flag.int_compare；
q.elite.trial_of_balance 應為 and + nested conditions；
rewards.effects 應呈現 Effect 指令形狀）。
此缺口會拖慢 Behavior Gate（CLI MVL）除錯效率。

Decision:
在不改變任何資料結構與 runtime 行為前提下，
將 questdump 輸出擴充為「摘要 + 關鍵值預覽」：
- complete_condition.type
- complete_condition.params.preview（flag_key/op/value）或 composite 的 conditions.len + preview_types
- rewards.effects.len + effects[0].type + effects[0] keys

Result:
可於 CLI 直接確認：
- flag.int_compare / and + nested condition 的解析穩定性
- rewards.effects 的 Effect 語意形狀（避免 Effect/Event 語意錯置）
不影響 SSOT、Schema Gate 或 MVL loop 行為。

---


## DD-013
Date: 2026-02-25  
Title: Quest accept_condition 接入 Condition evaluator（Behavior Gate）

Impact: Mid  
Scope: 05_engine/quest_runtime + 05_engine/cli_mvl accept behavior  

Reason:
Phase B MVL 需驗證「任務可接取門檻」可由資料驅動（accept_condition）控制，
並且應與 complete_condition 使用同一套 Condition schema（避免雙軌規則漂移）。

Decision:
- accept_condition 評估改由 QuestRuntime 的 Condition evaluator 處理
- 支援 leaf：flag.is_true / flag.is_false（MVP）
- CLI accept 若 accept_condition 不通過，拒絕接取並輸出 reason

Result:
- accept gate 行為可被 CLI list / accept 直接驗證
- 完整對齊 Condition schema 的單一判斷引擎（Single Writer Rule）

---

## DD-014
Date: 2026-02-25  
Title: SaveBlob 擴充 completed_ids（向後相容的存檔演進）

Impact: Mid  
Scope: 05_engine/save_manager + save format evolution  

Reason:
Phase B 開始需要表示「任務已完成」以支援 one-shot 任務語意與任務大廳顯示，
單靠 active_quest.completed_at 無法表示歷史完成狀態（完成後仍需可追溯）。

Decision:
- SaveBlob 新增 completed_ids: List[str]
- load 時若舊存檔缺欄位，補預設 []（Backward compatible）
- save 時固定輸出 completed_ids

Result:
- 不破壞既有存檔與 MVL loop
- 支援 CLI list 的 DONE 狀態與後續任務線 gating 擴充

---

## DD-015
Date: 2026-02-25  
Title: CLI 任務大廳（list）與 active quest guard / 完成後釋放 active

Impact: Low  
Scope: 05_engine/cli_mvl behavior & UX  

Reason:
Phase B 的核心是「驗證邏輯」，若需逐一 accept 才知道可接任務會降低除錯效率；
同時需避免 slot 內多個 active quest 覆寫導致測試不穩定。

Decision:
- CLI list 顯示 [DONE]/[ACTIVE]/[READY]/[LOCKED]，LOCKED 顯示 accept_condition reason
- CLI accept 增加 active quest guard（未完成時禁止接新任務）
- CLI complete 成功後：
  - 將 quest_id 追加到 completed_ids（避免重覆）
  - 清空 active_quest（讓下一個任務能被接取）

Result:
- CLI 成為可用的「遊戲大廳 / 除錯面板」
- 減少測試時的人為狀態錯誤與覆寫風險

---

## DD-016
Date: 2026-02-27
Title: Effect Dispatcher Expansion（Engine Layer Only）

Impact: Low
Scope: 05_engine/effect_executor

Reason:
為擴充內容層表達能力，在不修改 Schema、不改結構、不進入 Evolution Mode 前提下，
新增 inventory.add / inventory.remove / flag.int_add / var.add。

Decision:
擴充 EffectExecutor dispatcher，僅操作 save.game_state。
不讀 fixture，不改 schema。

Result:
Phase C 完成。
Regression 驗證通過。

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


# DD-021 – AI Collaboration Workflow Governance

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

好，這一步我直接幫你做到**可落地、可寫入、可執行**的正式版本。
以下內容你可以**直接貼進 `design_decision_log.md`**。

---

# 📄 DD-022 – Governance Layer Normalization & Structure Alignment

## Status

Accepted

## Date

2026-04-20

## Impact

High

## Scope

* 00_context（Governance Layer）
* 03_data（Structure Extension – registries）
* GOVERNANCE_INDEX.md（Navigation Alignment）

---

## 1. Context（背景）

在 Phase D.3 完成後，專案進入 D.4 準備階段，
透過 NotebookLM Drift Audit 發現以下問題：

---

### 1.1 Naming Drift（命名不一致）

* `PROJECT_STATE.json` 採 Canonical Uppercase
* `Project_Context_v1_bootstrap.json` 採 mixed naming + version suffix
* `Project_Soul.json` 採 PascalCase

👉 導致：

* AI 難以辨識 authority file
* 增加跨對話 context drift 風險

---

### 1.2 Structure Drift（結構未對齊）

* `03_data/registries/` 已實際存在
* 但未被 `PROJECT_STRUCTURE.md` 定義

👉 屬於：


Structure SSOT 與實體結構不一致


---

### 1.3 Navigation 不一致（讀取層優化需求）

* Snapshot 已加入 `AI Quick Context`
* 但 GOVERNANCE_INDEX 尚未反映「快速初始化層」

👉 導致：

* INIT_SOP 與實際使用模式略有偏差

---

## 2. Decision（決策）

本 DD 定義三項治理演進：

---

## 2.1 Governance Naming Normalization（命名標準化）

### Decision

將 Governance Layer JSON 檔案統一為：


CANONICAL UPPERCASE + snake_case


---

### Rename Mapping


Project_Context_v1_bootstrap.json → PROJECT_CONTEXT.json
Project_Soul.json                → PROJECT_SOUL.json


---

### Rules

1. ❌ 禁止 version suffix（如 v1, v2）
2. ❌ 禁止 PascalCase / mixedCase
3. ✔ 統一使用：

   * `PROJECT_*`
   * `UPPERCASE_WITH_UNDERSCORE`

---

### Rationale

* 強化 AI 對「authority file」辨識
* 降低 naming drift
* 對齊 `PROJECT_STATE.json`

---

## 2.2 Structure Extension（registries 正式納入）

### Decision

正式將以下目錄納入 Structure SSOT：


03_data/
  registries/


---

### Definition


registries = cross-entity mapping / lookup layer


用途：

* DSL registry
* effect mapping
* future schema-driven injection

---

### Constraint

* 不改變既有 content contract
* 不影響 loader 行為
* 不影響 engine runtime

---

### Rationale

* registry 已在 Phase D.3 實際使用
* 屬於 Schema–Data 中介層
* 為 D.4（Registry–Schema Sync）預備

---

## 2.3 Navigation Layer Alignment（讀取層對齊）

### Decision

將以下概念正式納入治理：


AI Quick Context = Startup Layer


---

### Classification Update

| Layer               | Files                                       |
| ------------------- | ------------------------------------------- |
| Core Governance     | PROJECT_STATE.json / PROJECT_STRUCTURE.md   |
| Decision History    | design_decision_log.md                      |
| Navigation Layer    | GOVERNANCE_INDEX.md / AI_COLLAB_INIT_SOP.md |
| Startup Layer (NEW) | PROJECT_STATE_SNAPSHOT.md (Quick Context)   |

---

### Rule


Startup Layer = 快速初始化（非 authority）


---

### Rationale

* 對齊 INIT_SOP 的 minimal startup strategy
* 降低 token 成本
* 提高 AI 初始化穩定性

---

## 3. Implementation（實作步驟）

---

### Step 1 – 檔名調整

git mv 00_context/Project_Context_v1_bootstrap.json 00_context/PROJECT_CONTEXT.json
git mv 00_context/Project_Soul.json 00_context/PROJECT_SOUL.json

---

### Step 2 – 更新 PROJECT_STRUCTURE.md

新增：

03_data/
  registries/

---

### Step 3 – 更新 GOVERNANCE_INDEX.md

新增：

Startup Layer:
- PROJECT_STATE_SNAPSHOT.md (AI Quick Context)

---

### Step 4 – 更新 PROJECT_STATE.json

在 `notes` 或 `governance_extensions` 補：

"DD-022 established: Governance Naming + Structure Alignment + Startup Layer introduction"

---

### Step 5 – Drift Audit（驗證）

使用 NotebookLM 檢查：

* structure alignment
* naming consistency
* SSOT integrity

---

## 4. Constraints（限制）

* ❌ 不修改 schema（Spec 1.3.0 保持）
* ❌ 不修改 engine
* ❌ 不修改 content JSON
* ❌ 不改變 workflow（DD-021）

---

## 5. Consequences（影響）

---

### Positive

* 消除 naming drift
* 修復 structure SSOT 不一致
* 強化 AI 初始化穩定性
* 為 Phase D.4 建立基礎

---

### Trade-off

* 需要一次性檔名遷移（git history 變更）
* GOVERNANCE_INDEX 需同步維護

---

## 6. Final State（完成後狀態）

✔ Naming fully canonical
✔ Structure fully aligned
✔ Startup layer established
✔ Ready for Phase D.4

### Approval

Approved by: Governance (User)
Effective Date: 2026-04-20

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

