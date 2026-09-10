# GNOZIS — PROJECT STATE

**State version:** 2026-09-10 / Audit baseline 1.0
**Public baseline:** Ψ-Core v33, 2026-09-03

## Current status
Gnozis is a research project investigating whether a minimal endogenous computational architecture can support recursive state evolution, model construction, autonomous hypothesis generation/testing/selection, and eventually broader machine reasoning and discovery.

**Current stage:** consolidation and purification of the minimal effective core, followed by adversarial validation. The immediate goal is not a larger intelligence layer, but a clean, reproducible and auditable state model.

## Fundamental model
The working mathematical lineage has converged toward:

```text
Ψ = (X, R)
```

`X` is system state; `R` is the relation structure. Auxiliary representation may exist, but the fundamental Ψ projection is `(X,R)`.

The central requirement is endogenous evolution: the next state should arise from the current state and internal transition machinery rather than a permanently external correction operator.

## Current evolutionary mechanism
```text
Current State → Generate candidates → Test → retain tested candidates → Select → Next State → Repeat
```

The repository implementation rejects empty candidate sets, rejects the case where no candidate passes the test, and rejects a selector result not contained in the tested candidates.

## Current invariants
1. Fundamental state is Ψ=(X,R).
2. Evolution is state-transition based.
3. Accepted candidates must pass the relevant test.
4. Selection occurs inside the evolutionary transition path.
5. Repeated steps can execute without a new external command after construction.
6. Fundamental transition behavior must be extensional over `(X,R)` rather than irrelevant hidden metadata.
7. Scientific claims remain separate from software behavior.
8. Reproducibility and negative results are first-class.
9. AI is an interface/reasoning component, not the definition of the core.
10. Minimum necessary complexity is preferred.

## Verified repository implementation
- `core/state.py`: `Psi(x, relations)` and immutable `State` wrapper.
- `core/engine.py`: deterministic transition, finite run and trajectory.
- `core/evolution.py`: Generate → Test → Select transition.
- `core/contract.py`: extensionality checks over the Ψ projection.
- `core/uroboros.py`: recursive wrapper and evolutionary constructor.
- Additional bridge/adapter components exist in the repository.

## Not established
The repository does not establish general intelligence, consciousness, physical theory validity, Born-rule derivation, Bell nonlocality derivation, Lorentz invariance/emergence, holographic-bound derivation, Standard Model gauge-group emergence, alpha≈137 derivation, a universal theory of reality, or strong biological autopoiesis. These remain research questions unless explicit reproducible evidence exists.

## Historical convergence
```text
Phenomenological intuition
  → Ψ as information/process model
  → Ψ=(X,R) minimalization
  → endogenous evolution E
  → extended state/rule-state ideas
  → Generate → Test → Select
  → adversarial audits of external selectors/hidden state/observers
  → minimal UROBOROS / Ψ-Core implementation
  → GNOSIS public baseline v33
  → current living-state + minimal-effective-core phase
```

Earlier formulations are historical unless explicitly promoted again.

## Do not reintroduce without new evidence
- permanent external correction as a fundamental operator;
- human confirmation as a required evolutionary selector;
- a hidden global observer/selector outside the transition;
- treating an AI model as the complete Gnozis core;
- treating a passing software test as proof of a scientific theory;
- resurrecting failed claims solely because an older version contained them.

## Current research frontier
1. Maintain one authoritative project state.
2. Make current mathematical definitions explicit and minimal.
3. Audit executable core against invariants.
4. Audit bridge/agent layers for external-control leakage.
5. Add adversarial regression tests for extensionality, autonomy, reproducibility and Generate/Test/Select integrity.
6. Then extend toward memory, internal models, multi-agent interaction and scientific discovery.
7. Keep physics/math claims as separate evidence tracks.

## Model handoff order
```text
PROJECT_STATE.md
PHILOSOPHY.md
EVOLUTION.md
ARCHITECTURE.md
CLAIMS.md
ROADMAP.md
CHANGELOG
code + tests
```

Repository evidence overrides conversational assumptions.

## Update rule
Every material decision must update this state, preserve historical evidence, classify claims, and update the roadmap when the next experiment changes. Failed and abandoned approaches must remain traceable rather than silently deleted.
