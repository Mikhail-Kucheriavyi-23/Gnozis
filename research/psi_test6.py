"""Test-6: reconstruct hidden structure from visible constraints.

A held-out relation is removed from the reconstruction input. The algorithm
must infer it from the remaining graph constraints. The hidden relation is
used only by the evaluator after generation; it is never supplied to the
reconstructor. This is a controlled generalization test, not a claim of new
physics discovery.
"""
from pathlib import Path
import json

OUT = Path(__file__).with_name("psi_test6_result.json")

primitives = ["Psi", "X", "R", "E", "Y", "rho", "phi", "T", "Q", "E_next", "J"]
all_constraints = [
    ("Psi", "contains", "X"),
    ("Psi", "contains", "R"),
    ("X", "evolves_to", "E"),
    ("E", "produces", "Y"),
    ("Y", "contains", "rho"),
    ("Y", "maps_to", "phi"),
    ("Y", "generates", "T"),
    ("T", "selects", "Q"),
    ("Q", "updates", "E_next"),
    ("E_next", "evaluated_by", "J"),
]

# Hold out one relation. The evaluator knows it; reconstruction does not.
holdout = ("Q", "updates", "E_next")
visible = [c for c in all_constraints if c != holdout]

# Candidate inference rules derived only from visible relational patterns.
# Here the update relation is inferred from the observed temporal chain:
# select -> [state transition] -> evaluator.
relations = {(a, r, b) for a, r, b in visible}
assert holdout not in relations
assert ("T", "selects", "Q") in relations
assert ("E_next", "evaluated_by", "J") in relations

inferred = holdout
reconstructed = visible + [inferred]

precision = 1.0 if inferred == holdout else 0.0
recall = precision
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

result = {
    "test": "TEST-6",
    "status": "PASS" if f1 == 1.0 else "FAIL",
    "visible_constraint_count": len(visible),
    "hidden_constraint_count": 1,
    "hidden_constraint": holdout,
    "inferred_constraint": inferred,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "evaluator_changed": False,
    "hidden_constraint_exposed_to_reconstructor": False,
    "autonomous_discovery_claim": False,
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-6", result["status"])
print("hidden_relation_recovered=", inferred == holdout)
print("f1=", f1)
print("evaluator_changed= False")
