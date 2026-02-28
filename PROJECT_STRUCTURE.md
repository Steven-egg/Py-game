## DD-004
Date: 2026-02-21  
Title: 資料夾預計 JSON Schema 資料生成結構（Structure SSOT 凍結）

Project_RPG/
│
├── 00_context/
│   ├── AI_BOOTSTRAP.md
│   ├── PROJECT_STATE.json
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
│   │   ├── common.schema.json
│   │   ├── event.schema.json
│   │   ├── effect.schema.json
│   │   ├── condition.schema.json
│   │   ├── flags.registry.schema.json
│   │   ├── content_manifest.schema.json
│   │   ├── save.schema.json
│   │   ├── monster.schema.json
│   │   ├── item.schema.json
│   │   └── quest.schema.json
│   │
│   ├── engine_contract.md
│   └── mvl_protocol.md
│
├── 03_data/
│   ├── monsters/
│   ├── items/
│   ├── quests/
│   ├── dungeons/
│   ├── events/
│   ├── dialogues/
│   └── registries/
│
├── 04_assets/
│   ├── backgrounds/
│   ├── characters/
│   ├── monsters/
│   ├── ui/
│   └── audio/
│
├── 05_engine/
│   ├── cli_mvl.py
│   ├── content_loader.py
│   ├── quest_runtime.py
│   ├── effect_executor.py
│   ├── save_manager.py
│   ├── validation/
│   └── save/
│
└── tools/
    └── add_schema_uri.py


Impact: High  
Scope: 專案整體資料夾結構、未來所有 AI 對話初始化流程、JSON 生成與規格書對齊機制  

Reason:
這是首次發現多對話產生架構漂移（Architecture Drift）的問題。  
為避免未來在不同 AI 對話中產生多版本資料夾結構與規格不一致情況，  
正式定義本專案的官方目錄標準，作為 Single Source of Truth (SSOT)。  

未來任何新增對話或大型規格生成，  
必須以此結構為依據，不得自行重構目錄層級。  

---


### Evolution Note

本目錄結構為 Structure SSOT。  

即使進入 Evolution Mode，  
也不得新增頂層資料夾或重構層級，  

除非：  
- 有新的 Design Decision (DD-XXX)  
- 並同步更新 Structure Version  

Evolution 僅允許在既有層級下新增 schema、模組或資料內容。