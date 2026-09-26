# Core Runtime Test Targets

- State objects are immutable.
- A transition referencing another source state is rejected.
- Missing transition identity is rejected.
- A rejected verification result never reports acceptance.
- Verification cannot accept a transition whose source does not match the current state.
