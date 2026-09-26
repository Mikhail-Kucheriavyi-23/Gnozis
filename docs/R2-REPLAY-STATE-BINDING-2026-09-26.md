# R2 Replay State-Binding Contract — 2026-09-26

## Gap

Replay previously accepted an explicit applier and reconstructed states, but it did not verify that each reconstructed state matched the persisted TransitionRecord hashes. A malicious or incorrect applier could therefore produce a different state while replay still reported success.

## Runtime contract

For every accepted history record:

1. sequence must equal its position in history;
2. for every non-first record, the current reconstructed state digest must equal previous_hash;
3. the explicit applier must return Psi;
4. the resulting state digest must equal state_hash;
5. candidate_hash must equal state_hash;
6. any mismatch fails closed.

The first record uses the explicit genesis predecessor marker; the current genesis-state digest is not silently substituted for that marker.

Therefore the reconstructed state is hash-bound to each persisted record and each non-genesis predecessor.

Replay remains reconstruction only. It does not call SemanticCommit and cannot become a semantic mutation authority.

## Adversarial evidence

Tests now cover valid multi-record reconstruction with real state hashes, state substitution returned by the applier, predecessor/hash substitution between records, explicit-applier requirement, and empty-history behavior.

## Scope

This closes the specific replay-to-state hash-binding gap. It does not claim complete durable persistence, crash recovery, snapshot invalidation, or universal mutation-path closure.
