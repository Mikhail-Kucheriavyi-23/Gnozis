# Gnozis Core

The trusted runtime boundary of Gnozis.

## Public surface

- State / Transition: immutable runtime model
- commit: fail-closed state transition
- Persistence / recover: integrity-checked storage and recovery
- ProvenanceRecord: operation provenance model
- AuditChain: append-only audit boundary
- state_digest: deterministic state identity

This package is intentionally small. Product services, knowledge repositories, research ingestion, commercial workflows, discovery, external models, and integrations remain outside the trusted Core boundary.
