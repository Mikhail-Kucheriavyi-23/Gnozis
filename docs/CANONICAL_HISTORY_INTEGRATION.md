# Canonical History Integration Decision Point — 2026-09-18

## Finding

`SemanticCommit.apply(history)` can already bind an accepted `Psi` to `AppendOnlyHistory`, but the current `PsiTransition` contract is `Psi -> Psi` and `Engine/Uroboros` consume that pure transition without a history object.

Forcing history into `PsiTransition` would change the fundamental mathematical operator and risk conflating dynamics with persistence.

## Required architecture

Keep `F: Psi -> Psi` as the fundamental transition.

Place persistence at the execution boundary:

`Psi --F--> Psi'`
`+ Admission/Proof metadata`
`-> SemanticCommit`
`-> TransitionRecord`
`-> AppendOnlyHistory`

The execution owner (not the pure transition function) must own the history value and return the updated state/history pair.

## Acceptance criteria

1. Pure `PsiTransition` remains `Psi -> Psi`.
2. Canonical execution cannot silently discard an accepted transition.
3. Every canonical production step creates exactly one `TransitionRecord`.
4. Record provenance is constructed from the admitted transition, not caller-supplied arbitrary hashes.
5. Replay reads accepted history and never becomes a commit authority.
6. Compatibility `Engine(State -> State)` remains outside canonical history guarantees.

## Current status

The repository has the commit/history primitives but not yet a single integrated execution owner satisfying all six criteria. Do not mark PM-12 complete until such an owner exists and regression tests cover one-record-per-step, rejection-without-record, and replay-without-commit.
