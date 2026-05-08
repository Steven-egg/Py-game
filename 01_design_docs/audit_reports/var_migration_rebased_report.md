# Var Migration Rebased Report

Base registry: latest uploaded `flags.registry.json`.

## Changed files
- flags.registry.json
- vars.registry.json
- test_complex_trial.json
- test_kill_slime.json
- test_kill3_slime.json
- test_quest.json

## Migration performed
- `flg.kill.slime.count` → `var.kill.slime.count`
- `flg.kill.goblin.count` → `var.kill.goblin.count`
- `flg.kill.wolf.count` → `var.kill.wolf.count`
- `flg.test.phase_c.counter` → `var.test.phase_c.counter`
- `flag.int_compare` → `var.int_compare`
- `flag.add_int` → `var.add_int`
- `params.delta` → `params.value` for `var.add_int`

## Registry changes
- Removed numeric state entries from `flags.registry.json`:
  - `flg.kill.slime.count`
  - `flg.kill.wolf.count`
- Added numeric state entries to `vars.registry.json`:
  - `var.kill.slime.count`
  - `var.kill.goblin.count`
  - `var.kill.wolf.count`
  - `var.test.phase_c.counter`

## Checks performed here
- JSON syntax check: PASS
- Residual invalid flag numeric pattern scan: PASS

## Remaining invalid references
None

## Not executed here
- Project-local validation command was not run because the local validation scripts and project folder are not available in this uploaded-file workspace.
- `sync_registry_to_schema.py` was not run because the tool file was not uploaded.

## Required local next commands
Run these in your project root after replacing files:

```powershell
# example only; use your actual validation command
py 05_engine/validation/mvl_test_v2.py
py <path-to>/sync_registry_to_schema.py
```
