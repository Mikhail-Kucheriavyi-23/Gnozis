# Research Machine Transfer Manifest R1

Status: INVENTORY_COMPLETE / TRANSFER_DESIGN
Purpose: define the controlled migration from legacy Gnozis research material into Gnozis-Research-Memory.

## Transfer classes
- TRANSFER: active machine-readable learning/evidence material.
- TRANSFER-REVIEW: useful material requiring normalization or conflict review.
- KEEP-CORE: operational runtime code/tests that must remain in Core.
- ARCHIVE: historical material retained for provenance but excluded from active retrieval.
- EXCLUDE: duplicate, obsolete, or unsupported material.

## Priority order
1. research_machine/records/* — primary knowledge/evidence corpus.
2. research_machine/INDEX.yaml and schemas — corpus index and validation rules.
3. verified contracts, invariants, mathematical definitions and proofs.
4. counterexamples, audits, provenance and runtime evidence.
5. research/* and structured AI context — normalize into atomic records.
6. decisions and evolution history.
7. raw historical context — preserve separately, never use as authoritative knowledge.

## Required record fields
memory_id
type
status
content
source
source_sha
provenance
related_contracts
related_math
related_counterexamples
core_relevance
promotion_state

## Promotion states
RAW -> REVIEW -> VERIFIED -> RETRIEVABLE -> CANDIDATE_SOURCE -> SHADOW_ONLY -> CORE_ELIGIBLE

No Research-Memory record directly mutates Core.

## Next
Generate a machine-readable inventory from this manifest, normalize records, resolve duplicates/conflicts, then migrate the selected corpus into the dedicated Gnozis-Research-Memory repository.
