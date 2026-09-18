# Mutation Entry-Point Matrix — 2026-09-18

Status: audit artifact; not a proof claim.

| Entry point / surface | Intended role | Required gate | Evidence available | Remaining gap |
|---|---|---|---|---|
| `core/evolution.py` | canonical evolution | Proof → Admission → Select → SemanticCommit | PROOF_MATRIX PM-04/PM-05 | prove every caller stays on canonical chain |
| `core/commit.py` | semantic mutation boundary | `require_admitted` | PM-05 + fail-closed regression | enumerate every alternative mutation caller |
| `PsiTransition` | canonical Ψ transition | admitted candidate | PM-01/PM-04 | runtime caller coverage |
| `legacy_engine.py` | compatibility path | must not become Ψ authority | PM-02 | eliminate/contain competing transition semantics |
| `replay.py` | history reconstruction | provenance/hash/replay rules | PM-14/PM-15 | prove replay cannot mutate canonical truth |
| snapshot/representation surfaces | observation/storage | never semantic authority | PM-13/PM-15 | bind to canonical commit chain |
| external/authority paths | external input | provenance + authority boundary | PM-20 | prove all external paths route through canonical admission |

## Acceptance rule

A mutation path is canonically safe only when: (1) identified; (2) classified as canonical, compatibility, replay, or representation; (3) canonical semantic mutation requires Admission; (4) rejected Admission fails closed; (5) path cannot independently manufacture committed Ψ; (6) runtime/adversarial coverage exists where bypass is plausible.

## Current conclusion

The repository has direct evidence for the canonical commit gate, but the universal statement `all semantic mutation paths require Admission` remains **unproven** until the complete caller/path inventory and adversarial coverage are established.

This matrix intentionally does not convert scoped/near-complete statuses in `PROOF_MATRIX.md` into universal guarantees.
