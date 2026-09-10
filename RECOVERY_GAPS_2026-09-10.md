# Gnozis Recovery Gaps — 2026-09-10

Purpose: explicit ledger for the September 2–10 historical reconciliation. This file prevents reconstructed material from being mistaken for recovered primary-source decisions.

## Status legend

- CONFIRMED — present in repository and/or directly executable in current code/tests.
- RECOVERED — exact historical decision/equation recovered from primary chat material.
- RECONSTRUCTED — derived from retained project context; not primary-source recovery.
- GAP — expected historical material is not currently available in the repository and must not be invented.
- PLANNED — accepted implementation work, not yet complete.

## Confirmed in repository / recovered audit material

- Minimal Ψ direction: `Ψ=(X,R)`.
- Endogenous evolution direction: `E:X→2^X` and state/rule-state extension `Y=(X,ρ)`.
- Hidden-state/extensionality constraints.
- Explicit anti-hidden observer/selector/correction/global-clock requirements.
- Locality and causal-closure regression contracts.
- Memory provenance regression contracts.
- Secure bridge / Internet Port direction with challenge binding, expiration, replay protection, fail-closed behavior, identity/provenance and authority boundaries.
- Living Context / project-state hierarchy.
- Historical core audit empirically reproduced: default `Uroboros()` identity transition; `with_relations()` losing relations; `Test` accepting truthy non-bools; `bool` accepted as `steps=1`; shallow immutability; hidden `_pending_message`; shared threaded chat state; fail-open authentication; misleading `/health`; duplicate `PsiTransition` implementations; formal Ψ boundary isolated from the live Engine/Uroboros/Evolution path.
- Recommended lightweight architecture: typed `Psi`, typed `State`, one canonical transition, explicit Ports/Adapters, property-based/adversarial regression tests.
- Direct prior-art comparison recovered: Ψ's Generate→Test→Select pattern is related to genetic programming/generate-and-test; formal proof-before-self-modification is closely related to Gödel Machine; practical agent loops include Voyager/Reflexion/Self-Refine. These are comparisons, not claims of equivalence.

## Historical recovery search status

A focused Library search was performed for the user-described episode in which a Gnozis-generated proposal about protected/internal memory was forwarded into the conversation. Searches covered semantic variants of: Gnozis + memory, protected/encrypted memory, key/nonce, hash, ciphertext, integrity, provenance, trajectory, state/trace, and related Russian wording.

Result: the exact forwarded Gnozis proposal and its cryptographic equations have NOT yet been uniquely identified. Do not mark them as recovered. The search did recover adjacent historical memory/state material and the engineering audit, but not the specific cryptographic proposal.

## Historical gaps requiring primary-source recovery

### 1. Protected / encrypted internal memory — PRIORITY 1

The repository explicitly states that the exact earlier cryptographic construction has not been recovered. Do not replace it with a newly invented design and label it historical.

Recovery target:

- exact mathematical state representation used in the earlier discussion;
- encryption/authentication construction actually discussed;
- key/nonce or equivalent state semantics if present;
- continuity/integrity equations;
- relation between protected memory and `M=H(trajectory)`;
- treatment of memory as derived history versus causal state;
- handoff/reconstruction semantics;
- exact security assumptions and failure cases.

### 2. Third-party / independent audits — PRIORITY 2

Recover exact findings rather than only the summarized labels. For each audit preserve:

`claim → criticism → counterexample → response → code/test → final status`.

Required themes include hidden state, extensionality, observer/selector dependence, global clock, external correction, locality leakage, endogenous rule update, reproducibility, provenance and authority.

### 3. September mathematical experiments — PRIORITY 3

Preserve exact formulas/parameters/results for the following branches where primary material exists:

- attractors / effective dimension;
- Bell/nonlocality;
- holographic/information bounds;
- path algebra / GNS / Born rule;
- Lorentz invariance / LIV;
- Lyapunov-style monotonicity;
- `α≈137` exploration;
- `SU(2)×SU(3)` correspondence;
- E8 exploration;
- causal DAG;
- information-memory “ball-in-ball” geometry;
- Green–Schwarz anomaly / island-topology experiment;
- large sparse `PsiCorev33InfinityEngine` stress experiment;
- spectral collision analysis.

These remain hypotheses/tests until exact evidence is recovered.

## Current engineering discrepancy to preserve

Recent CI evidence showed an import/contract failure involving `Selector` in `core/uroboros.py` importing from `core.evolution`. Do not resolve this by blindly adding a selector implementation: first verify whether the intended selector is an internal endogenous operator and what its explicit selection criterion is.

A separate HTTP replay contract previously returned `400` where the security contract expected `401`. Preserve this as a historical contract defect if it is already fixed in the current branch; do not describe the old failure as the current state without checking CI.

## Recovery rule

No historical equation, cryptographic design, audit result, or architectural decision may be promoted from RECONSTRUCTED to RECOVERED without primary-source evidence.

When primary chat material becomes available, update this ledger and then update:

1. `GNOZIS_MASTER_AUDIT.md`
2. `PROJECT_STATE.md`
3. `EVOLUTION.md`
4. `CLAIMS.md`
5. `ROADMAP.md`
6. `CHANGELOG`
7. executable tests where applicable
