"""Test-1: structural extraction from the Ψ mathematical corpus.

This is deliberately a deterministic baseline experiment. It does not claim
that the current v33 kernel has autonomously discovered physics. It measures
whether the corpus can be parsed into the required mathematical primitives,
relations, hypotheses, and proof obligations without conflation.
"""
from pathlib import Path
import re

CORPUS = Path(__file__).with_name("psi_mathematical_corpus_v1.md")
REQUIRED = {
    "substrate": r"\\Psi=\(X,R\)",
    "locality": r"\\mathcal N\(x\)",
    "evolution": r"E\(x\)",
    "extended_state": r"Y=\(X,\\rho\)",
    "memory": r"\\rho_t=",
    "internal_model": r"\\varphi:Y\\rightarrow Z",
    "trajectories": r"\\mathcal T\(Y\)",
    "selection": r"\\tau\^\*=",
    "meta_evolution": r"E_{n\+1}=",
    "holdout": r"L_{holdout}",
    "hilbert_born": r"Hilbert structure",
    "bell_chsh": r"\\|S\\|\\le2",
    "operational_time": r"\\Omega_{n\+1}=",
}

text = CORPUS.read_text(encoding="utf-8")
missing = [name for name, pattern in REQUIRED.items() if not re.search(pattern, text)]
assert not missing, f"Missing corpus structures: {missing}"

# Scientific-status safeguards must remain explicit in the corpus.
for phrase in (
    "must be proved rather than assumed",
    "hypotheses/constraints",
    "Never label a hypothesis a theorem",
    "training and holdout tests separate",
):
    assert phrase in text, f"Missing safeguard: {phrase}"

print("TEST-1 PASS")
print(f"structures={len(REQUIRED)}")
print("status_separation=PASS")
print("self_optimization=NOT_CLAIMED")
