# Core Boundary Test Targets

- Platform cannot mutate trusted Core state without the Core contract.
- Core has no runtime dependency on UI, GitHub, payment provider, or LLM.
- Rejected transitions cannot become committed state.
- Verification failure cannot silently commit a transition.
- A state transition is traceable through provenance and integrity evidence.
