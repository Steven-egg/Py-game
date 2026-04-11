# 05_engine – MVL Runtime

This folder contains the executable MVL (Minimal Viable Loop) runtime used to validate:

- Quest flow correctness
- Condition evaluation (accept / complete)
- Effect dispatch behavior
- Save-state integrity (SSOT)
- CLI-driven inspection & debugging
- Phase D.1 runtime location context (NEW)

---

## Current Verified State

- Phase C: Core quest loop → PASS
- Phase D.1: Runtime location context & completion gate → PASS

This runtime is **NOT gameplay**, but a deterministic verification environment.

---

## Architecture Role

### State SSOT
- `save.game_state` is the single source of truth
  - flags
  - inventory
  - vars

All conditions and effects operate strictly on this state.

---

### Runtime Responsibilities

- Quest lifecycle:
  - accept → progress → check → complete → save

- Condition evaluation:
  - accept_condition
  - complete_condition
  - recursive condition schema

- Effect dispatch:
  - gold / flags / inventory / vars

- Save synchronization:
  - active_quest
  - completed_ids
  - game_state

---

### CLI = Debug Console

The CLI acts as:

- Quest lobby
- State inspector
- Behavior validation panel

---

## Quick Start (IMPORTANT)

### Launch interactive CLI

```bash
py cli_mvl.py --slot slot_1
```
## Available Commands

Inside the CLI session:

```text
help
load
list
accept <quest_id>

progress <kind> <key> [value]
  kind: item | kill | flag | var

check
complete

where
locations
move <location_id>

show
questdump <quest_id>

save
reload
exit
```
---

## MVL Loop (Core Flow)

### Step 1: Accept Quest

```text
accept <quest_id>
```

Guards:

* blocked if another quest is active
* blocked if already completed

---

### Step 2: Report Progress

```text
progress kill slime 5
progress flag flg.npc.met_guard true
```

Updates:

* quest progress (ActiveQuest)
* global game_state (SSOT)

---

### Step 3: Check Completion

```text
check
```
Evaluates:

1. complete_condition / objectives
2. (NEW) location gate

---

### Step 4: Complete Quest

```text
complete
```

On success:

* apply rewards.effects
* append to completed_ids
* clear active_quest

---

### Step 5: Inspect State

```text
show
```
---

## Quest Lobby (list)

```text
list
```
Displays:

* [DONE] → quest_id in completed_ids
* [ACTIVE] → current active quest
* [READY] → accept_condition satisfied
* [LOCKED] → accept_condition failed (with reason)

---

## Debugging Tools

### Quest Dump

```text
questdump <quest_id>
```

Shows:

* condition type
* parameters preview
* effects structure

Used for:

* validating condition patterns
* checking effect semantics

---

## Phase D.1 – Runtime Location Context

### Overview

Introduces a session-scoped location layer.

This is:

* runtime-only
* NOT part of schema
* NOT stored in save
* engine-side behavior only

---

### Available Locations

* start_village (織星村)
* forest_edge (迷霧森林)
* town_gate (王都大門)

---

### Location Commands

```text
where
locations
move <location_id>
```

---

### Behavior

* CLI maintains current_location in runtime_context
* Quest completion may be gated by location

---

### Example: Location Gate

```text
> accept q.side.slime_hunt
> progress kill slime 5

> check
# blocked (wrong location)

> move forest_edge

> check
# now complete = True

> complete
# quest completes successfully
```

---

### Runtime Semantics
* One active quest per slot
* One-shot quests (via completed_ids)
* All conditions read from game_state (SSOT)
* Effects mutate game_state only
* CLI list acts as live validation panel
* Location context is session-only (Phase D.1)

---

### Important Constraints
* No schema changes in Phase D.1
* No loader changes
* No structure changes
* Location system is engine-side only

---

### Notes
* $schema warnings in fixtures are non-fatal at runtime
* Schema validation is handled by MVL validation layer
* Runtime focuses on behavior verification only

---

### Summary

This runtime provides a deterministic testbed for:

* data-driven quest logic
* condition correctness
* effect application
* state consistency
* (NEW) location-aware behavior

It is the foundation for future expansion (Phase D.2+),
but intentionally remains minimal and controlled.

---
