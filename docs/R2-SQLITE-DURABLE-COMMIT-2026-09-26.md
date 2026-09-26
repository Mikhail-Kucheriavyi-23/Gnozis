# R2 SQLite Durable Commit Boundary — 2026-09-26

## Runtime contract

The durable history boundary is:

`validate -> BEGIN IMMEDIATE -> INSERT -> COMMIT -> reload/recover`

Only the SQLite transaction changes durable history. The in-memory semantic value is not considered durably published merely because preparation succeeded.

## Failure semantics

- failure before transaction: no durable mutation;
- failure before INSERT: transaction is rolled back;
- failure after INSERT but before COMMIT: transaction is rolled back;
- failure after COMMIT: the record remains durable even if the caller never publishes the returned semantic value;
- retry of the same sequence/state hash is idempotent and returns the recovered durable history rather than appending a duplicate.

On process restart, `SQLiteHistoryStore.load()` reconstructs `AppendOnlyHistory` through its normal causal-chain validation. A broken durable chain therefore fails closed during recovery.

## Evidence

Injected-failure tests cover all three meaningful crash positions, restart recovery, retry idempotence, and conflicting same-sequence records.

## Boundary

This establishes durable history atomicity. It does not make SQLite the semantic authority: Core's verification/admission/commit path remains authoritative, while SQLite is the durable persistence substrate. It also does not claim OS-level filesystem durability beyond SQLite's successful transaction semantics.
