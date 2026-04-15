## 🔒 CURRENT PROJECT SNAPSHOT (EXCERPT)

Engine Version: 1.0.0
Spec Version: 1.3.0
Structure Version: 1.2.0

Governance Mode: Lock + Controlled Evolution
Evolution Mode: CLOSED

Current Phase:
Phase D.3 Complete – Effect DSL Governance Established


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

## 🚧 D.4 Evolution Direction (Pre-Activation)

DO NOT IMPLEMENT YET

D.4 will focus on:

1. Engine Naming Alignment (flag.int_add → flag.add_int)
2. var.add Contract Decision (DSL vs Engine-only)
3. Registry → Schema Sync (SSOT automation)
4. Effect Coverage Expansion

---

## ⚠️ AI HARD CONSTRAINTS

- DO NOT modify schema (02_specs)
- DO NOT modify structure
- DO NOT introduce new DSL
- DO NOT allow var.add in content
- DO NOT allow flag.int_add in content

All contract changes require:
→ DD + Evolution Mode

---
