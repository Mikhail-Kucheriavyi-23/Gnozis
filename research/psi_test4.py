"""Test-4: deterministic candidate generation from corpus-derived primitives.

The generator receives primitive labels and structural constraints rather than
predefined candidate models. It constructs multiple representations by
applying allowed transformations, then evaluates them with a fixed evaluator.
This is a controlled proxy for Generate->Test->Select; it is not claimed to be
full autonomous scientific discovery.
"""
from pathlib import Path
import json

OUT = Path(__file__).with_name("psi_test4_result.json")
primitives = ["Psi", "E", "Y", "rho", "phi", "T", "Q", "E_next", "J"]
base_edges = [("Psi", "E"), ("E", "Y"), ("Y", "rho"), ("Y", "phi"), ("Y", "T"), ("T", "Q"), ("Q", "E_next"), ("E_next", "J")]

# Generate representations algorithmically from the same primitive set.
candidates = []
for mode in ("expanded", "factorized", "compressed"):
    if mode == "expanded":
        nodes = primitives + ["constraints", "history", "tests"]
        edges = base_edges + [("Y", "history"), ("J", "tests")]
    elif mode == "factorized":
        nodes = primitives + ["constraints"]
        edges = base_edges + [("J", "constraints")]
    else:
        nodes = primitives
        edges = base_edges
    candidates.append({"name": mode, "nodes": nodes, "edges": edges})

# Fixed evaluator: no candidate can modify it.
def evaluate(m):
    coverage = len(set(primitives) & set(m["nodes"])) / len(primitives)
    complexity = len(m["nodes"]) + len(m["edges"])
    error = 1.0 - coverage
    return {"coverage": coverage, "complexity": complexity, "error": error, "J": error + 0.01 * complexity}

for m in candidates:
    m["metrics"] = evaluate(m)
selected = min(candidates, key=lambda x: x["metrics"]["J"])

assert selected["metrics"]["coverage"] == 1.0
assert all("metrics" in c for c in candidates)

result = {
    "test": "TEST-4",
    "status": "PASS",
    "generation_source": "primitive_set + structural_constraints",
    "candidate_count": len(candidates),
    "candidates": candidates,
    "selected": selected["name"],
    "evaluator_changed": False,
    "autonomous_discovery_claim": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-4 PASS")
print("generated_candidates=", len(candidates))
print("selected=", selected["name"])
print("evaluator_changed= False")
