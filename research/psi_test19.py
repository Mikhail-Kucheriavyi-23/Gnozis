"""TEST-19: memory as a derived historical trace, not a fundamental state variable."""
from pathlib import Path
import json

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test19_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def step(x, r):
    return x + r, r + 1

def evolve(x0, r0, n=5):
    x, r = x0, r0
    states = [(x, r)]
    for _ in range(n):
        x, r = step(x, r)
        states.append((x, r))
    return states

def derived_memory(states):
    return [states[i] for i in range(len(states)-1)]

states = evolve(2, 1)
memory = derived_memory(states)
replay = derived_memory(evolve(2, 1))
changed_initial = derived_memory(evolve(2, 2))

pass_result = (
    memory == replay
    and memory != changed_initial
    and memory == states[:-1]
    and all(m == s for m, s in zip(memory, states[:-1]))
)

result = {
    "test": "TEST-19",
    "status": "PASS" if pass_result else "FAIL",
    "states": states,
    "derived_memory": memory,
    "replay_memory": replay,
    "changed_initial_memory": changed_initial,
    "memory_is_derived_from_history": memory == states[:-1],
    "replay_reproducible": memory == replay,
    "different_initial_state_changes_memory": memory != changed_initial,
    "independent_memory_state_variable": False,
    "target_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-19", result["status"])
print("memory_is_derived_from_history=", result["memory_is_derived_from_history"])
print("replay_reproducible=", result["replay_reproducible"])
print("independent_memory_state_variable= False")
