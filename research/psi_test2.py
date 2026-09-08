"""Test-2: construct a compact model from the Ψ corpus.

This is a deterministic model-selection experiment, not an AI-discovery claim.
It compares a minimal structured representation against the raw corpus and
records coverage, complexity and unresolved obligations.
"""
from pathlib import Path
import re
import json

ROOT = Path(__file__).parent
CORPUS = ROOT / "psi_mathematical_corpus_v1.md"
OUT = ROOT / "psi_test2_result.json"
text = CORPUS.read_text(encoding="utf-8")

concepts = {
    "substrate": r"\\Psi=\(X,R\)",
    "locality": r"\\mathcal N\(x\)",
    "evolution": r"E\(x\)",
    "memory": r"Y=\(X,\\rho\)",
    "history": r"\\rho_t=",
    "model": r"\\varphi:Y\\rightarrow Z",
    "trajectories": r"\\mathcal T\(Y\)",
    "selection": r"\\tau\^\*=",
    "meta_evolution": r"E_{n\+1}=",
    "general_objective": r"J\(M\)=",
    "quantum_branch": r"Hilbert structure",
    "bell_branch": r"\\|S\\|\\le2",
    "time_branch": r"\\Omega_{n\+1}=",
}
covered = [k for k, p in concepts.items() if re.search(p, text)]
unresolved = [
    "Psi_to_Hilbert",
    "positivity_to_Born_without_extra_assumptions",
    "physical_interpretation_of_operational_time",
]

# Compact model: one node per primitive, one edge per explicit dependency.
nodes = ["Psi", "E", "Y", "rho", "phi", "T", "Q", "E_next", "J"]
edges = [
    ("Psi", "E"), ("E", "Y"), ("Y", "rho"), ("Y", "phi"),
    ("Y", "T"), ("T", "Q"), ("Q", "E_next"), ("E_next", "J"),
]
complexity = len(nodes) + len(edges)
coverage = len(covered) / len(concepts)

result = {
    "test": "TEST-2",
    "status": "PASS" if coverage == 1.0 else "FAIL",
    "coverage": coverage,
    "covered_concepts": covered,
    "unresolved_obligations": unresolved,
    "model": {"nodes": nodes, "edges": edges},
    "complexity": complexity,
    "complexity_metric": "nodes + edges",
    "self_optimization_claim": False,
}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("TEST-2", result["status"])
print("coverage=", coverage)
print("complexity=", complexity)
print("unresolved=", len(unresolved))
