import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "gnozis_core"

FORBIDDEN_ROOTS = {
    "genesis",
    "research_memory",
    "research-memory",
    "openai",
    "notion",
    "github",
}


def test_core_has_no_forbidden_imports():
    if not CORE.exists():
        return

    violations = []
    for path in CORE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]

            for name in names:
                root = name.split(".")[0].lower().replace("-", "_")
                if root in FORBIDDEN_ROOTS:
                    violations.append(
                        f"{path.relative_to(ROOT)} imports forbidden root: {name}"
                    )

    assert not violations, "\n".join(violations)
