from core.proof import prove_fundamental_transition


def test_fundamental_proof_does_not_require_candidate_pool():
    current = object()
    candidate = object()

    proof = prove_fundamental_transition(current, candidate, lambda value: True)

    assert proof.passed is True
    assert proof.invariant is True
    assert proof.viable is False
    assert proof.evidence["regime"] == "fundamental"
    assert proof.evidence["viability"] == "not_applicable"


def test_fundamental_fixed_point_is_valid_when_invariant_holds():
    state = object()

    proof = prove_fundamental_transition(state, state, lambda value: True)

    assert proof.passed is True
    assert proof.evidence["fixed_point"] is True


def test_fundamental_proof_fails_when_invariant_fails():
    current = object()
    candidate = object()

    proof = prove_fundamental_transition(current, candidate, lambda value: False)

    assert proof.passed is False
    assert proof.invariant is False
    assert proof.viable is False


def test_fundamental_invariant_must_return_exact_bool():
    current = object()
    candidate = object()

    try:
        prove_fundamental_transition(current, candidate, lambda value: 1)
    except TypeError as exc:
        assert "Invariant must return bool exactly" in str(exc)
    else:
        raise AssertionError("non-bool invariant result must fail closed")
