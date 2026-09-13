"""Research-only persistence experiment.

This test is intentionally kept outside the Core CI test tree. It depends on
research.drosophila_principles, which is an experimental research dependency
and is not part of the canonical Ψ-Core proof surface.
"""

from research.persistence_experiment import LIFState, Synapse


def test_persistence_experiment_import_surface():
    assert LIFState is not None
    assert Synapse is not None
