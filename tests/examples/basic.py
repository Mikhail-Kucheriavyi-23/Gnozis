from core import Engine, State, Uroboros


def increment(state: State) -> State:
    value = state.values.get("x", 0)

    return state.evolve(
        values={
            **state.values,
            "x": value + 1,
        }
    )


engine = Engine(transition=increment)

system = Uroboros(
    state=State(values={"x": 0}),
    engine=engine,
)

for _ in range(10):
    system = system.step()

print("Final state:", system.state.values)

