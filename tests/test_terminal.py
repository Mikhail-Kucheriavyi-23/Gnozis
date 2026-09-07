from terminal import GnosisTerminal


def test_status_reports_initial_runtime_state():
    terminal = GnosisTerminal()
    status = terminal.status()

    assert status["status"] == "ready"
    assert status["evolution_steps"] == 0
    assert status["received_messages"] == 0
    assert status["state"] == {}


def test_inject_and_evolution_are_observable():
    terminal = GnosisTerminal()

    result = terminal.dispatch({"action": "inject", "data": {"message": "hello"}})
    assert result["status"] == "accepted"
    assert result["state"]["last_input"] == {"message": "hello"}

    step = terminal.dispatch({"action": "step"})
    assert step["status"] == "stepped"
    assert step["evolution_steps"] == 1

    evolution = terminal.dispatch({"action": "evolution"})
    assert evolution["received_messages"] == 1
    assert evolution["evolution_steps"] == 1
    assert evolution["history_length"] == 2


def test_unknown_action_returns_error_over_stdin_transport():
    terminal = GnosisTerminal()

    try:
        terminal.dispatch({"action": "unknown"})
    except ValueError as exc:
        assert "unknown action" in str(exc)
    else:
        raise AssertionError("unknown action must raise ValueError")
