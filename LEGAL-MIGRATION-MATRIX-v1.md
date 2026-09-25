# GNOZIS Legal Migration Matrix v1

Status: PRE-IMPLEMENTATION REVIEW
Baseline: 03b92113e6d2cc2801e4f59a2a8f1c4fc285ccc3
Scope: existing root legal/rights artifacts only

## Findings

| Source artifact | Observed role | Proposed canonical scope | Migration action | Gate |
|---|---|---|---|---|
| COMMERCIAL-LICENSE | commercial authorization framework | legal-controlled / Genesis-facing; public reference only if intentionally published | REVIEW + REWRITE | legal review |
| COMMERCIAL-LICENSE.md | short commercial notice | public commercial notice or legal-controlled reference | REWRITE | legal review |
| LICENSE-RESEARCH | research-use license | public research repositories where applicable | REVIEW + REWRITE | legal review |
| LICENSE-RESEARCH.md | short research/commercial notice | public repository notices where applicable | REWRITE | legal review |
| COPYRIGHT.md | content appears to be trademark/project identity policy, not copyright notice | quarantine pending correction | QUARANTINE + RECONCILE | source/document mismatch |
| TRADEMARKS | trademark/project identity policy | legal-controlled master + public notices as applicable | REVIEW + REWRITE | legal review |
| TRADEMARKS.md | short trademark/naming notice | public repository notice as applicable | REWRITE | legal review |

## Critical source inconsistency

COPYRIGHT.md currently contains a GNOSIS trademark/project-identity document rather than a conventional copyright statement. This must not be silently propagated. Its filename/content mismatch is a provenance and legal-documentation defect.

Required action:
1. preserve the current file as historical evidence;
2. create a correctly scoped copyright notice only after legal review;
3. do not treat COPYRIGHT.md as the authoritative trademark policy;
4. keep trademark policy under a single canonical owner.

## License architecture to resolve

The current documents state a research/non-commercial access model and separate commercial authorization. They also contain broad definitions of Commercial Use. Before publishing five repository-specific licenses, determine:
- which exact artifacts are covered;
- whether the same license applies to Core, Exchange and Research-Memory;
- whether public Gnozis is software, documentation, or product-surface scope;
- whether Genesis contains independently created/proprietary material;
- how third-party dependencies remain separately licensed;
- how future repository additions are covered.

No new legal restriction should be inferred solely from repository separation.

## Repository treatment

### Gnozis
Use only public-facing terms actually applicable to the public product surface. Do not copy the private commercial agreement framework wholesale.

### Gnozis-Core
Use an explicit software license/notice applicable to the Core source. Preserve attribution and third-party license requirements.

### Gnozis-Exchange
Use terms applicable to connectors/integration code and clearly preserve third-party API/data-provider terms.

### Gnozis-Research-Memory
Use terms appropriate to research/evidence/documentation artifacts. Individual third-party sources may have separate rights.

### Gnozis-Genesis
Private repository. Do not infer that public Research License terms grant rights to proprietary Genesis material. Establish private ownership/licensing terms separately.

## Non-negotiable provenance rule

Legal documents are not interchangeable copies. Every repository-level legal file must have:
- canonical owner;
- source revision;
- applicable artifact scope;
- effective date;
- relationship to third-party licenses;
- explicit public/private status.

## Current blockers

1. COPYRIGHT.md filename/content mismatch.
2. Repository-specific license scope is not yet legally reviewed.
3. Trademark rights must not be stated as registered unless independently verified.
4. Commercial licensing language should remain an authorization framework, not be presented as a signed agreement.
5. Genesis proprietary rights require separate scope definition.

## Implementation gate

Technical repository creation/migration may proceed with legal artifacts quarantined, but no final public legal publication should occur until the above blockers are reviewed.

Status: LEGAL MATRIX DRAFT COMPLETE; LEGAL REVIEW REQUIRED.
