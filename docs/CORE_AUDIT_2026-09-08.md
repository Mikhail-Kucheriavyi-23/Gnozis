# Ψ-Core Audit — 2026-09-08

## Scope

Audit of the repository's computational core against the working model Ψ = (X, R), with emphasis on state ownership, evolution contracts, immutability boundaries, regression protection, package integrity, and CI.

## Verified architecture

- `State` is the single authoritative carrier of the current computational representation associated with both X and R.
- `State.values` remains the compatible implementation representation associated with X.
- `State.relations` is an immutable tuple representation of the relational structure R. The tuple is an implementation container and does not introduce mathematical ordering semantics.
- `Relation` remains a frozen record with unconstrained endpoints and validated relation type.
- `evolve()` creates a new State and distinguishes omitted components from explicit replacements; `relations=()` is the explicit representation of R = ∅; `None` is rejected.
- Standard nested dict/list/tuple/set containers in `values` are normalized to protected immutable-style representations for ordinary public mutation operations. Cyclic standard containers are rejected. Arbitrary objects are not recursively frozen.
- Generate → Test → Select operates on complete State candidates, allowing X, R, or both to evolve through the same state transition.
- The GTS boundary validates the initial State, all three operators, candidate State outputs, strict built-in `bool` tester results, and exact identity of the selected tested candidate.
- `Uroboros.with_relations()` stores R through State rather than maintaining a second relation state.
- `Uroboros.run()` repeats the endogenous transition without an external selection operator between steps.
- The bridge's legacy autonomous-selection entry point delegates to the canonical core GTS implementation rather than maintaining a second algorithm.
- The bridge-to-core adapters pass credential-free derived state into the core while keeping authentication concerns outside the core.

## Regression evidence

The latest completed GitHub Actions run for the audited branch passed **79 tests** on each Python 3.10, 3.11, 3.12, and 3.13 matrix job. The run was green on all four jobs.

The regression suite covers State ownership of X/R, evolve semantics, explicit empty R, rejection of `None`, standard-container alias protection, nested standard-container normalization, cyclic-container rejection, Relation freezing and validation, Uroboros relation integration, R evolution through GTS, strict boolean testing, State-only generator output, exact candidate identity, initial State validation, operator callability, Engine input contracts, and protection against direct structural mutation attempts.

CI additionally verifies package installation, dependency consistency with `pip check`, Python compilation of both `core` and the terminal bridge, and the full pytest suite.

## Explicit non-claims

This core does not claim arbitrary deep immutability: mutable custom objects stored in X or used as Relation endpoints remain outside the structural immutability contract. The standard-container protection is intended to cover ordinary public mutation paths; Python-level bypasses through base-class methods on compatibility container subclasses are not treated as part of the supported API.

The core also does not claim that a background process automatically runs forever. `Engine.run()` / `Uroboros.run()` provide finite endogenous repetition; scheduling or long-running execution remains infrastructure.

No mathematical semantics for the elements of X, no graph-specific assumptions, and no automatic consistency rule between Relation endpoints and the contents of X are introduced by this audit.

## Remaining research-level targets

1. Define and test any future semantic validity relation between R and X without hard-coding an unjustified element model.
2. Decide whether the abstract R representation should eventually expose set-like semantics while preserving endpoint generality.
3. Extend evidence around endogenous rule/model evolution only after the State-level contract remains stable.
4. Add repository branch protection / required CI checks at the GitHub governance layer if desired; workflow presence alone does not make a branch protected.
5. Consider a future dedicated immutable mapping type if stronger resistance to Python-level base-class mutation bypasses becomes a formal requirement; the current JSON-compatible dict subclass deliberately documents that boundary rather than claiming absolute immutability.
