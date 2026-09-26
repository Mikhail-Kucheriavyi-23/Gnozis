import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "gnozis_core"

FORBIDDEN_CORE_ROOTS = {
    "genesis",
    "research_memory",
    "research",
    "product",
    "commercial",
    "ui",
    "connectors",
    "connector",
}


def module_import_roots(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name.split(".")[0].lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module.split(".")[0].lower()


def test_core_dependency_direction():
    if not CORE.exists():
        return

    violations = []
    for path in CORE.rglob("*.py"):
        for root in module_import_roots(path):
            if root in FORBIDDEN_CORE_ROOTS:
                violations.append(f"{path.relative_to(ROOT)} -> {root}")

    assert not violations, "\n".join(violations)
