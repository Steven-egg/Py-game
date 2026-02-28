# 元素崩壞：遺落的試煉地 — Text RPG Engine v1 工程規格文件

（Python + Pygame 前視角 UI / Data-Driven / Modular）

## Version Metadata

Engine Version: 1.0.0  
Spec Version: 1.2.0  
Structure Version: 1.2.0  
Schema Base Version: evt@1.0  
Save Schema Version: save@1.0  
Last Updated: 2026-02-22  
Status: Active

參考專案啟動設定： 

---

## 0. 目標與非目標

### 0.1 目標

* 建立可重用的 Text-Based RPG 引擎 v1，內容（怪物/道具/任務/對話/地城事件）全部外部化為 JSON。
* 以「跨模組統一 Event Schema」作為觸發、流程、戰鬥、掉落、旗標（Flag）與存檔的唯一協議。
* 模組化：降低耦合、明確責任邊界、可擴充（後續可轉向 Survival/末日模式）。

### 0.2 非目標（v1 不做）

* 進階腳本語言（自訂 DSL / Lua）。
* 複雜地圖導航（網格、路徑尋路、視野遮蔽）。
* 多人/網路。
* 完整工具鏈（地城編輯器/可視化編輯器）。

---

## 1. 架構總覽

### 1.1 引擎層（Engine Layer）

* 只負責：讀取資料、執行規則、派發事件、維護狀態、存讀檔、與 UI 互動。
* 不負責：定義劇情、硬寫關卡、硬寫任務判斷、硬寫旗標名稱。

### 1.2 內容層（Content Layer, JSON）

* 定義：地城節點/事件池、怪物、掉落表、道具、商店、任務、對話、合成配方、職業與技能（v1 可先佔位）。
* 內容變更不得要求改引擎程式碼（除非新增 Event/Effect type）。

---

## 2. 跨模組共通 Event Schema（可擴充）

> 本章定義「事件訊息」與「效果（Effect）」格式。
> 事件：描述「發生了什麼」；效果：描述「狀態怎麼變」。
> Event Dispatcher 只認 Event Schema；各模組以 Effect 實作行為。

### 2.1 Event Envelope（事件信封）

```json
{
  "schema": "evt@1.0",
  "id": "evt.dungeon.node_enter",
  "ver": 1,
  "ts": 0,
  "source": { "module": "dungeon", "entity_id": "dungeon.forest_01", "node_id": "n12" },
  "actor": { "entity_id": "player", "party_id": "party.main" },
  "scope": { "run_id": "run.20260221.0001", "scene": "dungeon", "map_id": "forest_01" },
  "tags": ["step", "explore"],
  "payload": {},
  "ctx": { "seed": 123456, "debug": false },
  "trace": { "parent_event_id": null, "chain": [] }
}
```

#### 欄位規範

* `schema`：事件格式版本（固定字串），v1 為 `evt@1.0`
* `id`：事件種類 ID（字串，具命名規則，見 2.4）
* `ver`：事件種類的版本（整數；同一 `id` 升級時遞增）
* `ts`：引擎時間戳（整數；毫秒或 tick，v1 可用 tick）
* `source`：事件來源（模組名、相關 entity/node）
* `actor`：主要行為者（玩家/怪物/NPC）
* `scope`：事件作用域（本次 run、場景、地圖）
* `tags`：輔助分類（用於 UI、記錄、debug、filter）
* `payload`：事件資料（事件種類自定，但需符合其 schema）
* `ctx`：執行上下文（seed、難度、debug 等）
* `trace`：事件鏈追蹤（用於 log/回放/除錯）

### 2.2 Payload Pattern（事件負載模式）

* 事件 `payload` **只能**包含：

  * 基本型別（string/number/bool/null）
  * 陣列（元素為基本型別或 object）
  * object（不得含函式/程式碼）
* 禁止在 payload 放 UI 文字排版規則；文字內容必須走 `TextKey`（見 7.2）。

### 2.3 Effect Schema（統一效果格式）

> Effect 是 Dispatcher 分發後的「引擎可執行指令」。
> 同一事件可產生多個 effects（例如：扣血 + 掉落 + 旗標寫入 + 彈對話）。

```json
{
  "type": "stat.modify",
  "target": { "entity_id": "player" },
  "params": { "stat": "hp", "op": "add", "value": -12 },
  "meta": { "reason": "damage", "source_event_id": "evt.battle.hit" }
}
```

### Compare Operator Convention（op）

在條件判斷或比較運算中，`op` 統一使用代碼：
`eq | gt | gte | lt | lte`（禁止使用 >= <= 等符號），以維持資料層一致性與可驗證性。

#### Effect 通用欄位

* `type`：效果類型（命名規則見 2.4）
* `target`：目標（entity_id / party_id / inventory / world）
* `params`：效果參數（依 type 定義）
* `meta`：記錄用途，不參與邏輯（log/debug）

#### v1 需支援的 Effect Types（最小集合）

* `flag.set` / `flag.unset` / `flag.toggle`
* `flag.add_int`（整數累加，用於計數器）
* `stat.modify`（HP/MP/ATK/DEF/AGI 等）
* `inventory.add` / `inventory.remove`
* `gold.add`
* `battle.start`（切換到 battle 模組）
* `battle.end`（勝/敗/逃、回傳結果）
* `loot.roll`（掉落擲骰，產生 inventory.add）
* `quest.accept` / `quest.progress_add` / `quest.complete`
* `ui.message`（顯示訊息）
* `ui.choice`（顯示選項並回傳玩家選擇）
* `scene.change`（探索↔戰鬥↔城鎮設施）

### 2.4 命名規則（Event ID / Effect Type）

* Event ID：`evt.<domain>.<action>[.<detail>]`

  * 例：`evt.dungeon.step`, `evt.dungeon.node_enter`, `evt.battle.turn_start`
* Effect Type：`<domain>.<action>`

  * 例：`flag.set`, `inventory.add`, `battle.start`

### 2.5 事件與效果的擴充機制

* **新增事件種類**：只要定義 `id` + `ver` + payload schema 文件（本規格附錄或 /schemas），引擎 Dispatcher 不需改動；**事件產生哪些 effects** 由對應模組或 Rule Engine 決定。
* **新增 effect type**：需要在 `EffectExecutor` 註冊處增加 handler（程式碼改動點集中、可測）。

---

## 3. v1 引擎規格（完整）

### 3.1 核心遊戲循環（Core Loop）

1. 載入存檔 / 新遊戲初始化（state + flags + inventory + quests）。
2. 進入場景（dungeon / town / facility）。
3. 玩家操作（前進/後退/離開/互動）→ 產生 Event。
4. Dispatcher 收到 Event → 交給對應模組處理 → 產生 Effects。
5. EffectExecutor 依序套用 Effects → 更新 GameState。
6. UI 根據 state + ui effects 渲染；必要時等待玩家 choice。
7. 重複直到結束條件（死亡、通關、退出）。

### 3.2 狀態模型（GameState）

#### 3.2.1 必備狀態

* `player`：屬性（hp/mp/atk/def/agi/level/exp）、職業（v1 可先固定）
* `inventory`：物品堆疊（item_id, qty）
* `gold`
* `flags`：鍵值儲存（bool/int/string，v1 先限定 bool/int）
* `quests`：接受中/完成/進度計數
* `world`：目前地圖/地城節點指標、步數、難度、seed
* `battle`：戰鬥暫態（若在戰鬥中）

#### 3.2.2 存檔規範

* 存檔檔案：`save/<slot>.json`
* 必含：`save_schema: "save@1.0"`, `engine_version`, `content_manifest_hash`, `state`
* v1 需提供：向後相容（舊存檔可讀），必要時做 migration（見 6.3）。

### 3.3 模組清單（v1 必備）

* `Core`：GameState、主迴圈、時間、亂數、logger
* `ContentLoader`：讀取 JSON、驗證 schema、生成 manifest
* `EventDispatcher`：路由 Event → Module Handler
* `EffectExecutor`：執行 Effects（唯一能改 GameState 的通道）
* `Movement`：直線前進/後退/離開；每 step 觸發 encounter/event pool
* `Dungeon`：步進節點、事件池抽取、節點進出
* `Battle`：回合制、敏捷排序、技能/普攻、勝敗結算（v1 可先普攻）
* `Inventory & Items`：物品增減、使用消耗品、裝備（v1 裝備可先佔位）
* `Economy`：金幣、商店價格、掉落平衡（v1 最小：gold + shop buy）
* `Quest & Guild`：任務接取、進度累加、完成領獎（v1 最小：擊殺計數）
* `Progress & Flag`：旗標讀寫、條件判斷 API（規則集中）
* `UI (Pygame)`：前視角呈現、對話框、選項、資訊面板

### 3.4 事件路由（Dispatcher 規則）

* Dispatcher 以 `event.id` 前綴路由：

  * `evt.movement.*` → Movement
  * `evt.dungeon.*` → Dungeon
  * `evt.battle.*` → Battle
  * `evt.quest.*` → Quest
  * `evt.ui.*` → UI
* 允許「跨模組訂閱」：例如 Quest 模組可訂閱 `evt.battle.end` 以更新擊殺進度，但不得直接修改 state（只能產生 effects）。

### 3.5 回合戰鬥（v1 最小規格）

* 行動順序：依 AGI 由高到低（同值依 seed tie-break）。
* 行動類型（v1）：

  * `attack`（普攻）
  * `item_use`（消耗品）
  * `escape`（逃跑，成功率可先固定）
* 戰鬥結果 `BattleResult` 回傳到 `evt.battle.end.payload`：

```json
{
  "outcome": "win|lose|escape",
  "kills": [{"monster_id":"m.slime","count":2}],
  "exp": 12,
  "gold": 8,
  "drops": [{"item_id":"mat.slime_gel","qty":1}]
}
```

* 結算必轉為 Effects（加經驗、加金幣、掉落、旗標、任務進度）。

---

## 4. 模組責任邊界（誰能改什麼）

### 4.1 唯一改狀態原則（Single Writer Rule）

* **只有 `EffectExecutor` 可直接修改 `GameState`**。
* 任何模組不得直接寫 state；必須回傳 Effects。

### 4.2 模組權限矩陣（摘要）

* `ContentLoader`：可讀檔、產生 content objects；不得改 state。
* `Dispatcher`：可路由事件；不得改 state。
* `Movement/Dungeon/Battle/Quest/Economy/Inventory`：

  * 可：讀 state、讀 content、產生 events/effects
  * 不可：直接寫 state、直接做 UI I/O（只能 `ui.*` effects）
* `UI`：

  * 可：渲染、收集玩家輸入、產生 `evt.ui.choice_result` 等事件
  * 不可：直接改 state、不可解讀劇情邏輯（只顯示內容層給的 TextKey）
* `Progress&Flag`：

  * 可：提供條件判斷與 flag 操作 helper（但實際寫入仍透過 effects）
  * 不可：私自新增旗標（旗標必須出現在 manifest/flag registry）

### 4.3 跨模組互動約束

* 模組之間不得直接呼叫彼此內部方法（除非是穩定介面，如 `RuleAPI.evaluate(condition)`）。
* 共享只透過：

  1. Event（輸入）
  2. Effects（輸出）
  3. 只讀 Content（資料）
  4. 只讀 State（查詢）

---

## 5. Flag 命名規則

### 5.1 Flag Key 格式

`flg.<domain>.<subdomain>.<name>[@<scope>]`

* `domain`：`story|quest|dungeon|npc|system|battle|economy`
* `subdomain`：模組或地點/角色/任務群組
* `name`：snake_case，語意明確
* `scope`（可選）：`global|run|map:<id>|npc:<id>|quest:<id>`

#### 範例

* `flg.story.prologue.finished@global`
* `flg.quest.guild.rank_e.unlocked@global`
* `flg.dungeon.forest_01.boss_defeated@map:forest_01`
* `flg.npc.village_chief.met@npc:n.village_chief`
* `flg.system.tutorial.movement_shown@global`

### 5.2 Flag 型別（v1）

* `bool`：事件門檻、一次性觸發
* `int`：計數器（擊殺數、步數、訪問次數）
* v1 不建議 string；若要用，需在 registry 宣告與測試覆蓋。

### 5.3 禁止事項

* 禁止臨時在程式碼中硬塞新 flag key。
* 禁止用含糊名：`flg.tmp.*`, `flg.test.*`（除非在 dev profile 下）。

---

## 6. 版本管理方式（Event / Flag / Content）

### 6.1 引擎版本（Engine SemVer）

* `engine_version`: `MAJOR.MINOR.PATCH`

  * MAJOR：破壞性改動（事件/存檔/效果不相容）
  * MINOR：新增向後相容功能（新 effect type、新事件）
  * PATCH：修 bug，不改 schema

### 6.2 Event Schema 版本策略

* 全域 schema：`evt@1.0`
* 事件種類版本：`event.ver`（同一 `event.id` 的 payload 欄位變更時 +1）
* 兼容原則：

  * **新增欄位**：允許（需提供 default）
  * **刪除/改名欄位**：須提高 `evt@` 或提高 `event.ver` 並做 migration adapter

### 6.3 Save Migration

* `save_schema` 與 `engine_version` 必填
* 引擎提供 `migrations/`：

  * `save@1.0 -> save@1.1` 的轉換函式
* 若 content 更新導致旗標/道具 id 改名：

  * 必須提供 `id_aliases`（見 7.4）避免存檔報廢。

### 6.4 Flag Registry（旗標登記與審核）

* 建議檔：`content/flags.registry.json`

```json
{
  "schema": "flags@1.0",
  "flags": [
    {"key":"flg.dungeon.forest_01.boss_defeated@map:forest_01","type":"bool","default":false,"owner":"dungeon"},
    {"key":"flg.quest.guild.slime_hunt.count@quest:q.slime_hunt","type":"int","default":0,"owner":"quest"}
  ]
}
```

* 引擎啟動時驗證：

  * 所有被引用的 flag 必須存在 registry（靜態掃描 content 或由 manifest 提供）。
  * 未登記旗標禁止寫入（dev 模式可警告，release 模式視為錯誤）。

---


## 6.5 Condition（條件判斷）

* Condition 為純判斷層（不改 state、不產生 effects）。
* Schema：`02_specs/schema/condition.schema.json`（`cond@1.0`）。
* 用途：任務/怪物出現/地城事件/對話分支等條件判斷統一描述。

## 7.0 Content Schemas（內容層 Schema）

* Monster Schema：`02_specs/schema/monster.schema.json`（`monster@1.0`），ID 前綴建議 `m.`。
* Item/Quest Schema 將依相同原則逐步補齊。

## 7. 內容資料規格（v1 範圍）

### 7.1 Content Manifest

* 引擎啟動讀取 `content/manifest.json`
* 必含：

  * `content_version`
  * `hash`（可用檔案列表 hash）
  * `paths`（monsters/items/quests/dungeons/dialogues/flags）
  * `id_aliases`（可選）

### 7.2 TextKey（文字資源鍵）

* UI 顯示文字不要直接硬寫在事件/效果；用 `txt.<domain>.<key>`
* 例：`txt.npc.village_chief.greeting_01`
* 實際字串位於 `content/texts/zh-TW.json`

### 7.3 Dungeon（步進 + 事件池）

* 最小資料：

  * `dungeon_id`
  * `nodes`（線性序列或簡單分叉，v1 建議線性）
  * `event_pool`（節點可配置權重抽取）
  * `encounter_table`（怪物群組與權重）

### 7.4 ID Aliases（避免改名毀存檔）

```json
{
  "schema":"aliases@1.0",
  "items": [{"from":"item.slimegel","to":"mat.slime_gel"}],
  "flags": [{"from":"flg.dungeon.forest.boss_dead@global","to":"flg.dungeon.forest_01.boss_defeated@map:forest_01"}]
}
```

---

## 8. 測試與驗證（v1 必做）

* Schema 驗證：

  * manifest、monsters、items、quests、dungeons、flags registry
* 事件回放測試（最小）：

  * 固定 seed 的 run，事件序列應可重現（同樣輸入 → 同樣輸出）
* 破壞性變更檢查：

  * 未登記 flag 寫入 → fail
  * 未註冊 effect type → fail
  * content id 變更無 alias → warn/fail（依模式）

---

## 9. 附錄：v1 標準事件清單（建議最小集合）

### 探索/移動

* `evt.movement.step`：payload `{ "dir":"forward|back" }`
* `evt.dungeon.node_enter`：payload `{ "node_id":"n12" }`
* `evt.dungeon.encounter_roll`：payload `{ "table_id":"enc.forest_01" }`

### 戰鬥

* `evt.battle.start`：payload `{ "encounter_id":"enc..." }`
* `evt.battle.turn_start`：payload `{ "turn":1 }`
* `evt.battle.action_selected`：payload `{ "action":"attack|item_use|escape", "target":"..." }`
* `evt.battle.end`：payload（見 3.5）

### 任務

* `evt.quest.accept`：payload `{ "quest_id":"q.slime_hunt" }`
* `evt.quest.progress`：payload `{ "quest_id":"q.slime_hunt", "delta":1, "kind":"kill", "target_id":"m.slime" }`
* `evt.quest.complete`：payload `{ "quest_id":"q.slime_hunt" }`

### UI

* `evt.ui.choice_result`：payload `{ "choice_id":"c001", "selected":"opt_2" }`

---

以上文件可直接作為 v1 引擎的「唯一規格來源」。若你下一步要進入落地實作，我可以在同一套規格下，補齊：

* `content/` 目錄結構與各 JSON schema 範本
* Dispatcher / EffectExecutor 的介面定義（Python typing）
* 最小可跑的「探索→遭遇→戰鬥→結算→任務進度」端到端流程樣板
