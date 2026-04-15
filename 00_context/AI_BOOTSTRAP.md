# =========================================================
# 🔒 CURRENT PROJECT SNAPSHOT (AI MUST READ FIRST)
# =========================================================

Source of Truth:
- Version & State → PROJECT_STATE.json
- Structure → PROJECT_STRUCTURE.md
- Decisions → design_decision_log.md

⚠️ This snapshot is a HUMAN-READABLE MIRROR only.
⚠️ If any conflict occurs, PROJECT_STATE.json ALWAYS takes precedence.

---

## Current State (Derived from PROJECT_STATE.json)

Engine Version: 1.0.0  
Spec Version: 1.3.0  
Structure Version: 1.2.0  

Governance Mode: Lock + Controlled Evolution  
Evolution Mode: CLOSED

Current Phase:
Phase D.3 Complete – Effect DSL Governance Established

---

## Verified Runtime Scope (Behavior Gate Confirmed)

### CLI MVL Loop
- interactive loop enabled
- load → list → accept → progress → check → complete → save → reload
- where / locations / move (location control)

---

### Condition System
- flag.is_true / flag.is_false
- flag.int_compare (eq / gt / gte / lt / lte)
- logical AND (nested conditions)
- inventory.has

---

### Quest System
- accept_condition evaluation
- complete_condition evaluation
- rewards.effects dispatch
- active quest guard
- completed_ids tracking

---

### Runtime Context 
- session-scoped current_location (mirror of game_state)
- valid locations:
  - start_village
  - forest_edge
  - town_gate
- CLI-driven location control

---

### Location Gating
- quest completion gate (engine-side overlay)
- wrong location blocks completion
- correct location allows completion
- persistent location via save.game_state.current_location

---

### State Integrity
- save.game_state = { flags, inventory, vars, current_location } (SSOT)
- runtime_context mirrors persistent state (Single Writer Rule)
- backward compatibility preserved (load-time normalization)

---

## Structural Constraints (HARD RULES)

- ❌ No structure changes
- ❌ No loader modification
- ❌ No new top-level governance files
- ❌ No registry mutation outside append-only

- ⚠️ Schema evolution allowed ONLY via Evolution Mode (already used in D.2)

- ✅ All changes must remain within existing structure
- ✅ All structural evolution must go through DD + Evolution Mode

---

## 🚧 D.4 Evolution Direction (Pre-Activation)

DO NOT IMPLEMENT YET

D.4 will focus on:

1. Engine Naming Alignment (flag.int_add → flag.add_int)
2. var.add Contract Decision (DSL vs Engine-only)
3. Registry → Schema Sync (SSOT automation)
4. Effect Coverage Expansion

## AI Collaboration Rules (Quick Mode)

When AI joins this project, it MUST:

1. Read this snapshot first
2. Treat PROJECT_STATE.json as:
   - Version authority
   - Phase authority
   - Capability authority
3. Treat PROJECT_STRUCTURE.md as structure SSOT
4. Treat design_decision_log.md as evolution history
5. Refuse any action that violates governance constraints

## 🧠 EFFECT DSL GOVERNANCE (DD-020)

### 1. Canonical Naming

* ✅ flag.add_int → ONLY valid DSL naming
* ❌ flag.int_add → forbidden in content (Naming Drift)

---

### 2. Contract Boundary

* 🚫 var.add → Engine-only capability
* ❌ Forbidden in 03_data

Rule:

> Content must ONLY use schema-defined DSL

---

### 3. Coverage Validation

Effect DSL must pass:

* Schema Coverage
* Behavior Coverage

Only **Fully Covered** effects are allowed in content.

---

### 4. Verified DSL (Fully Covered)

```md
gold.add
flag.set
flag.add_int
inventory.add
inventory.remove
```

---

### 5. Forbidden / Blocked DSL

```md
flag.int_add   → Naming Drift
var.add        → Contract Violation
```

---

### 6. Gate Enforcement Rules

* ❌ Non-canonical DSL → BLOCK
* ❌ Engine-only DSL → BLOCK
* ❌ Not Covered DSL → BLOCK

````

---

## 🚧 D.4 Evolution Direction (Pre-Activation)

```md
DO NOT IMPLEMENT YET

D.4 will focus on:

1. Engine Naming Alignment (flag.int_add → flag.add_int)
2. var.add Contract Decision (DSL vs Engine-only)
3. Registry → Schema Sync (SSOT automation)
4. Effect Coverage Expansion
````

---

## ⚠️ AI HARD CONSTRAINTS

```md
- DO NOT modify schema (02_specs)
- DO NOT modify structure
- DO NOT introduce new DSL
- DO NOT allow var.add in content
- DO NOT allow flag.int_add in content

All contract changes require:
→ DD + Evolution Mode
```

---


# =========================================================
# END OF SNAPSHOT — BELOW IS FULL GOVERNANCE CONTRACT
# =========================================================

# AI_BOOTSTRAP.md

Project_RPG – AI Collaboration Initialization Protocol

---

## 1. Purpose

This document defines the official collaboration contract between this project and any AI model (ChatGPT, Gemini, Claude, etc.).

Its purpose is to:

- Prevent Architecture Drift
- Maintain Single Source of Truth (SSOT)
- Ensure schema alignment
- Guarantee version consistency
- Enforce governance rules

Any AI generating specifications, code, schema, or structural suggestions must comply with this document.

---

## 2. Official Project Structure (SSOT)

The following directory structure is the ONLY valid structure.

AI is NOT allowed to:

- Propose restructuring directory hierarchy
- Introduce new top-level folders
- Move schema outside 02_specs/schema
- Split engine_contract.md unless approved via Decision Log

---

## 3. Governance Documents (Must Be Read Before Generation)

Before generating any structural or specification changes, AI must acknowledge:

- PROJECT_STRUCTURE.md (if exists)
- design_decision_log.md
- 02_specs/engine_contract.md
- Current Engine Version

If generation conflicts with these documents, AI must:

> Refuse generation and explain the inconsistency.

---

## 4. Version Anchoring

Version Source of Truth:
See `PROJECT_STATE.json` for:

- engine_version
- spec_version
- structure_version

All generated content must explicitly declare which versions (from PROJECT_STATE.json) it targets.

If version mismatch is detected between generated content and PROJECT_STATE.json,
AI must request clarification before proceeding.

## 5. Folder Responsibility Rules

Layer separation must be respected:

- 01_design_docs → conceptual design only
- 02_specs → technical contracts and schemas
- 03_data → pure JSON game data
- 05_engine → Python implementation only

No cross-layer mixing is allowed.

---

## 6. Schema Discipline

Rules:

- Schema files must follow naming pattern: `*.schema.json`
- No "final2", "v3_fixed", etc.
- Flag naming: snake_case only
- All flags must exist in registry
- Runtime MVL may treat missing `$schema` in fixtures as non-fatal warning,
  provided Schema Gate (MVL validation tools) passes successfully.

---

### 6.1 Behavior Gate Debugging (Non-Structural)

CLI 允許提供「摘要 + 關鍵值預覽」以提升除錯效率（例如 questdump 顯示 complete_condition.type/params 與 rewards.effects 摘要）。
此類輸出改動不得改變資料結構、不得引入新資料夾、不得改寫 schema 契約。

Condition 評估層必須採遞迴 + leaf handler dispatch（例如 and/or/not → recurse；flag.int_compare / inventory.has → leaf handlers），不得將「底層條件」寫死為單一類型。

### 6.2 Runtime Context Extension (Non-Schema)

Engine may introduce session-scoped runtime context for behavior validation,
provided that:

- no schema is modified
- no content JSON contract is changed
- no loader behavior is changed
- runtime context remains engine-local

Examples:
- current_location
- CLI session context
- engine-side action gating overlays

Location-based gating may be implemented as engine-side logic
before any formal schema evolution is approved.

## 7. AI Behavioral Rules

AI must:

- Optimize within existing structure
- Not propose structural redesign unless explicitly requested
- Avoid generating duplicate structure patterns
- Ask for version confirmation when uncertain
- Prefer incremental refinement over refactoring

---

## 8. When Structural Change Is Required

Structural change must follow:

1. Propose change
2. Justify reason
3. Evaluate impact
4. Add new Design Decision (DD-XXX)
5. Update PROJECT_STRUCTURE.md

No silent structural evolution allowed.

---

## 9. Deterministic Collaboration Rule

If identical input and version are given, output structure should remain consistent.

If AI produces different structure for same input,
it must acknowledge deviation.

---

## 10. Final Rule

This project values:

Consistency > Elegance  
Governance > Creativity  
Stability > Rapid Iteration

AI must operate within these constraints.

---

## 11. Architecture Evolution Protocol (Controlled Evolution Mode)

This project supports controlled architectural evolution.

Evolution is allowed only under the following protocol.

### 11.1 When Evolution Mode May Be Activated

Evolution Mode can be entered when:

- A new core schema is required (e.g., Condition.schema.json)
- Existing schema cannot express required game logic
- Core dependency structure must change
- Structure Version needs bumping
- A new module is introduced at Engine Layer

Routine content expansion (monsters, items, quests) does NOT require Evolution Mode.

---

### 11.2 Evolution Procedure (Mandatory Steps)

When entering Evolution Mode:

1. Explicitly declare:
   `Entering Evolution Mode (Structure Version X → X+1)`

2. Provide:
   - Dependency impact analysis
   - Circular dependency check
   - Governance compliance review

3. Update:
   - design_decision_log.md (New DD entry)
   - PROJECT_STRUCTURE.md (if folder changes)
   - Structure Version (if affected)

4. Confirm:
   - No SSOT violation
   - No cross-layer contamination

5. Explicitly declare:
   `Exiting Evolution Mode`

No structural change may occur without completing this sequence.

---

### 11.3 Evolution Constraints

Even in Evolution Mode, the following remain prohibited:

- Silent folder restructuring
- Breaking common.schema without version bump
- Introducing circular schema dependencies
- Mixing 03_data and 02_specs responsibilities
- Bypassing Flag Registry governance

---

### 11.4 Versioning Rules for Evolution

- Minor structural extension → Structure Version +0.1
- Breaking change → Structure Version +1.0
- Schema addition (non-breaking) → Spec Version +0.1
- Core contract modification → Engine Version +1.0

---

### 11.5 Deterministic Output Rule (Evolution Mode)

If Evolution Mode is active, AI must restate:

- Current Engine Version
- Current Spec Version
- Current Structure Version

before proposing structural changes.

---

### 12. Naming Integrity Rule

Schema 檔名必須與 `$id` 與語意一致。
不得出現 effect/event 等語意與檔名互換情形。
若發現語意錯置，需透過 DD 流程修正並重新執行 MVL。

---

End of AI_BOOTSTRAP.md
