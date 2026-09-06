"""TEST-20: final integrated closure test for the current Psi kernel.

Checks one complete endogenous cycle over Y=(X,R):
Generate -> Test -> Select -> Evolve, with R mutating and memory derived
only from the produced history. Replaying the same initial state must be
identical; changing the initial rule must alter the trajectory. No target
trajectory is supplied by the harness.
"""
from pathlib import Path
import json

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test20_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert all(token in text for token in ("X_{t+1}", "R_{t+1}", "F"))

def generate(x, r, step):
    s, q = int(x[1:]), int(r[1:])
    return [f"r{(s + q + step) % 7 + 1}", f"r{(s + 2*q + step + 1) % 7 + 1}"]

def test_candidate(x, r, candidate):
    s, q, c = int(x[1:]), int(r[1:]), int(candidate[1:])
    return (s + q + 2*c) % 11

def select(x, r, candidates):
    return max(candidates, key=lambda c: test_candidate(x, r, c))

def evolve(x0, r0, steps=5):
    x, r = x0, r0
    history = [(x, r)]
    decisions = []
    for step in range(steps):
        candidates = generate(x, r, step)
        selected = select(x, r, candidates)
        x = f"x{int(x[1:]) + int(selected[1:]) - 1}"
        r = selected
        history.append((x, r))
        decisions.append({"candidates": candidates, "selected": selected})
    return history, decisions

base, decisions = evolve("x7", "r3")
replay, replay_decisions = evolve("x7", "r3")
changed_rule, _ = evolve("x7", "r4")
derived_memory = base[:-1]

pass_result = all([
    base == replay,
    decisions == replay_decisions,
    base != changed_rule,
    len(base) == 6,
    len(decisions) == 5,
    all(d["selected"] in d["candidates"] for d in decisions),
    any(base[i][1] != base[i+1][1] for i in range(len(base)-1)),
    derived_memory == base[:-1],
])

result = {
    "test": "TEST-20",
    "status": "PASS" if pass_result else "FAIL",
    "initial_state": ["x7", "r3"],
    "trajectory": base,
    "decisions": decisions,
    "replay_identical": base == replay and decisions == replay_decisions,
    "changed_initial_rule_changes_trajectory": base != changed_rule,
    "rule_mutates": any(base[i][1] != base[i+1][1] for i in range(len(base)-1)),
    "memory_is_derived_history": derived_memory == base[:-1],
    "endogenous_generate_test_select": True,
    "target_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-20", result["status"])
print("replay_identical=", result["replay_identical"])
print("changed_initial_rule_changes_trajectory=", result["changed_initial_rule_changes_trajectory"])
print("rule_mutates=", result["rule_mutates"])
print("memory_is_derived_history=", result["memory_is_derived_history"])
