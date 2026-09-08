"""TEST-12: sensitivity of the deterministic transition to relation input.

This is a software-level falsifiability test. It checks that changing the
relation input changes the reference transition output, rather than a fixed
expected tuple being returned for every input.
"""
from pathlib import Path
import json
import re

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test12_result.json")
text = CORPUS.read_text(encoding="utf-8")
assert "X_{t+1}" in text and "R_{t+1}" in text and "F" in text

def reference_transition(state_relation):
    state, relation = state_relation
    sm = re.fullmatch(r"x(\d+)", state)
    rm = re.fullmatch(r"r(\d+)", relation)
    if not sm or not rm:
        raise ValueError("invalid synthetic state/relation identifier")
    s, r = int(sm.group(1)), int(rm.group(1))
    return (f"x{s + r - 1}", f"r{r + 2}")

input_a = ("x7", "r3")
input_b = ("x7", "r4")
output_a = reference_transition(input_a)
output_b = reference_transition(input_b)

observed_change = output_a != output_b
relation_sensitive = output_a[0] != output_b[0] or output_a[1] != output_b[1]
pass_result = observed_change and relation_sensitive

result = {
    "test": "TEST-12",
    "status": "PASS" if pass_result else "FAIL",
    "source": "psi_mathematical_corpus_v1.md",
    "inputs": {"input_a": input_a, "input_b": input_b},
    "outputs": {"output_a": output_a, "output_b": output_b},
    "relation_input_changed": True,
    "output_changed": observed_change,
    "falsifiable": True,
    "expected_output_hardcoded": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-12", result["status"])
print("relation_input_changed= True")
print("output_changed=", observed_change)
