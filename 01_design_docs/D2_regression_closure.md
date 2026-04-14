# D.2 Regression Closure Note

Date: 2026-04-13

## Result
- mvl_test_v1.py: PASS
- mvl_test_v2.py: PASS

## Fix Summary
- Removed `$schema` from fixtures
- Aligned reward effects with schema contract
- Fixed missing `target` in effects
- Adjusted flag key patterns
- Removed `var.add` from quest fixture (not in schema contract)

## Observation
- Engine capability (DD-016) includes `flag.int_add` / `var.add`
- Schema enum uses `flag.add_int`
- Potential naming inconsistency exists between engine and schema

## Conclusion
- D.2 regression fully passes
- No evidence of location persistence breaking MVL baseline