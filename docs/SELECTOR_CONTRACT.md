# Selector Contract

## Status

This document freezes the current selector contract for the regression stage. It does not claim that this criterion is the final mathematical selector for Ψ.

### Generic compatibility selector

For `select_next_state(State, Generate, Test)`, candidates are filtered by the strict boolean Test contract and the selected candidate is:

`min(valid, key=_generic_score)`

where `_generic_score(state) = (repr(state),)`.

This makes the generic selector deterministic and independent of external selector state, but it is not a semantic claim about Ψ.

### Canonical Ψ selector

For `evolutionary_psi_transition`, valid candidates are ranked by:

`(|R|, repr(Ψ))`

with `Ψ=(X,R)` obtained from `State.to_psi()`.

Therefore the current canonical criterion prefers fewer relations first and uses representation ordering only as a deterministic tie-breaker.

### Consequence

A test must not infer monotonic increase of `X` merely from the existence of an endogenous selector. If a transition must prefer increasing `X`, that preference must be explicitly added to and justified as part of the canonical selection criterion.

### Regression rule

Do not change selector semantics solely to satisfy an old trajectory assertion. First define the criterion, then encode it as a contract test.
