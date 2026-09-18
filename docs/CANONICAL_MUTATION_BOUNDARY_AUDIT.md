# Canonical Mutation Boundary Audit — 2026-09-18

## Finding

The repository currently has two related commit layers:

1. `core/canonical_chain.py::admit_transition()` is the declared generic canonical admission boundary and owns SafetyGate + GasBudget + Provenance + `commit_once()`.
2. `core/execution.py::CanonicalExecutor.evolve()` is the canonical Ψ evolutionary owner and currently calls `commit(...).apply()` directly.

These are not automatically equivalent.

## Consequence

The Ψ executor currently guarantees admission, selection and history continuity, but it does not consume the generic canonical-chain SafetyGate/GasBudget/Provenance contract.

Therefore the repository must not claim that all canonical mutations pass through one universal `canonical_chain` entrypoint.

The defensible statement is narrower: canonical Ψ evolution passes through `CanonicalExecutor` and its history-bound `SemanticCommit`; generic canonical admission has a separate Safety/Gas/Provenance boundary.

## Required next decision

Either unify `CanonicalExecutor` with `canonical_chain.admit_transition()` without weakening Ψ-specific invariants, or explicitly define the two boundaries as separate layers with a documented composition contract.

Do not blindly route the executor through `canonical_chain`: the generic API currently accepts arbitrary current/next state and does not itself enforce Ψ, transition identity, or the executor's selected-candidate semantics.

## Gate

This is an architectural consistency finding, not a claimed runtime failure. Full regression remains pending.
