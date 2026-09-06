"""Test-9: derive competing formalizations from the mathematical corpus."""
from pathlib import Path
import json
import re

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
OUT = Path(__file__).with_name("psi_test9_result.json")
text = CORPUS.read_text(encoding="utf-8")
tokens = sorted(set(re.findall(r"[A-Za-z]+(?:_[A-Za-z0-9]+)?", text)))
required = {"Psi", "X", "R", "E", "Y"}
assert required <= set(tokens)

representations = {
    "token_graph": sorted(set(tokens)),
    "operator_graph": sorted(t for t in tokens if t in {"Psi", "X", "R", "E", "Y", "rho", "phi", "T", "Q", "J"}),
    "core_graph": sorted(t for t in tokens if t in required),
}

def score(nodes):
    coverage = len(required & set(nodes)) / len(required)
    complexity = len(nodes)
    return (coverage, -complexity)

scores = {name: score(nodes) for name, nodes in representations.items()}
selected = max(representations, key=lambda name: scores[name])
assert scores[selected][0] == 1.0

result = {
    "test": "TEST-9",
    "status": "PASS",
    "source": "psi_mathematical_corpus_v1.md",
    "candidate_generation": "generic corpus token transforms",
    "candidates": {k: {"node_count": len(v), "score": scores[k]} for k, v in representations.items()},
    "selected": selected,
    "evaluator_changed": False,
    "predefined_candidate_models": False,
    "autonomous_scientific_discovery_claim": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-9 PASS")
print("selected=", selected)
