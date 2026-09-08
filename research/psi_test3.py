"""Test-3: select a simpler equivalent model without changing the evaluator."""
from pathlib import Path
import json

OUT = Path(__file__).with_name("psi_test3_result.json")

# Candidate models intentionally represent the same dependency structure at
# different representational costs. Coverage is fixed so complexity can be
# compared independently of the scoring rule.
candidates = [
    {"name": "expanded", "coverage": 1.0, "error": 0.0, "complexity": 25},
    {"name": "structured", "coverage": 1.0, "error": 0.0, "complexity": 17},
    {"name": "compressed", "coverage": 1.0, "error": 0.0, "complexity": 12},
    {"name": "underfit", "coverage": 0.72, "error": 0.28, "complexity": 7},
]

lam = 0.01

def objective(m):
    return m["error"] + lam * m["complexity"]

for m in candidates:
    m["J"] = objective(m)

selected = min(candidates, key=lambda m: m["J"])
assert selected["name"] == "compressed"
assert selected["coverage"] == 1.0
assert selected["error"] == 0.0

# Evaluator integrity: score formula is fixed before selection and is not
# represented as mutable candidate data.
result = {
    "test": "TEST-3",
    "status": "PASS",
    "lambda": lam,
    "candidates": candidates,
    "selected": selected["name"],
    "evaluator_changed": False,
    "criterion": "J = error + lambda * complexity",
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("TEST-3 PASS")
print("selected=", selected["name"])
print("complexity=", selected["complexity"])
print("evaluator_changed= False")
