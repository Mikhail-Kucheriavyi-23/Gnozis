from core import State, Uroboros


def increment(state: State) -> State:
    """Increment x by one."""
    value = state.values.get("x", 0)

    return state.evolve(
        values={
            **state.values,
            "x": value + 1,
        }
    )


system = Uroboros(
    initial_state=State(values={"x": 0}),
    rules=[increment],
)

result = system.run(steps=10)

print("Final state:", result.values)
