# PROJECT STRUCTURE (SSOT)

This document defines the official directory structure of the project.

⚠️ This is the Structure Single Source of Truth (SSOT)  
⚠️ Any structure change MUST go through Design Decision (DD) process  

---

# 1. Structure Overview (Human + AI Readable)


Project_RPG/
│
├── 00_context/        ← Governance Layer (AI Control Tower)
├── 01_design_docs/    ← Conceptual Design Layer
├── 02_specs/          ← Technical Contract Layer
├── 03_data/           ← Content Data Layer (JSON only)
├── 04_assets/         ← Static Resources (images/audio/etc.)
├── 05_engine/         ← Runtime Implementation Layer (Python)
└── tools/             ← Utility Scripts


---

# 2. Layer Responsibilities (STRICT BOUNDARY)

## 00_context → Governance Layer

Purpose:

* AI collaboration control
* State anchoring
* Drift prevention

Contains:

* AI_BOOTSTRAP.md → governance contract
* PROJECT_STATE.json → version/state SSOT
* PROJECT_STATE_SNAPSHOT.md → AI-readable mirror
* Other context/control files

Rules:

* No runtime logic
* No schema definitions
* No game content

---

## 01_design_docs → Conceptual Design

Purpose:

* System ideas and design thinking
* Not executable
* Not enforced by engine

Examples:

* battle_system.txt
* dungeon_system.txt
* movement_system.txt

Rules:

* No JSON schema
* No runtime dependency

---

## 02_specs → Technical Contracts

Purpose:

* Define ALL system rules
* Schema + engine contract

Structure:

02_specs/
├── schema/
│   ├── *.schema.json
│
├── engine_contract.md
└── mvl_protocol.md


Rules:

* All schema MUST live here
* No duplication across folders
* No data content allowed

---

## 03_data → Content Layer (JSON ONLY)

Purpose:

* Game content
* Must conform to schema

Structure:

03_data/
├── monsters/
├── items/
├── quests/
├── dungeons/
├── events/
├── dialogues/
└── registries/  <-- (DD-022 新增)

registries:
- cross-entity mapping layer
- used for DSL / effect / future schema alignment


Rules:

* JSON only
* No logic
* No Python
* Must pass MVL validation

---

## 04_assets → Static Resources

Purpose:

* Non-logic files

Examples:

* images
* UI assets
* audio

Rules:

* No JSON logic
* No schema

---

## 05_engine → Runtime Layer

Purpose:

* Execute system behavior

Structure:

05_engine/
├── cli_mvl.py
├── content_loader.py
├── quest_runtime.py
├── effect_executor.py
├── save_manager.py
├── validation/
└── save/


Rules:

* Python only
* No content definition
* No schema definition

---

## tools → Utilities

Purpose:

* Development support scripts

Examples:

* schema tools
* conversion scripts

---

# 3. AI Structure Reading Protocol (CRITICAL)

When AI evaluates project structure:

### Step 1

Read THIS file as Structure SSOT

### Step 2

DO NOT rely on:

* tree /f output
* raw filesystem dumps

### Step 3

If structure conflict occurs:

* THIS file takes precedence

---

# 4. Allowed vs Forbidden Actions

## Allowed

* Add files inside existing folders
* Extend schema inside 02_specs/schema
* Add JSON content inside 03_data

---

## Forbidden (Without DD Process)

* Add new top-level folders
* Move schema outside 02_specs
* Mix data into engine layer
* Introduce cross-layer dependency

---

# 5. Structure Change Protocol

If structure change is needed:

1. Propose change
2. Justify reason
3. Impact analysis
4. Create Design Decision (DD-XXX)
5. Update this document

---

# 6. Drift Prevention Rules (AI ENFORCED)

AI must REFUSE if:

* New folder is introduced without DD
* Schema is placed outside 02_specs
* Data appears outside 03_data
* Engine writes content directly

---

# 7. Relationship to Other SSOT Files

| Domain     | Source of Truth           |
| ---------- | ------------------------- |
| Structure  | PROJECT_STRUCTURE.md      |
| State      | PROJECT_STATE.json        |
| State (AI) | PROJECT_STATE_SNAPSHOT.md |
| Governance | AI_BOOTSTRAP.md           |
| Evolution  | design_decision_log.md    |

---

# 8. Evolution Note

Structure is LOCKED under DD-004.

Evolution is allowed ONLY if:

* DD process is followed
* Structure version is updated
* No SSOT violation occurs

---

# END OF FILE

---
