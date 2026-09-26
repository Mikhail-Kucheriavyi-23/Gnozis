# CI Regression Classification

Run: 36245157123
Commit: 205d99d946de0450aab09af06b366cb0caa51aec
Result: 223 passed / 43 failed / 1 xfailed

## A. Expected contract migration failures

These tests still encode pre-canonical APIs and must not drive weakening of the new boundary:

- direct `commit(...)` calls without required `kernel_version`
- positional admission passed into `CanonicalExecutor.step()`
- textual assumptions that canonical evolution is implemented in `core/evolution.py`
- legacy State crossing the explicit canonical boundary

## B. Genuine semantic defects requiring implementation work

1. Selector semantics: current selection does not satisfy the documented relation/x sensitivity contract.
2. Proof/admission: invalid candidates can still reach selection in affected paths.
3. Hidden closure: transition acceptance does not yet enforce extensional `Psi=(X,R)` sufficiency.
4. State-space closure: invalid candidates can be repaired/reintroduced instead of being rejected.
5. Hashability: canonical State representation currently exposes `mappingproxy` where trajectory/set operations require a stable hashable representation.
6. Canonical Uroboros wiring: evolutionary compatibility path still needs a clean adapter into the canonical `Psi` executor without allowing legacy State to become authority.

## C. Boundary/API contract mismatches requiring explicit decision

- Engine must reject non-`PsiTransition` transition objects/results.
- Transition boundary must expose only `Psi=(X,R)`.
- Replay/non-commit surfaces must require an explicit transition applier.
- Empty-valid-set behavior and error contract must be standardized.

## Rule

Do not change canonical trust-boundary requirements merely to make legacy tests green. Each failing test is classified first; implementation changes are made only for category B defects or after an explicit contract migration decision for category A/C.
