from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "gnozis_core"


def test_trusted_core_has_no_external_product_layers():
    forbidden = {"knowledge", "research", "commercial", "ui", "connectors", "integrations"}
    paths = {p.name.lower() for p in CORE.iterdir() if p.is_dir()}
    assert not (paths & forbidden)


def test_legacy_core_contains_no_new_runtime_module():
    legacy = ROOT / "platform" / "core"
    if not legacy.exists():
        return
    runtime_files = [p for p in legacy.rglob("*.py") if p.name != "__init__.py"]
    assert runtime_files == [], "legacy Core must remain frozen during migration"
