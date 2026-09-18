# Gnozis Proof Matrix — 2026-09-18

Status: first evidence-backed mapping after Mathematical Freeze (CLXI–CLXIV).

Legend:
- IMPLEMENTED: code exists and repository evidence directly supports the contract.
- PARTIAL: a boundary/approximation exists, but the full mathematical contract is not established.
- MISSING: no corresponding implementation was found in the current repository tree/search.
- UNVERIFIED: implementation/tests exist, but the current tool pass did not execute the suite.

This document is an audit map, not a proof claim.

| ID | Mathematical requirement | Repository evidence | Status | Proof / test obligation | Next |
|---|---|---|---|---|---|
| PM-01 | Psi=(X,R) is the semantic core | core/state.py::Psi | IMPLEMENTED | T1–T2; state representation tests | Formalize typed X/R |
| PM-02 | State is an adapter, not second semantic model | State.to_psi()/from_psi() | PARTIAL | T3; adapter/extensionality tests | Remove/constrain competing State transition path |
| PM-03 | Deep immutability | recursive _freeze() | IMPLEMENTED* | T4; nested mutation tests | *Only supported built-ins; custom payloads remain outside contract |
| PM-04 | Generate -> Test -> proof/admission -> Select -> Transition | core/evolution.py, core/proof.py | PARTIAL | T5–T12; proof-gate tests | Separate explicit Admission from current proof-gated selection |
| PM-05 | Apply cannot bypass Admission | `core/admission.py` + `core/commit.py`; canonical evolutionary Ψ path now crosses `SemanticCommit` | COMPLETE (canonical Ψ scope) | T41 | Keep adversarial regression coverage; audit future semantic callers against the boundary |
| PM-06 | Selection is not an external oracle | endogenous selection + adversarial tests | IMPLEMENTED at tested path | T18–T23 | Formal proof, not only tests |
| PM-07 | Partial-order/branch outcome allowed | `Branch` ancestry + `incomparable()` + `ParallelOutcome` explicitly retain concurrent branches | COMPLETE (branch-order scope) | T18–T23 | Preserve regression coverage; broader merge algebra remains separate work if required |
| PM-08 | Conflict is retained, not silently erased | branch-aware `Conflict`, `ResolutionCandidate`, `DeferredConflict`; admitted resolutions use Proof→Admission→SemanticCommit | COMPLETE (resolution scope) | T18–T23 | Regression audit only |
| PM-09 | Self-evolution has protected root invariant K0 | `core/root_invariant.py::RootInvariant` + preservation tests + meta-transition gate | COMPLETE (K0 boundary) | T24–T29, T38 | Bind K0 to canonical kernel representation as self-evolution expands |
| PM-10 | Meta-transition requires refinement proof | `MetaAdmission` unifies K0 + refinement + closure; FixedPoint remains descriptive | COMPLETE (executable contract scope) | T24–T29 | Distinguish witness evidence from universal proof; strengthen only if required by formal target |
| PM-11 | Resource/gas bound | `core/gas.py::GasBudget` provides deterministic finite charging and fail-closed exhaustion | PARTIAL→NEAR-COMPLETE | T23/T29 | Bind gas budget to canonical autonomous operation executor; prove no bypass |
| PM-12 | Append-only causal history H | `core/history.py::TransitionRecord` + `AppendOnlyHistory` enforce contiguous sequence and hash-linked append-only records | NEAR-COMPLETE | T30–T36 | Bind history append to canonical SemanticCommit; prove no mutation path |
| PM-13 | SQLite is persistence representation, not semantic truth | documented in AI_CONTEXT; no SQLite persistence module found | MISSING | T30–T36 | Implement after schema/acceptance definition |
| PM-14 | Replay(Genesis,History,KernelVersions)=State | tests cover trajectory reproducibility, but no canonical persistence replay found | PARTIAL | T30/T39 | Add replay object/contract |
| PM-15 | Snapshot != source of truth | conceptual only; no canonical snapshot module found | MISSING | T31 | Define snapshot certificate |
| PM-16 | Crash atomicity/idempotent commit | no canonical persistence commit layer found | MISSING | T35/T36 | Persistence phase |
| PM-17 | Kernel version attached to accepted transition | `TransitionRecord.kernel_version` required for accepted records | PARTIAL | T34/T39 | Bind record creation to canonical commit/persistence boundary |
| PM-18 | Evidence/provenance separated from semantic commit | bridge has provenance/authority concepts; Core proof has evidence mapping | PARTIAL | T13–T17 | Formalize evidence type and commit barrier |
| PM-19 | Hard stop when mandatory verification is unresolved | empty candidate/dead-end raises; fail-closed bridge exists | PARTIAL | T41 + stop semantics | Unify stop as explicit Core outcome |
| PM-20 | No external actor gets semantic commit authority | tests cover selector injection/external boundaries; no universal commit API proof | PARTIAL | T41 | Prove canonical commit boundary |
| PM-21 | Persistence/recovery cannot create hidden state | memory-independence tests exist; protected memory is documented GAP | PARTIAL | T30–T40 | Recover protected-memory specification |
| PM-22 | Formal machine-proof layer | no Lean/Coq proof tree found in repository tree | MISSING | T1–T41 | Create minimal formal-core proof target after code audit |

## Immediate evidence-backed gaps

1. Explicit Admission is now a first-class Core primitive for the proof-gated evolutionary path, but universal non-bypass is not yet proven.
2. Merge/conflict/resolution calculus has documentation but no canonical Core implementation was found.
3. Meta-kernel/root-invariant/refinement proof layer is not established as a concrete implementation.
4. Canonical persistence/history/replay/snapshot machinery is not established; current repository contains experiments and documentation rather than a confirmed SQLite state-history subsystem.
5. Machine-checked proof artifacts are absent from the current repository tree.
6. Protected internal memory remains a documented GAP and must be recovered before replacement design.

## Important non-findings

The absence of a search hit is not proof that a concept can never be implemented elsewhere. It means the current repository evidence did not establish a canonical implementation during this audit pass.

## Next task gate

Do not implement all gaps at once.

First resolve:
PM-05 Admission Boundary

Acceptance:
- one canonical semantic commit boundary exists;
- every accepted state mutation passes it;
- external bridge/AI/user/database paths cannot bypass it;
- adversarial regression tests demonstrate non-bypass;
- documentation and Task Registry identify the exact boundary.

Then re-audit PM-07–PM-22 against the resulting architecture.
