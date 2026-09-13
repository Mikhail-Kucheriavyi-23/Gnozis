import pytest

from core.proof import prove_transition


def invariant(candidate):
    return candidate.get("valid") is True


def test_valid_candidate_with_valid_continuation_passes():
    current = {"id": 0, "valid": True}
    candidate = {"id": 1, "valid": True}
    continuation = {"id": 2, "valid": True}

    proof = prove_transition(current, candidate, [candidate, continuation], invariant)

    assert proof.invariant is True
    assert proof.viable is True
    assert proof.passed is True
    assert proof.evidence["depth"] == 1


def test_invalid_candidate_fails():
    current = {"id": 0, "valid": True}
    candidate = {"id": 1, "valid": False}
    continuation = {"id": 2, "valid": True}

    proof = prove_transition(current, candidate, [candidate, continuation], invariant)

    assert proof.invariant is False
    assert proof.viable is False
    assert proof.passed is False


def test_dead_end_candidate_fails_viability():
    current = {"id": 0, "valid": True}
    candidate = {"id": 1, "valid": True}

    proof = prove_transition(current, candidate, [candidate], invariant)

    assert proof.invariant is True
    assert proof.viable is False
    assert proof.passed is False


def test_truthy_non_bool_invariant_result_is_rejected():
    def bad_invariant(_candidate):
        return 1

    with pytest.raises(TypeError, match="Invariant.*bool"):
        prove_transition({}, {}, [{"id": 1}], bad_invariant)


def test_proof_does_not_generate_or_select():
    current = {"id": 0, "valid": True}
    candidate = {"id": 1, "valid": True}
    continuation = {"id": 2, "valid": True}

    proof = prove_transition(current, candidate, [candidate, continuation], invariant)

    assert proof.evidence["candidate_count"] == 2
    assert proof.evidence["has_distinct_continuation"] is True
