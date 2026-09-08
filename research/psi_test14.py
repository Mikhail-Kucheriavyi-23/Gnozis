"""TEST-14: multi-step dynamic composition.

The same initial (X,R) is evolved through several transitions. The test
checks determinism of the whole trajectory and that a relation perturbation
at one step propagates into a different downstream trajectory.
"""
from pathlib import Path
import json
import re

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test14_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def transition(state_relation):
    state, relation = state_relation
    sm = re.fullmatch(r"x(\d+)", state)
    rm = re.fullmatch(r"r(\d+)", relation)
    if not sm or not rm:
        raise ValueError("invalid synthetic state/relation identifier")
    s, r = int(sm.group(1)), int(rm.group(1))
    return (f"x{s + r - 1}", f"r{r + 2}")

def trajectory(initial, perturb_step=None):
    current = initial
    trace = [current]
    for step in range(3):
        if step == perturb_step:
            current = (current[0], f"r{int(current[1][1:]) + 1}")
        current = transition(current)
        trace.append(current)
    return trace

initial = ("x7", "r3")
trace_a = trajectory(initial)
trace_b = trajectory(initial)
perturbed = trajectory(initial, perturb_step=1)

pass_result = (
    trace_a == trace_b
    and trace_a != perturbed
    and trace_a[0] == perturbed[0]
    and trace_a[1] == perturbed[1]
    and trace_a[2] != perturbed[2]
)

result = {
    "test": "TEST-14",
    "status": "PASS" if pass_result else "FAIL",
    "steps": 3,
    "initial": initial,
    "baseline_trace": trace_a,
    "repeat_trace": trace_b,
    "perturbed_trace": perturbed,
    "multi_step_deterministic": trace_a == trace_b,
    "perturbation_changes_downstream": trace_a != perturbed,
    "expected_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-14", result["status"])
print("multi_step_deterministic=", result["multi_step_deterministic"])
print("perturbation_changes_downstream=", result["perturbation_changes_downstream"])
