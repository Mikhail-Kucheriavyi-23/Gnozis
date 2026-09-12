# Core Regression Matrix

## Scope

This matrix separates direct canonical Ψ evidence from generic Engine/legacy evidence. It is a status map, not a claim that the mathematical theory is proven.

| Contract | Evidence | Classification | Status |
|---|---|---|---|
| State deep immutability | `tests/test_state_immutability.py` | CORE | GREEN by test coverage |
| Test(candidate) returns bool | `tests/test_core_contract_repairs.py` | CORE | GREEN by test coverage |
| bool cannot be step count | `tests/test_core_contract_repairs.py` | CORE | GREEN by test coverage |
| Relation extinction `R -> ∅` | `tests/test_relation_evolution.py` | CANONICAL Ψ | GREEN by test coverage |
| X/R separation | `tests/test_x_r_separation.py` | CANONICAL Ψ | GREEN by test coverage |
| locality | `tests/test_locality_contract.py` | CANONICAL Ψ | GREEN by test coverage |
| causal closure | `tests/test_causal_closure.py` | CANONICAL Ψ | GREEN by test coverage |
| deterministic pure transition | `tests/test_pure_transition.py` | CANONICAL Ψ | GREEN by test coverage |
| trajectory/state-space closure | `tests/test_trajectory_closure.py`, `tests/test_state_space_closure.py` | CANONICAL Ψ | GREEN by test coverage |
| memory provenance/independence | `tests/test_memory_provenance.py`, `tests/test_memory_independence.py` | SUPPORTING | GREEN by test coverage; does not implement protected persistent memory |
| Engine State->State contract | `tests/test_legacy_transition_boundary.py` | COMPATIBILITY | GREEN by contract coverage |
| Engine/Uroboros Ψ integration | `tests/test_psi_transition.py` and related integration tests | CANONICAL Ψ | GREEN by targeted coverage; full CI evidence still separate |
| Port security | Port CI | BRIDGE | GREEN for available Port CI run |
| Full repository pytest | `test.yml` | CI GATE | EVIDENCE MUST BE VERIFIED ON CURRENT HEAD |

## Interpretation

A GREEN row means the named implementation/test evidence is present. It does not mean the general theory is mathematically proven.

The next gate is a full `pytest -q` CI result on the current HEAD, followed by adversarial regression. Only after those gates should the legacy transition path be considered for removal.
