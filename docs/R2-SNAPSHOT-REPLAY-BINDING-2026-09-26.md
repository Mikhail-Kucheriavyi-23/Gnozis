# R2 Snapshot Replay Binding — 2026-09-26

## Gap

SnapshotCertificate already separated snapshots from semantic truth, but the certificate could be checked only against caller-supplied metadata. It did not directly bind acceptance to the state reconstructed by replay.

## Runtime contract

A snapshot is a usable cache only if all three certificate dimensions remain valid and its state hash equals the digest of the actual replayed Psi:

- history_head matches the current history head identifier;
- state_hash equals SHA-256 of the replayed canonical Psi;
- kernel_version matches the active kernel version.

If any dimension changes, the snapshot is stale and must not be consumed as a certified cache. `invalidate_if_stale()` therefore returns the snapshot only when replay and certificate agree; otherwise it returns None.

The snapshot remains observational/cache state. It does not become semantic authority and does not write to history.

## Adversarial evidence

Tests cover replayed-state substitution, history-head change, kernel-version change, and non-Psi replay input.

## Scope

This closes the PM-15 replay-binding/invalidation contract. It does not implement durable SQLite persistence or crash recovery; PM-13/PM-16 remain separate infrastructure boundaries.
