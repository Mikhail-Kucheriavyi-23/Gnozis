# PM-05 Semantic Apply Path Audit — 2026-09-18

## Classification

| Path | Classification | Semantic Ψ authority |
|---|---|---|
| core/psi_engine.py PsiEngine(PsiTransition) | CANONICAL Ψ | Yes |
| Uroboros.evolutionary -> Engine(PsiTransition) | CANONICAL Ψ adapter | Yes, through PsiTransition.on_state() |
| Engine(State -> State) | LEGACY/GENERIC COMPATIBILITY | No, not evidence of fundamental Ψ semantics |
| gnosis-terminal-bridge/src/core_evolution.py | BRIDGE/COMPATIBILITY | No, must not be treated as canonical Ψ evidence |
| CoreChat | BRIDGE/ADAPTER | No, stateful adapter only |

## Evidence

core/psi_engine.py accepts only PsiTransition and Psi.
core/psi_transition.py defines the canonical Psi -> Psi boundary and its on_state() adapter.
core/evolution.py::evolutionary_psi_transition() now constructs Admission objects before selection.
core/admission.py provides admit() and fail-closed require_admitted().

The generic Engine(State -> State) remains intentionally compatible with existing tests/examples. Removing it would conflate compatibility cleanup with proof of the canonical model.

The bridge creates a generic Engine from an authenticated context. That path is explicitly not canonical Ψ semantics and therefore cannot be used to claim T41 for Ψ.

## Result

PM-05 remains PARTIAL.

The canonical evolutionary Ψ path has an explicit Admission gate, but the repository does not yet have a universal type-level or runtime rule making every possible State -> State mutation pass through Admission.

## Required next design decision

Do not silently delete Engine(State -> State).

Choose one of:

A. Deprecate it and require an explicit legacy compatibility namespace.
B. Keep it as a non-semantic generic utility and formally exclude it from the Ψ semantic surface.
C. Replace it with a typed compatibility adapter that cannot be imported by canonical Ψ modules.

Acceptance for PM-05 COMPLETE:
- canonical Ψ semantic mutations have exactly one admissible commit path;
- compatibility adapters cannot be mistaken for Ψ semantic transitions;
- adversarial tests demonstrate the classification and non-bypass;
- documentation names the trusted semantic boundary.
