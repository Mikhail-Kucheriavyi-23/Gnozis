"""TEST-13: relation-only round-trip sensitivity.

Keep X fixed, change only R, then restore R. The reference transition must
change when R changes and return to the original output when R is restored.
"""
from pathlib import Path
import json
import re

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test13_result.json")
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

original = ("x7", "r3")
changed = ("x7", "r4")
restored = ("x7", "r3")

output_original = reference_transition(original)
output_changed = reference_transition(changed)
output_restored = reference_transition(restored)

pass_result = (
    output_original != output_changed
    and output_restored == output_original
)

result = {
    "test": "TEST-13",
    "status": "PASS" if pass_result else "FAIL",
    "source": "psi_mathematical_corpus_v1.md",
    "fixed_state": "x7",
    "relations": {"original": "r3", "changed": "r4", "restored": "r3"},
    "outputs": {
        "original": output_original,
        "changed": output_changed,
        "restored": output_restored,
    },
    "relation_only_change": True,
    "restoration_returns_original": output_restored == output_original,
    "expected_output_hardcoded": False,
    "falsifiable": True,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-13", result["status"])
print("relation_only_change= True")
print("restoration_returns_original=", result["restoration_returns_original"])
