# Canonical Ψ Selector Invariant — 2026-09-26

## Frozen current criterion

For the current audited implementation:

`score(Ψ) = (|R|, repr(Ψ))`

and selection is the minimum lexicographic score over admitted candidates.

## Proven properties of this criterion

1. **Permutation invariance:** candidate enumeration order is not a selection signal because selection uses `min(..., key=score)`.
2. **Determinism:** for the same admitted candidate set and stable representations, the result is deterministic.
3. **No implied X-monotonicity:** the criterion does not claim that larger `X` is preferred.
4. **R sensitivity:** relation cardinality is the primary ordering component; representation is the tie-breaker.

## Contract boundary

A requirement such as "selection must prefer increasing X" is a different invariant and is not implied by endogenous selection. It must be introduced as a new mathematical criterion before changing production code.

Therefore this R2 closure does not alter `_psi_score()`.

## Legacy separation

The existing permutation tests exercise the legacy `State -> State` compatibility selector. They provide evidence for deterministic ordering but are not proof of the canonical `Ψ` selector. Canonical selector evidence must use `evolutionary_psi_transition` and admitted candidates.

## Decision

No production selector change is justified by the currently documented contract. Any future X-sensitive selection requirement requires a separate contract, counterexamples, and canonical tests.
