from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "gnozis_core"


def test_trusted_core_has_no_product_layers():
    forbidden = {"knowledge", "research", "commercial", "ui", "connectors", "integrations"}
    directories = {p.name.lower() for p in CORE.iterdir() if p.is_dir()}
    assert not directories.intersection(forbidden)


def test_legacy_core_runtime_is_gone():
    legacy = ROOT / "platform" / "core"
    runtime_files = [] if not legacy.exists() else [p for p in legacy.rglob("*.py") if p.name != "__init__.py"]
    assert runtime_files == []


def test_active_core_namespace_exists():
    required = {"__init__.py", "model.py", "transition.py", "verify.py", "commit.py", "digest.py", "persistence.py", "recovery.py", "provenance.py", "audit.py"}
    assert required.issubset({p.name for p in CORE.iterdir()})
