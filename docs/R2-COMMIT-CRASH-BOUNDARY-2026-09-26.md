# R2 Commit Crash-Boundary Contract — 2026-09-26

## Finding

`commit_once()` provides idempotence and conflict detection for an immutable in-memory `AppendOnlyHistory`, but it does not by itself model where a crash can occur between preparation, history append, and publication of the new state.

## Minimal contract

The canonical commit boundary is therefore represented as explicit phases:

`PREPARE -> APPEND -> PUBLISH`

- PREPARE validates that the record is exactly the next causal record and points to the current head.
- APPEND creates the next immutable history value.
- PUBLISH exposes the next semantic value only together with the appended history.

A crash before APPEND leaves the original immutable history unchanged. A crash after APPEND but before an external publication must retain the appended history as the authoritative durable result once a durable store exists; this property is not yet implemented by the current in-memory model.

## Important limitation

This change is a crash-boundary contract/state model, **not yet durable crash recovery**. It does not claim filesystem/SQLite transaction atomicity, fsync durability, process-crash recovery, or cross-record persistence guarantees.

Those require the persistence layer and an injected failure harness against the actual durable backend.

## Adversarial evidence

Tests cover invalid sequence preparation, immutability of pre-append history, rejection of publishing a different head, and publication only after the prepared record has been appended.
