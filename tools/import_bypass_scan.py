"""Import-aware static audit for semantic commit bypass routes."""
from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
FORBIDDEN_MODULES = {"core.commit_contract", "core.history"}
FORBIDDEN_NAMES = {"commit_once", "SemanticCommit"}

def scan() -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for path in CORE.rglob("*.py"):
        if path.name == "canonical_chain.py":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module in FORBIDDEN_MODULES:
                    for alias in node.names:
                        if alias.name in FORBIDDEN_NAMES:
                            findings.append((str(path.relative_to(ROOT)), node.lineno, f"import:{module}.{alias.name}"))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in FORBIDDEN_MODULES:
                        findings.append((str(path.relative_to(ROOT)), node.lineno, f"import:{alias.name}"))
    return findings

if __name__ == "__main__":
    for finding in scan():
        print(f"{finding[0]}:{finding[1]}: {finding[2]}")
