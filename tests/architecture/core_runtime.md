# Core Runtime Test Targets

- State objects are immutable.
- A transition referencing another source state is rejected.
- Missing transition identity is rejected.
- A rejected verification result never reports acceptance.
- Verification cannot accept a transition whose source does not match the current state.
- Commit cannot occur after failed verification.
- Successful commit creates a new immutable state with incremented version.
- Persistence rejects state records without an integrity digest.
- Persisted state can be retrieved by stable state identity.
