# Canonical PsiTransition Delegation Audit — 2026-09-18

## Finding

The repository defines `core/psi_transition.py::PsiTransition` as the canonical fundamental operator `F: Psi -> Psi`. However, `core/execution.py::CanonicalExecutor.evolve()` currently adapts `Psi -> State`, invokes the supplied `generate(State)` and `test(State)`, and converts selected candidates back to `Psi` before commit.

Therefore the current CanonicalExecutor path is Ψ-shaped at its input/output boundary but does not itself delegate generation/testing to `PsiTransition`.

## Why this matters

The historical regression classification states that canonical Ψ evidence must use `PsiTransition` or explicitly prove delegation to the same Ψ semantics. Generic `State -> State` callables can close over hidden external state, so they cannot by themselves establish that the transition is a function only of `(X,R)`.

## Status

OPEN architectural conformance finding. This is not evidence that the current executor is incorrect; it is evidence that the declared `PsiTransition` contract and the executor's actual operator boundary are not yet formally connected.

## Required decision

Before claiming Markov sufficiency for canonical evolution, choose and document one of:

1. make `PsiTransition` the explicit generator/operator boundary for canonical evolution and keep candidate testing/selection as separate functions; or
2. prove that the existing `generate(State)` + `test(State)` path is a valid implementation of the same `F: Psi -> Psi` contract, including a precise rule for closure/external state.

Do not remove `State` compatibility merely to make the types look cleaner; preserve the adapter role unless the semantic contract is deliberately changed.
