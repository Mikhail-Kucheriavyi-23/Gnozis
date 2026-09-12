# Gnozis Core Conformance Matrix

Updated: 2026-09-12

Purpose: connect the Ψ contract to the live implementation and prevent tests from becoming a separate proof island.

## Status legend

- GREEN — implemented and covered by executable evidence in the current repository.
- YELLOW — partially integrated or evidence exists only for a boundary/adapter.
- RED — known discrepancy or missing canonical integration.

| Invariant / contract | Requirement | Current implementation | Evidence | Status |
|---|---|---|---|---|
| Fundamental domain | Ψ=(X,R) | `core/state.py::Psi` | Ψ transition tests | GREEN |
| State adapter | State projects to and reconstructs Ψ | `State.to_psi()` / `State.from_psi()` | state/transition tests | GREEN |
| Canonical Ψ transition | One fundamental `F: Ψ→Ψ` | `core/psi_transition.py` | integration/conformance tests | YELLOW — legacy State-callable path remains explicit compatibility |
| X representation | X remains the state payload | `Psi.x` / State `x` field | adapter tests | GREEN at boundary level |
| R representation | R is an immutable tuple of `Relation` values at the Uroboros relation boundary | `Uroboros.with_relations()` validates and stores `tuple[Relation, ...]` | repair regression | GREEN at canonical relation boundary |
| Deep immutability | Built-in nested containers cannot mutate prior State | recursive `_freeze()` | state tests | GREEN for supported built-ins |
| Relation persistence | R is part of state, not discarded metadata | `Uroboros.with_relations()` | repair regression | GREEN |
| Strict Test contract | `Test(candidate) -> bool` exactly | `_test_candidate()` | repair regression | GREEN |
| Step-count contract | `steps` is real `int`; bool rejected | `Engine._validate_steps()` | repair regression | GREEN |
| Fail-closed Uroboros | Unconfigured core must not silently identity-evolve | `_unconfigured_transition()` | repair regression | GREEN |
| Endogenous selection | validity + deterministic state-derived selection | `evolution.py` | adversarial/reproducibility tests | GREEN |
| Locality | transition depends only on declared state | existing suite | locality tests | GREEN |
| Causal closure | evolution stays within declared causal boundary | existing suite | causal-closure tests | GREEN |
| Memory provenance | external memory cannot silently affect transition | existing suite | memory-independence suite | GREEN |
| Protected internal memory | exact historical cryptographic design | not recovered | recovery ledger | RED / GAP |
| Internet Port/Core alignment | bridge preserves authority/provenance boundaries | bridge + security tests | port suite | YELLOW |
| Latest CI evidence | current commit has actual workflow evidence | workflow exists; latest evidence must be rechecked | GitHub Actions | YELLOW |

## 2026-09-12 reconciliation update

The relation boundary is now stricter: `Uroboros.with_relations()` accepts only `Relation` instances and stores them as an immutable tuple. This closes the previous ambiguity where arbitrary tuples could masquerade as relations.

This is a boundary-level consolidation, not a claim that every possible `R` payload in the entire repository is already fully typed. The fundamental Ψ contract remains `Ψ=(X,R)`, while the canonical Uroboros relation API now defines the concrete relation representation.

## Current reconciliation rule

The formal Ψ transition boundary is explicitly present, but the project must converge on one canonical route:

`Ψ → State adapter → Engine/Evolution → Ψ`

No second semantic transition implementation should be introduced. Boundary adapters may exist, but they must delegate to the canonical transition rather than redefine it.

## Next gate

Before expanding mathematical/physics research, run the full regression suite against the repaired live Core, then make the explicit architectural decision whether the legacy State-callable transition remains as a documented compatibility API or is removed.
