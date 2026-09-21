# Gnozis Research Library — Machine-Readable Index

## Repository role
This repository is the public research library for Gnozis. It preserves research, reverse-analysis, mathematical models, experiments, historical implementations and provenance. It is not the canonical production Core.

## Canonical lineage
Research Library → Gnozis Core → specialized research kernels → user/commercial versions.

## Admission rule
Research does not become Core functionality merely by being documented. The engineering path is:
Observation → Pattern → Formalization → Evidence → Engineering Consequence → Core Requirement → Task → Implementation → Test/CI → Audit → Acceptance.

## Stable record schema
Each research record should use a stable ID and, where applicable, fields:
- ID
- TYPE
- PARENT
- QUESTION
- OBSERVATION
- DERIVATION
- RESULT
- EVIDENCE
- ENGINEERING_CONSEQUENCE
- GAP
- CORE_ADMISSIBILITY
- STATUS
- NEXT

## Status vocabulary
RESEARCH
HYPOTHESIS
FORMALIZED
EVIDENCE_PENDING
ENGINEERING_CANDIDATE
IMPLEMENTED
TESTED
CI_VERIFIED
AUDITED
ACCEPTED
REJECTED
SUPERSEDED

These statuses must not be conflated.

## Existing research continuity
The historical AI_CONTEXT.md remains a source document. Its mathematical and reverse-analysis material is being normalized into stable research records rather than duplicated into Core.

## Priority
Preserve provenance and useful discovery context; remove ambiguity and duplicate operational instructions.

## Current engineering bridge
Research should reference engineering tasks when a concrete consequence exists. Engineering tasks should reference source files, tests and audit evidence.

## Next
Normalize the existing E-series/reverse-analysis sequence into this index and record format.