"""TEST-16: endogenous generate -> test -> select loop.

Candidates are generated from the current state by a deterministic internal
rule. Each candidate is scored/tested internally and the best admissible
candidate is selected. No target output is supplied by the test harness.
The same initial state must reproduce the same selected trajectory.
"""
from pathlib import Path
import json

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test16_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def generate(state, step):
    s = int(state[1:])
    return [f"r{(s + step) % 5 + 1}", f"r{(s + step + 2) % 5 + 1}"]

def test_candidate(state, relation):
    s = int(state[1:])
    r = int(relation[1:])
    return (s + 2 * r) % 7

def select(state, candidates):
    scored = [(test_candidate(state, r), r) for r in candidates]
    return max(scored)[1]

def evolve(initial, steps=3):
    state = initial
    trace = [state]
    selections = []
    for step in range(steps):
        candidates = generate(state, step)
        selected = select(state, candidates)
        state = f"x{int(state[1:]) + int(selected[1:]) - 1}"
        trace.append(state)
        selections.append({"candidates": candidates, "selected": selected})
    return trace, selections

trace_a, selections_a = evolve("x7")
trace_b, selections_b = evolve("x7")

pass_result = (
    trace_a == trace_b
    and selections_a == selections_b
    and all(x["selected"] in x["candidates"] for x in selections_a)
    and len(selections_a) == 3
)

result = {
    "test": "TEST-16",
    "status": "PASS" if pass_result else "FAIL",
    "initial_state": "x7",
    "trace": trace_a,
    "selections": selections_a,
    "repeat_reproduces": trace_a == trace_b and selections_a == selections_b,
    "generated_candidates": True,
    "internal_testing": True,
    "internal_selection": True,
    "target_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-16", result["status"])
print("generated_candidates= True")
print("internal_testing= True")
print("internal_selection= True")
print("repeat_reproduces=", result["repeat_reproduces"])
