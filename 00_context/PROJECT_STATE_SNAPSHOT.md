# PROJECT STATE SNAPSHOT

⚠️ This document is a HUMAN-READABLE MIRROR of PROJECT_STATE.json  
⚠️ It is NOT the Source of Truth  
⚠️ In case of any mismatch, PROJECT_STATE.json ALWAYS takes precedence  

---

## AI Quick Context (Startup Summary)

Phase: D.3 Complete  
Spec: 1.3.0  
Structure: Locked (1.2.0)  
Governance Mode: Lock + Controlled Evolution  

Authority:
- State SSOT → PROJECT_STATE.json
- Structure SSOT → PROJECT_STRUCTURE.md

Core Governance:
- DD-020: Effect DSL Governance ACTIVE
- DD-021: AI Workflow Governance ACTIVE

Critical Constraints:
- ❌ flag.int_add forbidden in content
- ❌ var.add forbidden in content
- ❌ Production cannot modify DSL / Schema
- ❌ JIRA is NOT SSOT

System Status:
- Schema: Stable
- Engine: Stable
- Validation: PASS
- Evolution Mode: CLOSED (D.4 pending)

Next Focus:
 Phase D.4 preparation:
- registry–schema alignment
- DSL naming normalization
- coverage expansion

## Version Anchoring

Engine Version: 1.0.0  
Spec Version: 1.3.0  
Structure Version: 1.2.0  

Governance Mode: Lock + Controlled Evolution  
Structure Anchor: DD-004  

---

## Current Phase

Phase D.3 Complete – Effect DSL Governance Established

---

## Schema Layer Status

Completed:
- common
- condition
- effect
- event
- flags.registry
- content_manifest
- save
- monster
- item
- quest

In Progress:
- (none)

Planned:
- (none)

---

## Engine Capabilities (Verified)

### State Model
- save.game_state = { flags, inventory, vars, current_location } (SSOT)

---

### Effect Dispatcher
- gold.add ✅ (Fully Covered)
- flag.set ✅ (Fully Covered)
- flag.add_int ✅ (Canonical Naming)
- inventory.add ✅ (Fully Covered)
- inventory.remove ✅ (Fully Covered)

- flag.int_add ⚠️ (Non-canonical / Naming Drift – forbidden in content)
- var.add 🚫 (Engine-only / Contract Violation if used in content)

---

### Condition System
- flag.is_true
- flag.is_false
- flag.int_compare (eq / gt / gte / lt / lte)
- logical AND (nested conditions)
- inventory.has

---

### Quest Runtime
- accept_condition evaluation
- complete_condition evaluation
- rewards.effects dispatch
- active quest guard
- completed_ids tracking

---

### CLI MVL Loop
- interactive loop enabled
- load → list → accept → progress → check → complete → save → reload
- where / locations / move (location control)

---

### Runtime Context (Phase D.2)
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

## Validation Status

MVL Protocol Version: 1.0  

Schema Gate:
- monster: PASS
- item: PASS
- quest: PASS

Behavior Gate:
- status: PASS

Location Gate:
- status: PASS

Location Persistence:
- status: PASS

Last Validation Date:
- 2026-04-12

---

## Verified System Behavior

- Phase C fully completed (Effect Dispatcher + Quest Runtime)
- Main quest chain (002 → 005) validated via CLI MVL
- Condition system verified across all required patterns
- Behavior Gate stable for accept → progress → complete flow
- State SSOT integrity confirmed (all reads from save.game_state)
- Effect dispatch verified (gold.add / flag.set / inventory.add)
- Save system backward compatible (completed_ids introduced)
- CLI system stable (ACTIVE / DONE / READY / LOCKED states)
- Regression PASS (legacy effects stable)

### Phase D.1 Additions
- Runtime location context validated
- Interactive CLI loop validated
- Location-gated quest completion verified
- Wrong location blocks completion with explicit message
- Correct location allows completion when conditions met
- No schema changes introduced in Phase D.1
- No structure changes introduced in Phase D.1

### Phase D.2 Additions
- Location persistence integrated into save.game_state
- current_location added to save schema (Spec 1.3.0)
- CLI move / save / reload behavior validated across multiple cycles
- Runtime context now mirrors persistent location (Single Writer Rule)
- Save payload upgraded to new schema:
  - save_schema
  - engine_version
  - content_manifest_hash
  - active_quest
  - game_state
  - completed_ids
- Backward compatibility verified via load-time normalization
- No structure changes introduced in Phase D.2

---

## Next Targets

- Evaluate extending location gating to accept / event / action flows
- Assess need for formal world/location schema
- Evaluate adjacency / movement constraints (graph or rule-based)
- Define Phase D.4 scope (Registry–Schema sync / DSL alignment / coverage expansion)
- Run full MVL Protocol regression under Spec 1.3.0

---

## Governance Interpretation

Effect DSL Governance Charter (DD-020) is now active:

- Naming Authority → Schema defines canonical DSL
- Boundary Enforcement → Engine-only capabilities cannot enter content
- Coverage Validation → DSL must pass Schema + Behavior

Negative Constraints:

- ❌ flag.int_add forbidden in 03_data
- ❌ var.add forbidden in 03_data
- ❌ Uncovered effects cannot be marked as Ready

System State:

- Schema Layer → Stable (Spec 1.3.0)
- Structure → Locked (1.2.0)
- Engine → Stable (with internal drift isolated)
- Evolution Mode → CLOSED (D.4 pending activation)

---

## Usage Rule (For AI Systems)

When using this snapshot:

1. Always cross-check with PROJECT_STATE.json if precision is required
2. Do NOT infer structure evolution from this file
3. Treat this file as read-only reference for:
   - Phase understanding
   - Capability awareness
   - constraint enforcement
4. If governance state and code state diverge, PROJECT_STATE.json takes precedence
5. Do NOT treat this file as modification authority

---

## Governance Extensions (DD-020 / DD-021 Synced)

### Effect DSL Governance (DD-020)

- Canonical Naming Authority: schema-defined DSL (e.g. flag.add_int)
- Non-canonical forbidden: flag.int_add (blocked in content layer)
- Engine-only boundary:
  - var.add → NOT allowed in 03_data
- Coverage requirement:
  - Schema Coverage + Behavior Coverage (dual gate)
- Enforcement:
  - Negative enforcement (violation → block usage)

---

### AI Collaboration Workflow (DD-021)

#### Role Separation

- ChatGPT (Governance):
  - DSL / Blueprint / audit / task decomposition

- ChatGPT (Production):
  - code / JSON / debug
  - cannot modify DSL / Schema

- Gemini:
  - JIRA bridge only

- NotebookLM:
  - SSOT validator (drift detection)

---

#### Boundary Enforcement

- JIRA is NOT SSOT
- JIRA cannot store:
  - DSL
  - Schema
  - Audit / Gate logic

- Production cannot modify:
  - DSL
  - Schema

- Governance does not implement runtime

---

#### Workflow Pipeline

Governance → Task → JIRA → Production → Validation → Feedback

---

### System Interpretation Update

System is now governed by:

1. Effect DSL Governance (DD-020)
2. AI Workflow Governance (DD-021)

These rules are ACTIVE and enforced at:

- Content authoring
- DSL usage
- AI collaboration boundary

---

### State Consistency Note

If mismatch occurs:

- PROJECT_STATE.json remains the ONLY authority
- Snapshot must be regenerated to reflect latest governance