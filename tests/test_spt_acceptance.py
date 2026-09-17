from research.spt_acceptance import evaluate_spt


def test_spt_requires_matched_budget_and_beats_random_control():
    result = evaluate_spt(
        [0.2, 0.3],
        [0.2, 0.35],
        [0.2, 0.5],
        random_budget=4,
        initial_budget=4,
    )
    assert result.matched_budget
    assert result.plastic_over_random == 0.15
    assert result.accepted


def test_spt_rejects_unmatched_random_control():
    result = evaluate_spt(
        [0.2],
        [0.2],
        [0.9],
        random_budget=5,
        initial_budget=4,
    )
    assert not result.matched_budget
    assert not result.accepted


def test_spt_does_not_accept_plasticity_below_random_control():
    result = evaluate_spt(
        [0.2],
        [0.8],
        [0.7],
        random_budget=4,
        initial_budget=4,
    )
    assert result.matched_budget
    assert not result.accepted
