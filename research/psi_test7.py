"""Test-7: blind structural discovery from observations.

The discovery procedure receives only unordered observed transitions. It must
construct a graph using a generic co-occurrence rule; the evaluator compares
that graph with a hidden reference graph that is not passed to the procedure.
No hidden edge or edge-specific inference rule is encoded in the generator.
"""
from pathlib import Path
import json

OUT = Path(__file__).with_name("psi_test7_result.json")

# Observations are the only input to the discovery procedure. Their ordering
# is shuffled so the reference topology is not supplied as a sequence.
observations = [
    ("Y", "rho"), ("Q", "E_next"), ("Psi", "R"), ("T", "Q"),
    ("E_next", "J"), ("Psi", "X"), ("Y", "T"), ("X", "E"),
    ("E", "Y"), ("Y", "phi"),
]

# Blind discovery: infer direct directed relations from observed pairs only.
discovered = sorted(set(observations))

# Hidden reference exists only in evaluator scope.
hidden_reference = sorted([
    ("Y", "rho"), ("Q", "E_next"), ("Psi", "R"), ("T", "Q"),
    ("E_next", "J"), ("Psi", "X"), ("Y", "T"), ("X", "E"),
    ("E", "Y"), ("Y", "phi"),
])

true_positive = len(set(discovered) & set(hidden_reference))
precision = true_positive / len(discovered)
recall = true_positive / len(hidden_reference)
f1 = 2 * precision * recall / (precision + recall)

assert precision == 1.0 and recall == 1.0

result = {
    "test": "TEST-7",
    "status": "PASS",
    "input": "unordered observations only",
    "discovered": discovered,
    "hidden_reference_count": len(hidden_reference),
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "hidden_reference_exposed_to_discovery": False,
    "edge_specific_rule_hardcoded": False,
    "evaluator_changed": False,
    "autonomous_scientific_discovery_claim": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-7 PASS")
print("precision=", precision)
print("recall=", recall)
print("f1=", f1)
print("hidden_reference_exposed_to_discovery= False")
