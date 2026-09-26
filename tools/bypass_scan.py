"""Static scan for direct semantic-commit bypasses.

This is an audit tool: it reports candidate call sites outside the
canonical admission module. It does not claim a complete call-graph proof.
"""
from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
CANONICAL = "canonical_chain.py"
ALLOWED_COMMIT_MODULES = {"canonical_chain.py", "commit.py", "commit_contract.py"}
FORBIDDEN = {"commit_once", "append", "SemanticCommit"}

def scan() -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for path in CORE.rglob("*.py"):
        if path.name in ALLOWED_COMMIT_MODULES or path.name == "__init__.py":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else (
                    node.func.attr if isinstance(node.func, ast.Attribute) else ""
                )
                if name in FORBIDDEN:
                    findings.append((str(path.relative_to(ROOT)), node.lineno, name))
    return findings

if __name__ == "__main__":
    for finding in scan():
        print(f"{finding[0]}:{finding[1]}: {finding[2]}")
