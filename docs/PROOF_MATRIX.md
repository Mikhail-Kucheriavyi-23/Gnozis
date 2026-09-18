# Gnozis Proof Matrix — 2026-09-18

Status: first evidence-backed mapping after Mathematical Freeze (CLXI–CLXIV).

Legend:
- IMPLEMENTED: code exists and repository evidence directly supports the contract.
- PARTIAL: a boundary/approximation exists, but the full mathematical contract is not established.
- MISSING: no corresponding implementation was found in the current repository tree/search.
- UNVERIFIED: implementation/tests exist, but the current tool pass did not execute the suite.

This document is an audit map, not a proof claim.

| ID | Requirement | Evidence | Status | Remaining |
|---|---|---|---|---|
| PM-01 | Psi=(X,R) core | core/state.py::Psi | IMPLEMENTED | typed X/R |
| PM-02 | State is adapter | adapter paths | PARTIAL | remove competing transition path |
| PM-03 | Deep immutability | recursive freeze | IMPLEMENTED* | custom payload boundary |
| PM-04 | Generate→Test→Proof/Admission→Select→Transition | evolution/proof stack | PARTIAL | explicit admission separation |
| PM-05 | Apply cannot bypass Admission | canonical Ψ path | COMPLETE(scope) | regression |
| PM-06 | Selection not external oracle | endogenous selection | PARTIAL | universal proof |
| PM-07 | Partial-order branches | Branch/ParallelOutcome | COMPLETE(scope) | regression |
| PM-08 | Conflict retained | Conflict/Resolution/DeferredConflict | COMPLETE(scope) | regression |
| PM-09 | Protected K0 | RootInvariant/MetaTransition | COMPLETE(scope) | kernel binding |
| PM-10 | Meta refinement | MetaAdmission | COMPLETE(contract) | machine-proof semantics |
| PM-11 | Gas bound | GasBudget | NEAR-COMPLETE | executor/no bypass |
| PM-12 | Append-only history | AppendOnlyHistory | NEAR-COMPLETE | SemanticCommit binding |
| PM-13 | SQLite representation, not truth | no SQLite implementation | MISSING | persistence phase |
| PM-14 | Deterministic replay | replay() | NEAR-COMPLETE | kernel dispatch + hash equality |
| PM-15 | Snapshot != truth | SnapshotCertificate | NEAR-COMPLETE | replay binding/invalidation |
| PM-16 | Crash atomicity/idempotence | commit_once() | NEAR-COMPLETE | durable crash tests |
| PM-17 | Kernel/provenance attached | TransitionRecord + Provenance | NEAR-COMPLETE | commit binding |
| PM-18 | Evidence separated from commit | provenance contract | NEAR-COMPLETE | integration |
| PM-19 | Hard stop unresolved | `canonical_chain.admit_transition` gates Safety + Gas before commit | NEAR-COMPLETE | prove all operation paths use chain |
| PM-20 | External actor no authority | `authority.py` + provenance/commit boundary | NEAR-COMPLETE | route all external paths |
| PM-21 | Protected kernel/workspace | `memory.py` boundary remains separate from commit chain | NEAR-COMPLETE | bind protected state/persistence |
| PM-22 | Machine-checked proof | formal/MinimalCore.lean | PARTIAL | real definitions + invariant proof |

## Reconciliation result

This table supersedes the stale status table. PM-11–PM-21 now have executable contract evidence; PM-22 has an initial machine-proof target. These are not universal proofs.

Critical remaining gaps:
1. PM-13 persistence representation is absent by design.
2. PM-11–PM-21 still need canonical integration plus adversarial/no-bypass/crash/recovery tests where applicable.
3. PM-22 must replace placeholder propositions with actual Core definitions and prove invariant preservation.
4. PM-02, PM-04 and PM-06 remain independent formal/architectural gaps.