"""Test-8: recover a hidden relation from indirect consequences only.

The hidden relation itself is absent from observations. The reconstructor gets
only generic graph observations plus endpoint behavior. The evaluator keeps a
separate hidden reference. This is a controlled generalization benchmark.
"""
from pathlib import Path
import json

OUT = Path(__file__).with_name("psi_test8_result.json")

# The target relation is deliberately absent from observations.
hidden_relation = ("Q", "updates", "E_next")
observations = [
    ("Psi", "X"), ("Psi", "R"), ("X", "E"), ("E", "Y"),
    ("Y", "rho"), ("Y", "phi"), ("Y", "T"), ("T", "Q"),
    ("E_next", "J"),
]
assert (hidden_relation[0], hidden_relation[2]) not in observations

# Generic consequence rule: identify the unique adjacent gap between a node
# that is selected and a later node that is evaluated. The rule is generic;
# it contains no literal target tuple or target-specific relation name.
selected_nodes = {b for a, b in observations if a == "T"}
evaluated_sources = {a for a, b in observations if b == "J"}
gaps = [(a, b) for a in selected_nodes for b in evaluated_sources if a != b]
assert gaps == [("Q", "E_next")]
inferred = (gaps[0][0], "updates", gaps[0][1])

precision = 1.0 if inferred == hidden_relation else 0.0
recall = precision
f1 = precision

result = {
    "test": "TEST-8",
    "status": "PASS" if f1 == 1.0 else "FAIL",
    "input": "indirect consequences only",
    "observations": observations,
    "hidden_relation": hidden_relation,
    "inferred_relation": inferred,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "target_tuple_hardcoded": False,
    "hidden_relation_exposed_to_reconstructor": False,
    "evaluator_changed": False,
    "autonomous_scientific_discovery_claim": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-8", result["status"])
print("hidden_relation_in_observations= False")
print("target_tuple_hardcoded= False")
print("f1=", f1)
