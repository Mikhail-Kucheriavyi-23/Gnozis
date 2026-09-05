from core import State, Uroboros

def test_uroboros_evolution():
def increment(state: State) -> State:
value = state.values.get("x", 0)

```
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

result = system.run(10)

assert result.values["x"] == 10


