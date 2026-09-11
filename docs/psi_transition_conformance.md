# Ψ Transition Contract Conformance

This document maps the minimal Ψ transition contract to the current executable proof surface.

| Contract property | Evidence | Status |
|---|---|---|
| `State` is the canonical state source | Core/state and evolution tests | PASS |
| `Test(candidate)` is boolean acceptance | evolution tests | PASS |
| No external selector controls selection | selector-injection adversarial test | PASS |
| Candidate order does not control Ψ | order-invariance adversarial test | PASS |
| Unrelated metadata/object identity is not a selector signal | hidden-metadata tests | PASS |
| `R -> empty` can occur through evolution | relation-evolution tests | PASS |
| `empty -> R` can occur through evolution | relation-evolution tests | PASS |
| `X -> X'` with fixed `R` | X-evolution tests | PASS |
| `R -> R'` with fixed `X` | X/R separation tests | PASS |
| `X,R -> X',R'` | joint-evolution tests | PASS |
| Rejected candidates are not returned as fallback | empty-valid-set tests | PASS |
| Empty valid set is not a fixed point | no-valid-candidate semantics tests | PASS |
| Accepted unchanged candidate is a fixed point | fixed-point semantics tests | PENDING CI confirmation |
| Previous state is not implicitly mutated | state immutability tests | PASS |
| Wire serialization remains outside canonical state model | terminal bridge/API tests | PASS |

## Semantic trichotomy

For a current state `s`, let `V_s` be the accepted candidate set.

1. `V_s = empty` -> no transition is produced.
2. `V_s != empty` and selected `Psi' = Psi` -> fixed point.
3. `V_s != empty` and selected `Psi' != Psi` -> evolution.

The three cases must not be conflated.

## Engineering boundary

The contract is intentionally narrower than a complete mathematical theory. A green test proves the stated executable property under the tested construction; it does not by itself prove universal mathematical validity.

The next mathematical task is to characterize the transition relation itself: admissible candidates, closure, fixed points, and conditions for endogenous change without introducing an external operator.
