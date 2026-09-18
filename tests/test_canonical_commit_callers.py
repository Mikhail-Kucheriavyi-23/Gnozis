from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_production_commit_callers_are_known():
    evolution = _read("core/evolution.py")
    resolution = _read("core/resolution.py")
    assert "semantic_commit = commit(" in evolution
    assert "return commit(previous, admission)" in resolution


def test_evolution_returns_only_semantic_commit_result():
    source = _read("core/evolution.py")
    assert "committed = semantic_commit.apply()" in source
    assert "return committed.x, committed.relations" in source


def test_resolution_checks_candidate_identity_before_commit():
    source = _read("core/resolution.py")
    assert "admission.candidate != resolution.candidate" in source
    assert "return commit(previous, admission)" in source


def test_no_direct_semantic_commit_constructor_outside_commit_module():
    core = ROOT / "core"
    offenders = []
    for path in core.glob("*.py"):
        if path.name == "commit.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "SemanticCommit(" in text:
            offenders.append(str(path))
    assert offenders == []
