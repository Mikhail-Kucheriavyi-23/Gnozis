# Temporal persistence gate

Structural connectivity is not enough. This experiment asks whether an organization remains dynamically active across time using its current relations.

For each step t, record:

`X_t, R_t, V_t`

where `V_t` is the structural viability diagnostic.

The experiment must distinguish:

1. **Transient activity** — activity disappears without continuing input.
2. **Driven persistence** — activity continues only because external input is continuously supplied.
3. **Recurrent persistence** — existing relations sustain activity after a finite initial input.
4. **Self-support** — the organization regenerates conditions needed for continued activity and remains viable after perturbation.

The current implementation measures persistence but does not claim category 4. A future experiment must explicitly remove external input after initialization and test whether activity and viability persist.
