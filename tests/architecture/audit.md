# Audit Chain Test Targets

- First record links to GENESIS.
- Each record links to the previous record digest.
- Records are exposed as an immutable sequence.
- Audit records retain operation identity and event type.
- A missing or conflicting chain link must fail verification before trusted recovery.
