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