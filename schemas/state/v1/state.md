# State Contract v1

State is the authoritative representation of the Core runtime at a versioned point.

A state transition must be explicit, deterministic where the contract requires it, validated, and attributable to an authorized operation.

State must not depend on wall-clock time, hidden globals, external selectors, or an LLM decision inside the trusted transition path.