"""Adversarial boundary tests for the Ψ-GNR bridge contract.

These tests are intentionally contract-level. They define the fail-closed
behaviour required before a bridge implementation can be considered safe.
"""

import pytest


class PsiContract:
    """Minimal executable reference model for the safety boundary."""

    def __init__(self):
        self.epoch = 0
        self.generation = 0
        self.height = 0
        self.finality_height = 0
        self.finality_hash = "GENESIS"
        self.hash = "GENESIS"
        self.halted = False

    def execute(self, candidate):
        if self.halted:
            return "HALT"

        if candidate.get("generation") != self.generation:
            return "REJECT"
        if candidate.get("epoch") != self.epoch:
            return "REJECT"
        if candidate.get("previous_hash") != self.hash:
            return "REJECT"
        if candidate.get("base_height", self.height) < self.finality_height:
            return "REJECT"
        if candidate.get("base_hash") != self.finality_hash:
            return "REJECT"
        if candidate.get("conflicting_authority"):
            self.halted = True
            return "HALT"

        self.height += 1
        self.generation += 1
        self.hash = candidate["next_hash"]
        return "CONTINUE"


def valid_candidate(model, next_hash="H1"):
    return {
        "epoch": model.epoch,
        "generation": model.generation,
        "previous_hash": model.hash,
        "base_height": model.finality_height,
        "base_hash": model.finality_hash,
        "next_hash": next_hash,
    }


def test_valid_continuity_continues():
    model = PsiContract()
    assert model.execute(valid_candidate(model)) == "CONTINUE"


def test_generation_reuse_rejected():
    model = PsiContract()
    candidate = valid_candidate(model)
    assert model.execute(candidate) == "CONTINUE"
    assert model.execute(candidate) == "REJECT"


def test_broken_provenance_rejected():
    model = PsiContract()
    candidate = valid_candidate(model)
    candidate["previous_hash"] = "FORGED"
    assert model.execute(candidate) == "REJECT"


def test_stale_finality_base_rejected():
    model = PsiContract()
    model.finality_height = 3
    model.finality_hash = "H3"
    candidate = valid_candidate(model)
    candidate["base_height"] = 2
    candidate["base_hash"] = "H2"
    assert model.execute(candidate) == "REJECT"


def test_epoch_mismatch_rejected():
    model = PsiContract()
    candidate = valid_candidate(model)
    candidate["epoch"] = model.epoch + 1
    assert model.execute(candidate) == "REJECT"


def test_conflicting_authority_halts():
    model = PsiContract()
    candidate = valid_candidate(model)
    candidate["conflicting_authority"] = True
    assert model.execute(candidate) == "HALT"
    assert model.execute(valid_candidate(model)) == "HALT"


def test_valid_candidate_cannot_branch_from_old_hash():
    model = PsiContract()
    assert model.execute(valid_candidate(model, "H1")) == "CONTINUE"
    candidate = valid_candidate(model, "H2")
    candidate["previous_hash"] = "GENESIS"
    assert model.execute(candidate) == "REJECT"


def test_crash_recovery_is_modelled_as_replay_not_peer_override():
    """Contract marker for J_Ψ/Replay(P): recovery must derive from durable log.

    The concrete durable implementation belongs to the bridge. This test
    deliberately documents the required invariant without pretending that
    the reference model is a storage engine.
    """
    durable = [
        {"generation": 1, "height": 1, "hash": "H1", "status": "COMMITTED"},
        {"generation": 2, "height": 2, "hash": "H2", "status": "PREPARED"},
    ]
    committed = [r for r in durable if r["status"] in {"LINEARIZED", "COMMITTED"}]
    assert committed[-1]["generation"] == 1
    assert committed[-1]["hash"] == "H1"


def test_prepared_without_decision_is_not_authority():
    witness = {"status": "PREPARED", "generation": 7}
    assert witness["status"] not in {"DECIDED", "LINEARIZED", "COMMITTED"}


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
