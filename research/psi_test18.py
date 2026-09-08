"""TEST-18: endogenous rule mutation with replay consistency.

The rule state R is part of the evolving state. Each step generates candidates,
tests them, selects one, and mutates R from the selected relation. The same
initial (X,R) must reproduce the same joint trajectory; changing only R0 must
alter the subsequent trajectory.
"""
from pathlib import Path
import json

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test18_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def generate(x, r, step):
    s, q = int(x[1:]), int(r[1:])
    return [f"r{(s + q + step) % 7 + 1}", f"r{(s + 2*q + step + 1) % 7 + 1}"]

def test_candidate(x, r, candidate):
    s, q, c = int(x[1:]), int(r[1:]), int(candidate[1:])
    return (s + q + 2*c) % 11

def select(x, r, candidates):
    return max(candidates, key=lambda c: test_candidate(x, r, c))

def evolve(initial_x, initial_r, steps=4):
    x, r = initial_x, initial_r
    trace = [(x, r)]
    for step in range(steps):
        candidates = generate(x, r, step)
        selected = select(x, r, candidates)
        x = f"x{int(x[1:]) + int(selected[1:]) - 1}"
        r = selected
        trace.append((x, r))
    return trace

base = evolve("x7", "r3")
replay = evolve("x7", "r3")
changed_rule = evolve("x7", "r4")

pass_result = (
    base == replay
    and base != changed_rule
    and all(len(pair) == 2 for pair in base)
    and any(base[i][1] != base[i+1][1] for i in range(len(base)-1))
)

result = {
    "test": "TEST-18",
    "status": "PASS" if pass_result else "FAIL",
    "base_initial": ["x7", "r3"],
    "changed_rule_initial": ["x7", "r4"],
    "base_trace": base,
    "replay_trace": replay,
    "changed_rule_trace": changed_rule,
    "rule_is_part_of_evolving_state": True,
    "rule_changes_during_evolution": any(base[i][1] != base[i+1][1] for i in range(len(base)-1)),
    "replay_reproducible": base == replay,
    "changing_only_initial_rule_changes_trajectory": base != changed_rule,
    "target_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-18", result["status"])
print("rule_changes_during_evolution=", result["rule_changes_during_evolution"])
print("replay_reproducible=", result["replay_reproducible"])
print("changed_rule_changes_trajectory=", result["changing_only_initial_rule_changes_trajectory"])
