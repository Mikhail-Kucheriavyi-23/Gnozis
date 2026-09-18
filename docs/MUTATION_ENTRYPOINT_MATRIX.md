# Mutation Entry-Point Matrix — 2026-09-18

Status: audit artifact; not a proof claim.

| Entry point / surface | Intended role | Required gate | Current code finding | Remaining gap |
|---|---|---|---|---|
| `core/evolution.py::evolutionary_psi_transition` | canonical evolution | Proof → Admission → Select → SemanticCommit | **PASS (local path)**: constructs proofs, admissions, filters accepted candidates, then calls `commit(...).apply()` | prove every canonical caller uses this chain |
| `core/commit.py::SemanticCommit.apply` | semantic mutation boundary | `require_admitted` | **PASS (fail-closed)**: rejected admission cannot apply | enumerate all alternative mutation callers |
| `core/psi_transition.py::PsiTransition` | canonical Ψ transition surface | canonical function boundary | **PASS (typed surface)**; `on_state` is an adapter | audit callers and distinguish transition calculation from semantic commit |
| `core/legacy_engine.py::LegacyEngine` | compatibility path | must not become Ψ authority | **PASS (classified)** as legacy/compatibility | PM-02 remains because a competing State→State transition exists |
| `core/replay.py::replay` | history reconstruction | replay/provenance rules | **CLASSIFIED**: returns reconstructed Ψ; does not call SemanticCommit | prove replay cannot be treated as a live mutation authority |
| `core/snapshot.py` | observation/cache | never semantic authority | **PASS (documented)**; certificate-backed cache | runtime invalidation/recovery binding |
| `core/merge.py::merge` | candidate/conflict construction | Admission before commit | **PASS (candidate-level)**; conflict yields no candidate | adversarial test that merge output cannot bypass admission |
| `core/refinement.py` | verification/comparison | no direct semantic authority | **CLASSIFIED**: witnesses transitions, does not commit | ensure refinement API cannot be used as commit path |
| `core/authority.py` | external evidence | provenance + admission | **PASS (local contract)**: foreign evidence returns `admitted=False` | audit all external input paths |

## Acceptance rule

A mutation path is canonically safe only when: (1) identified; (2) classified; (3) canonical semantic mutation requires Admission; (4) rejected Admission fails closed; (5) path cannot independently manufacture a committed Ψ; (6) runtime/adversarial coverage exists where bypass is plausible.

## Current conclusion

The direct canonical path inspected here is correctly gated. The repository still does **not** justify the universal statement `all semantic mutation paths require Admission`: the legacy State→State surface remains a competing transition path, while replay, merge, refinement, snapshot, and external-input callers need explicit adversarial coverage where they could influence canonical state.

This matrix intentionally does not convert scoped/near-complete statuses in `PROOF_MATRIX.md` into universal guarantees.
