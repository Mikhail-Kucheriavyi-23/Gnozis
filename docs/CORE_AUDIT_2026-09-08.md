# Ψ-Core Audit — 2026-09-08

## Scope

Audit of the repository's computational core against the working model Ψ = (X, R), with emphasis on state ownership, evolution contracts, immutability boundaries, regression protection, and CI.

## Verified architecture

- `State` is the single authoritative carrier of the current computational representation associated with both X and R.
- `State.values` remains the compatible implementation representation associated with X.
- `State.relations` is an immutable tuple representation of the relational structure R. The tuple is an implementation container and does not introduce mathematical ordering semantics.
- `Relation` remains a frozen record with unconstrained endpoints and validated relation type.
- `evolve()` creates a new State and distinguishes omitted components from explicit replacements; `relations=()` is the explicit representation of R = ∅; `None` is rejected.
- Standard nested dict/list/tuple/set containers in `values` are normalized to immutable representations. Cyclic standard containers are rejected. Arbitrary objects are not recursively frozen.
- Generate → Test → Select operates on complete State candidates, allowing X, R, or both to evolve through the same state transition.
- Tester results must be the built-in `bool` type.
- Selector output must be one of the exact candidate objects that passed the test.
- `Uroboros.with_relations()` stores R through State rather than maintaining a second relation state.
- `Uroboros.run()` repeats the endogenous transition without an external selection operator between steps.
- The bridge's legacy autonomous-selection entry point delegates to the canonical core GTS implementation rather than maintaining a second algorithm.

## Regression evidence

At the audited branch head before this hardening pass, GitHub Actions completed successfully on Python 3.10, 3.11, 3.12, and 3.13 with **55 tests passed**.

The hardening pass adds regression coverage for engine input validation and cyclic standard containers and updates CI to install the package itself before running the full suite. The resulting commit must be accepted only after its new CI run is green on the complete matrix.

## Explicit non-claims

This core does not claim arbitrary deep immutability: mutable custom objects stored in X or used as Relation endpoints remain outside the structural immutability contract.

The core also does not claim that a background process automatically runs forever. `Engine.run()` / `Uroboros.run()` provide finite endogenous repetition; scheduling or long-running execution remains infrastructure.

No mathematical semantics for the elements of X, no graph-specific assumptions, and no automatic consistency rule between Relation endpoints and the contents of X are introduced by this audit.

## Remaining research-level targets

1. Define and test any future semantic validity relation between R and X without hard-coding an unjustified element model.
2. Decide whether the abstract R representation should eventually expose set-like semantics while preserving endpoint generality.
3. Extend evidence around endogenous rule/model evolution only after the State-level contract remains stable.
4. Add repository branch protection / required CI checks at the GitHub governance layer if desired; workflow presence alone does not make a branch protected.
