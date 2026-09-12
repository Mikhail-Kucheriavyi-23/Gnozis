# No-input self-support gate

This experiment removes continuous external input after a finite initialization pulse.

Protocol:

1. Initialize a finite state `X0`.
2. Provide the initial pulse only through the initial state.
3. Set external input to zero for all subsequent steps.
4. Propagate only through the current relation structure `R`.
5. Record activity and structural viability over time.

Interpretation:

- activity dies immediately: no recurrent persistence;
- activity persists briefly then dies: transient recurrence;
- activity persists for the full observation window: candidate recurrent self-support;
- after perturbation, the organization restores activity without external input: stronger candidate for self-maintaining organization.

This experiment does not establish autopoiesis by itself. The current model has no metabolism, boundary, or resource regeneration. It tests only whether local relational dynamics can maintain their own activity after external drive is removed.
