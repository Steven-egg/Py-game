05\_engine – MVL Runtime (Phase B)
This folder contains the Phase B Minimal Viable Loop (MVL) Runtime and CLI tools.

Phase B is the executable runtime layer used to validate:

Schema Discipline: Loader validation against existing specs.

Governance Behavior Gates: Ensuring logic follows defined protocols.

State SSOT: Single Source of Truth consistency.

MVL Loop Correctness: accept → progress → check → complete → save.

This layer is NOT gameplay, but a deterministic verification runtime.

Role in Architecture (Phase B)

State SSOT: save.game\_state (flags / inventory / vars) is the single source of truth for condition evaluation and effect application.
Runtime Execution: Processing quest logic based on JSON definitions.

Condition Evaluation: Logic for accept\_condition and complete\_condition.

Effect Dispatch: MVP implementation for applying rewards (gold, flags).

Save State Synchronization: Persistent storage of player progress and history.

CLI-based Inspection: A "game lobby" interface to monitor state.

Quick Start \& Core Concepts

1. Load Content \& Warnings
   Bash
   python 05\_engine/cli\_mvl.py load
   **Note on $schema:** Warnings about missing $schema fields in fixtures are non-fatal for runtime but should be resolved in the data layer for full compliance.
2. Save Slots \& Typical States
   Use --slot to isolate different testing scenarios:

Slot 2 (slot\_2.json): Demonstrates an Active State. Contains an ongoing quest. Use this to test progress and complete.

Slot 3 (slot\_3.json): Demonstrates a Post-Completion State. Contains completed\_ids. Use this to test "one-shot" quest guards.

3. The Quest Lobby (list)
   The list command dynamically checks the environment and save state:

\[DONE]: Quest ID is in completed\_ids.

\[ACTIVE]: Current active\_quest in the slot.

\[READY]: accept\_condition is met.

\[LOCKED]: accept\_condition failed (displays the specific missing requirement).

Bash
python 05\_engine/cli\_mvl.py --slot slot\_3 list
The MVL Loop (Step-by-Step)
Step 1: Accept a Quest
Bash
python 05\_engine/cli\_mvl.py --slot slot\_1 accept <quest\_id>
Guard 1: Blocked if another quest is already active.

Guard 2: Blocked if the quest\_id is already in completed\_ids (default one-shot quest semantics).

Step 2: Report Progress
Updates the trackers and the global game state.

Bash

# Update kill counts

python 05\_engine/cli\_mvl.py --slot slot\_1 progress kill slime 5

# Update world flags

python 05\_engine/cli\_mvl.py --slot slot\_1 progress flag flg.npc.met\_guard true
Step 3: Complete Quest
Evaluates completion conditions and triggers effects.

Bash
python 05\_engine/cli\_mvl.py --slot slot\_1 complete
Upon success:

rewards.effects are applied to game\_state.

quest\_id is moved to completed\_ids.

active\_quest is set to None.

Step 4: Verification (show)
Inspect the final SSOT state to ensure data integrity.

Bash
python 05\_engine/cli\_mvl.py --slot slot\_1 show
Debugging: Quest Dump
For a semantic preview of a quest's internal logic without opening the JSON:

Bash
python 05\_engine/cli\_mvl.py questdump q.side.slime\_hunt

---



\## Phase B Runtime Semantics (Current)



\- One active quest per slot.

\- One-shot quests by default (tracked via completed\_ids).

\- accept\_condition and complete\_condition use the same recursive Condition evaluator.

\- All conditions read from save.game\_state (SSOT).

\- Effects mutate save.game\_state only (never fixture data).

\- CLI list acts as a live validation panel.

