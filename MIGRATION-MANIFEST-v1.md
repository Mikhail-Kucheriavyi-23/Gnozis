# GNOZIS Migration Manifest v1

Status: FROZEN FOR REVIEW
Manifest ID: GNOZIS-MIGRATION-MANIFEST-V1-2026-09-25
Source repository: Mikhail-Kucheriavyi-23/Gnozis
Source baseline: 03b92113e6d2cc2801e4f59a2a8f1c4fc285ccc3
Migration mode: provenance-preserving, staged
Physical migration: NOT STARTED

## Repository topology

| Repository | Scope | Visibility |
|---|---|---|
| Gnozis | Public product, opportunity, partner/tester surface | Public |
| Gnozis-Core | Operational runtime core, invariants, executable verification | Public |
| Gnozis-Exchange | Internet Port, external sources, connectors, market integrations | Public |
| Gnozis-Research-Memory | Research, formal history, evidence, provenance, machine context | Public/controlled |
| Gnozis-Genesis | Proprietary Module Factory and commercial/private implementation | Private |

## Non-negotiable boundary rules

1. Any artifact that may contain commercially valuable implementation, data, strategy, credentials, proprietary algorithms, or private module logic is PRIVATE/QUARANTINE until explicitly classified.
2. Gnozis-Core is authoritative for operational state transition, admission, selection, evolution, and commit semantics.
3. Gnozis-Exchange may ingest and normalize external information but must not acquire Core authority.
4. Gnozis-Research-Memory stores evidence, research, provenance, historical context, and machine-readable reasoning; it is not Core authority.
5. Gnozis-Genesis is not a dependency of Gnozis-Core.
6. No artifact is physically removed from the source until its target copy is verified.
7. No duplicate artifact may remain as two canonical authorities.
8. Historical evidence is not equivalent to runtime correctness.
9. Every migrated artifact must retain provenance: source path, source revision, target path, action, and verification status.
10. Unknown or legally ambiguous artifacts go to QUARANTINE, not public repositories.

## Domain mapping

### Gnozis-Core

Target:
- core/
- operational formal proofs and contracts
- Core invariant/admission/selection/commit tests
- adversarial Core tests
- Core security/bypass tooling
- Core CI
- Core operational documentation

Known candidates:
- formal/AdmissionCommit.lean
- formal/CanonicalBoundary.lean
- formal/FullTransition.lean
- formal/MinimalCore.lean
- formal/ProofGate.lean
- formal/PsiInvariants.lean
- formal/RootInvariant.lean
- formal/RuntimeConformance.lean
- formal/SelectionCommitBridge.lean
- formal/StatePsi.lean
- formal/TestAdmissionBridge.lean
- tools/bypass_scan.py
- tools/import_bypass_scan.py

Action: MOVE/REWRITE after dependency verification.

### Gnozis-Exchange

Target:
- gnosis-terminal-bridge/
- Internet Port
- external adapters
- external/market connectors
- integration/port tests
- Exchange CI

Known boundary candidates:
- core_adapter.py -> Exchange adapter
- core_chat.py -> Exchange integration
- core_evolution.py -> Exchange boundary adapter; rename/rewrite
- autonomous_selection.py -> NOT Exchange authority; Core audit candidate

Action: SPLIT/REWRITE by authority boundary.

### Gnozis-Research-Memory

Target:
- AI_CONTEXT.md
- historical audits
- research notes
- mathematical research not yet promoted to Core contracts
- provenance/history artifacts
- philosophy/context material
- claims/evidence registry
- historical project state
- research validation

Known candidates:
- provenance/GPE-01_INITIAL_MANIFEST.md
- contracts/MRM-01_MATHEMATICAL_REVERSE_MAPPING.md
- contracts/MRM-03_LEGAL_AVAILABILITY_PROVENANCE_EXPERIMENT.md
- AI_CONTEXT.md
- GNOZIS_MASTER_AUDIT.md
- PHILOSOPHY.md
- PROJECT_STATE.md
- RECOVERY_GAPS_2026-09-10.md
- RESEARCH_SOURCES.md
- historical audit documents

Action: MOVE, preserving evidence identity.

### Gnozis

Target:
- public README/product registry
- public opportunity surface
- public discovery policy
- public partner/tester documentation
- approved public outputs
- product roadmap

Action: REWRITE/SELECTIVE COPY only. Do not expose private implementation.

### Gnozis-Genesis

Target:
- proprietary modules
- commercial Module Factory
- private evolution
- proprietary algorithms
- private datasets
- commercial credentials/secrets
- private opportunity-generation implementation

Action: PRIVATE/QUARANTINE until explicit classification. No automatic extraction from current public repository.

## Formal artifact rule

A mathematical artifact becomes a Core authority only when the chain is established:

definition -> formal contract -> implementation mapping -> executable test/evidence.

Formalization alone does not prove runtime conformance.

## Cross-repository flow

External source / market
-> Gnozis-Exchange
-> validation / normalization / provenance
-> Gnozis-Core
-> verified result
-> Gnozis public surface and/or Research-Memory evidence.

Genesis remains isolated. Only explicitly approved public outputs may cross from Genesis to Gnozis.

## Migration transaction

For each artifact:

SOURCE
-> source revision/hash
-> target copy
-> dependency check
-> tests
-> provenance record
-> source removal only after verification.

## Legal gate

License, copyright, trademark, and commercial-use documents are not copied mechanically between repositories. Their scope must be reviewed against the final repository boundary before public migration.

## Freeze criteria

Migration Manifest v1 may be considered implementation-ready when:
- every source domain has a target or QUARANTINE state;
- no unknown commercial artifact remains unclassified;
- legal scope is explicitly assigned;
- cross-repository dependencies are recorded;
- target repositories exist or are scheduled for creation;
- provenance verification procedure is agreed.

Current state: architecture frozen; legal scope remains PARTIAL; physical migration is NOT STARTED.
