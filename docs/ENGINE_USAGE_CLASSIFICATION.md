# Engine Usage Classification

## Purpose

This document separates evidence for canonical Ψ evolution from compatibility and infrastructure use of `Engine`.

## Classification

| Area | Classification | Rule |
|---|---|---|
| `core/uroboros.py` evolutionary path | CANONICAL Ψ | Must use `PsiTransition` |
| Ψ transition integration tests | CANONICAL Ψ | Evidence for `(X,R)` evolution |
| Generic `Engine(State -> State)` tests | GENERIC ENGINE | Valid engine contract, not Ψ proof |
| Legacy examples/callers | COMPATIBILITY | May remain temporarily |
| Terminal/bridge integration | BRIDGE | Must not be treated as canonical Ψ evidence |

## Decision rule

A test or caller using a plain `State -> State` callable cannot by itself establish a Ψ invariant. It may establish the generic Engine contract or compatibility behavior.

A claim about canonical Ψ semantics requires the `PsiTransition` path or an explicit proof that the compatibility layer delegates to the same Ψ semantics.

## Next gate

Run the full regression suite and adversarial suite, then audit whether any remaining generic/legacy caller is required by supported public behavior. Only then decide whether the compatibility path can be removed.
