from pathlib import Path


def test_ci_runs_repository_tests_and_fails_on_pytest_failure():
    workflow = Path(".github/workflows/test.yml").read_text()
    assert "python -m pytest -q tests --ignore=tests/research" in workflow
    assert "PIPESTATUS[0]" in workflow
