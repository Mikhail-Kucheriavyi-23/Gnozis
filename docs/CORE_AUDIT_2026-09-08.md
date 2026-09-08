# Ψ-Core Audit — 2026-09-08

## Scope

Audit of the repository's computational core against the working model Ψ = (X, R), with emphasis on state ownership, evolution contracts, immutability boundaries, regression protection, and CI.

## Verified architecture

- `State` is the single authoritative carrier of the current computational representation associated with both X and R.
- `State.values` remains the compatible implementation representation associated with X.
- `State.relations` is an immutable tuple representation of the relational structure R. The tuple is an implementation container and does not introduce mathematical ordering semantics.
- `Relation` remains a frozen record with unconstrained endpoints and validated relation type.
- `evolve()` creates a new State and distinguishes omitted components from explicit replacements; `relations=()` is the explicit representation of R = ∅; `None` is rejected.
- Standard nested dict/list/tuple/set containers in `values` are normalized to protected immutable-style representations for ordinary public mutation operations. Cyclic standard containers are rejected. Arbitrary objects are not recursively frozen.
- Generate → Test → Select operates on complete State candidates, allowing X, R, or both to evolve through the same state transition.
- Tester results must be the built-in `bool` type.
- Generator output must consist only of `State` instances.
- Selector output must be one of the exact candidate objects that passed the test.
- `Uroboros.with_relations()` stores R through State rather than maintaining a second relation state.
- `Uroboros.run()` repeats the endogenous transition without an external selection operator between steps.
- The bridge's legacy autonomous-selection entry point delegates to the canonical core GTS implementation rather than maintaining a second algorithm.

## Regression evidence

The audited branch currently has **58 tests passing** on the full GitHub Actions matrix for Python 3.10, 3.11, 3.12, and 3.13. The latest completed run was green on all four jobs.

The regression suite covers State ownership of X/R, evolve semantics, explicit empty R, rejection of `None`, standard-container alias protection, cyclic-container rejection, Relation freezing, Uroboros relation integration, R evolution through GTS, strict boolean testing, State-only generator output, exact candidate identity, and Engine input contracts.

## Explicit non-claims

This core does not claim arbitrary deep immutability: mutable custom objects stored in X or used as Relation endpoints remain outside the structural immutability contract. The standard-container protection is intended to cover ordinary public mutation paths; Python-level bypasses through base-class methods on compatibility container subclasses are not treated as part of the supported API.

The core also does not claim that a background process automatically runs forever. `Engine.run()` / `Uroboros.run()` provide finite endogenous repetition; scheduling or long-running execution remains infrastructure.

No mathematical semantics for the elements of X, no graph-specific assumptions, and no automatic consistency rule between Relation endpoints and the contents of X are introduced by this audit.

## Remaining research-level targets

1. Define and test any future semantic validity relation between R and X without hard-coding an unjustified element model.
2. Decide whether the abstract R representation should eventually expose set-like semantics while preserving endpoint generality.
3. Extend evidence around endogenous rule/model evolution only after the State-level contract remains stable.
4. Add repository branch protection / required CI checks at the GitHub governance layer if desired; workflow presence alone does not make a branch protected.
