# Transition Contract v1

Transition represents an attempted change from one valid state to another.

Flow:
Candidate → Test → Select → Evolve → Verify → Commit

Rejected transitions do not become committed state. Verification failure is fail-closed for trusted operations.

## Required trace
A transition identifies its source state, candidate, verification result, and resulting state when committed.