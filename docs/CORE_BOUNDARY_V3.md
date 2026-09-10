# Core boundary v3

## Contract

The fundamental state is Ψ = (X, R).

- `X` is the system content/state payload.
- `R` is an immutable finite collection of `Relation` objects.
- `State` remains the compatibility/application wrapper.
- `State.to_psi()` is the explicit projection to the mathematical core.
- `State.from_psi()` is the explicit adapter back to the application wrapper.

This stage deliberately does not move higher-level AI, worker, GitHub, or I/O concerns into the core.

## Invariants

1. A `Psi` instance is immutable.
2. Relations are stored as an immutable tuple.
3. Every relation in `Psi.R` is a `Relation`.
4. `State.to_psi()` rejects states that do not explicitly contain both `x` and `relations`.
5. `State.from_psi(State.to_psi(s))` preserves the fundamental `X` and `R` values.
6. The legacy `State.values` API remains only as an adapter surface during migration.

## Next gate

After these invariants are green, the next refactor may change the Engine contract from `State -> State` to `Psi -> Psi`, with `State` kept at the outer compatibility boundary. That change should happen only after all existing consumers are mapped.
