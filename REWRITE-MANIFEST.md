# Gnozis Clean-Room Rewrite Manifest

Status: ACTIVE
Architecture trigger: 2026-09-26

## Target
Replace the previous public repository architecture with the canonical Gnozis platform while preserving validated knowledge, evidence, provenance, and legal/ownership records through controlled migration.

## Migration rule
Audit → classify → extract contract/invariant → rewrite → test → verify → migrate.

Never bulk-copy the previous implementation into the new architecture.

## Source repositories
- Gnozis: public legacy/product material
- Gnozis-Exchange: merge relevant product concepts into Gnozis Platform; repository is not a target runtime
- Thoth/Athena/Hephaestus/Daedalus/Prometheus: audit and classify before archival; no automatic code adoption
- Gnozis-Core: private trusted runtime source; rewrite separately
- Gnozis-Genesis: private development source; rewrite separately
- Gnozis-Research-Memory: preserve research/audit/context material and restructure

## First implementation boundary
Public platform only. Core authority remains a separate private boundary.
