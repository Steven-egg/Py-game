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
Spec Version: 1.4.0  
Structure Version: 1.2.0  

Governance Mode: Evolution Active  
Evolution Mode: ACTIVE

Current Phase:
Phase D.4 Active – Registry Schema Evolution

---

## Registry Status (D.4 Critical Context)

- registry is introduced as schema-aligned mapping layer
- registry is integrated into validation pipeline (REG-002 completed)
- registry is NOT used in runtime
- registry is NOT DSL authority
- registry is NOT part of content_manifest
- registry fixture is allowed for validation only

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
- ❌ No registry usage in runtime

- ⚠️ Schema evolution allowed ONLY via Evolution Mode (ACTIVE)

- ✅ registry allowed ONLY in:
  - 02_specs/schema (schema)
  - 03_data/registries (data)
  - validation layer (MVL)

---

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


gold.add
flag.set
flag.add_int
inventory.add
inventory.remove


---

### 5. Forbidden / Blocked DSL


flag.int_add   → Naming Drift
var.add        → Contract Violation


---

### 6. Gate Enforcement Rules

* ❌ Non-canonical DSL → BLOCK
* ❌ Engine-only DSL → BLOCK
* ❌ Not Covered DSL → BLOCK

---

## 🚧 D.4 Evolution Scope (ACTIVE)

D.4 allows ONLY:

1. registry schema contract
2. registry validation integration
3. registry data migration (REG-003)
4. DSL alignment preparation

---

## ❗ D.4 Forbidden Scope

* ❌ registry → runtime integration
* ❌ registry → DSL authority
* ❌ schema modification (existing contracts)
* ❌ engine behavior change

---

## ⚠️ AI HARD CONSTRAINTS


- DO NOT modify schema (02_specs)
- DO NOT modify structure
- DO NOT introduce new DSL
- DO NOT allow var.add in content
- DO NOT allow flag.int_add in content
- DO NOT use registry in runtime

All contract changes require:
→ DD + Evolution Mode


---

# =========================================================

# END OF SNAPSHOT — BELOW IS FULL GOVERNANCE CONTRACT

# =========================================================
