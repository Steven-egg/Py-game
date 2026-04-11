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
Spec Version: 1.2.0  
Structure Version: 1.2.0  

Governance Mode: Lock + Controlled Evolution  

Current Phase:  
Phase C Complete – Main Quest Chain Validated

---

## Verified Runtime Scope (Behavior Gate Confirmed)

- CLI MVL loop: PASS (load → accept → progress → complete → save)

- Condition system:
  - flag.is_true / flag.is_false
  - flag.int_compare (eq/gt/gte/lt/lte)
  - logical AND (nested conditions)
  - inventory.has

- Quest system:
  - accept_condition evaluation
  - complete_condition evaluation
  - rewards.effects dispatch
  - active quest guard
  - completed_ids tracking

- State integrity:
  - save.game_state = SSOT confirmed
  - backward compatibility preserved

---

## Structural Constraints (HARD RULES)

- ❌ No schema changes
- ❌ No structure changes
- ❌ No loader modification
- ❌ No new top-level governance files
- ❌ No registry mutation outside append-only

- ✅ All changes must remain within existing structure
- ✅ All structural evolution must go through DD + Evolution Mode

---

## Current Focus (Next Targets from PROJECT_STATE.json)

- Define Phase D scope (World / Location context layer)
- Implement minimal location context at CLI level (no schema changes)
- Introduce context-aware action gating (location-based constraints)
- Evaluate need for future schema evolution (map / world / entity layer)
- Decide quest repeatability semantics (one-shot vs repeatable)

---

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
