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