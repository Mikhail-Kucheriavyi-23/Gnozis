# Recovered Historical Audit — 2026-09-10

This document records findings recovered from archived ChatGPT project material. It is intentionally limited to evidence actually found; unresolved historical claims remain marked as gaps.

## Recovered engineering findings

1. `Uroboros()` had an identity-transition default. Historical execution showed `u.step().state == u.state`.
2. `Uroboros.with_relations()` accepted relations and discarded them; historical execution showed state relations remained empty.
3. `Engine.run()` / `trajectory()` accepted `bool` as `int` (`True == 1`).
4. `select_next_state()` accepted arbitrary truthy values from `Test`; historical execution showed `lambda s: "yes"` accepted a candidate.
5. `State.evolve()` performed only a shallow copy, permitting nested mutable aliasing despite `frozen=True`.
6. Two independent `PsiTransition` implementations existed with different interfaces/semantics, creating multiple sources of truth.
7. `Relation` existed as a type but was not actually represented as the formal `R` of the live `State` contract.
8. `CoreChat` used mutable `_pending_message` as hidden transition input, violating state sufficiency/endogenous transition requirements.
9. `ThreadingHTTPServer` shared mutable chat state across requests without synchronization.
10. `default_chat_transition` used role `core` for a canned response, risking confusion between core output and AI-adapter output.
11. Bridge identity handling historically defaulted missing `authenticated` to `True` (fail-open); intended repair is fail-closed.
12. `/health` historically reported core readiness without verifying an actual working core transition.
13. The Ψ boundary existed partly as isolated tests while the live Engine/Uroboros/Evolution path remained based on an untyped `Mapping[str, Any]` state.

## Recovered architectural direction

- Use one explicit typed Ψ representation (`X` and `R`) rather than string-key conventions inside an untyped dictionary.
- Keep Domain/Ψ-Core independent of HTTP, GitHub, Worker, terminal and AI adapters.
- Treat Generator/Tester/Selector/Transition as explicit ports/contracts.
- Keep Test contract strict: `Test(candidate) -> bool`.
- Prefer a single source of truth for transition and selection logic.
- Property-based testing (e.g. Hypothesis) was proposed to strengthen hidden-state/extensionality tests.
- Mutation testing and an independent conformance suite were proposed as stronger verification mechanisms.
- Do not equate engineering conformance with scientific novelty; prior-art comparisons identified generate-and-test, genetic programming, model/state formalisms, and Gödel-machine-like proof-before-change as relevant neighbors.

## Memory-specific recovery status

Recovered:
- Memory was discussed as a historical trace/derived information rather than automatically as a new fundamental primitive.
- Memory provenance and integrity are recognized as architectural requirements.
- Hidden memory/state channels are prohibited when they influence transition.

Not recovered yet:
- the exact cryptographic construction from the user's forwarded Gnozis proposal;
- exact equations for encrypted/protected memory;
- exact key/nonce construction;
- exact authenticated-memory/reconstruction protocol.

These remain `GAP` and must not be replaced by an invented design and labeled as historical.

## Scientific audit branches that must remain tracked

- attractors and effective dimension;
- Bell/nonlocality;
- holographic/information bounds;
- path algebra/GNS/Born rule;
- Lorentz invariance and LIV;
- Lyapunov-like monotonicity and irreversibility;
- alpha≈137 exploration;
- SU(2)×SU(3);
- E8;
- causal DAG;
- information-memory geometry;
- Green–Schwarz anomaly / island-topology experiment;
- large sparse `PsiCorev33InfinityEngine` stress test;
- spectral collision analysis.

## Recovery rule

A result is marked recovered only when supported by archived primary material. A result reconstructed from memory or inference must be labeled `RECONSTRUCTED`. A planned implementation is not a completed implementation.
