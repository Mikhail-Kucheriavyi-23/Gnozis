# Genesis Provenance Experiment — GPE-01

**Date:** 2026-09-24
**Status:** ACTIVE — experimental / non-legal
**Depends on:** MRM-01, MRM-03

## Objective
Construct the first machine-readable provenance graph for the accessible Gnozis development history from 2026-09-01 onward, using only evidence that can be lawfully accessed and retained.

## Evidence hierarchy
1. Git commits/releases and repository metadata.
2. Repository documents and explicit audit records.
3. Contract records.
4. Clearly attributed external audit statements.
5. Conversation-derived design decisions only where a durable project artifact records the decision.

Do not reconstruct missing history by inference.

## Node classes
QUESTION, HYPOTHESIS, AUDIT, DECISION, CONTRACT, ARTIFACT, COMMIT, TEST, VERIFICATION, CONTRIBUTION, OUTCOME.

## Edge classes
MOTIVATED_BY, REFINES, CONSTRAINS, IMPLEMENTS, VERIFIES, DERIVES_FROM, DEPENDS_ON, SUPERSEDES.

## Record
Each node should minimally contain: stable ID; type; source reference; timestamp if evidenced; actor reference only where evidenced; permission/legal-status label; content digest; parent/edge references; verification state.

## Hashing
Use deterministic canonical serialization before hashing. Prefer SHA-256 for the initial experiment. Record algorithm and canonicalization version. Never hash ambiguous textual representations as if they were canonical.

## Privacy
Do not include raw personal data, secrets, credentials, private messages, or restricted third-party material. Where an actor reference is needed, use the minimum necessary pseudonymous identifier unless public attribution is clearly appropriate.

## AI contribution
Do not infer legal authorship from AI involvement. Record AI-assisted generation as process provenance only.

## Output
Produce: (1) Genesis timeline; (2) Provenance DAG; (3) Contribution/evidence table; (4) Hash manifest; (5) Uncertainty register; (6) Missing-evidence register; (7) Candidate provenance schema for future partner repositories.

## Integrity test
Recomputing the canonical representation must reproduce the same digest. Any changed source must produce a different digest.

## Acceptance
GPE-01 is complete when a third party can reproduce the graph and hashes from the cited lawful source artifacts, while every inferred or legally uncertain relationship is explicitly marked.

## Non-goals
No ownership assignment, valuation, royalty calculation, legal authorship determination, or commercial entitlement is created by this experiment.
