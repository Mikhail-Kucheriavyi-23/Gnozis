from core.proof import prove_transition


def invariant(candidate):
    return candidate.get("valid") is True


def test_invariant_valid_unchanged_candidate_is_fixed_point():
    current = {"id": 0, "valid": True}

    proof = prove_transition(current, current, [current], invariant)

    assert proof.invariant is True
    assert proof.viable is True
    assert proof.passed is True
    assert proof.evidence["fixed_point"] is True
    assert proof.evidence["has_distinct_continuation"] is False


def test_changing_valid_candidate_without_continuation_is_not_viable():
    current = {"id": 0, "valid": True}
    candidate = {"id": 1, "valid": True}

    proof = prove_transition(current, candidate, [candidate], invariant)

    assert proof.invariant is True
    assert proof.viable is False
    assert proof.passed is False
    assert proof.evidence["fixed_point"] is False
