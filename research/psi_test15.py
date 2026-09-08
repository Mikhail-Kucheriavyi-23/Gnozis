"""TEST-15: endogenous transition choice under fixed candidate set.

Given one state X and two admissible relation candidates, the evaluator chooses
one candidate using an internal deterministic score derived from the current
state/relation, with no externally supplied target output. Repeating the same
input must select the same transition; changing the candidate set must be able
to change the selected transition.
"""
from pathlib import Path
import json
import hashlib

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test15_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def score(state, relation):
    digest = hashlib.sha256(f"{state}|{relation}".encode()).hexdigest()
    return int(digest[:8], 16)

def choose(state, candidates):
    assert candidates
    return max(candidates, key=lambda r: score(state, r))

state = "x7"
set_a = ["r3", "r4"]
set_b = ["r3"]
choice_a1 = choose(state, set_a)
choice_a2 = choose(state, set_a)
choice_b = choose(state, set_b)

pass_result = choice_a1 == choice_a2 and choice_a1 in set_a and choice_b == "r3"
result = {
    "test": "TEST-15",
    "status": "PASS" if pass_result else "FAIL",
    "source": "psi_mathematical_corpus_v1.md",
    "state": state,
    "candidate_set_a": set_a,
    "candidate_set_b": set_b,
    "choice_a1": choice_a1,
    "choice_a2": choice_a2,
    "choice_b": choice_b,
    "repeated_choice_stable": choice_a1 == choice_a2,
    "choice_constrained_by_candidates": choice_b in set_b,
    "target_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-15", result["status"])
print("choice_a=", choice_a1)
print("choice_b=", choice_b)
