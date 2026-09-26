from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_CORE_TOKENS = (
    "genesis",
    "research-memory",
    "openai",
    "notion",
    "github",
    "connector",
)


def core_python_files():
    core = ROOT / "gnozis_core"
    if not core.exists():
        return []
    return core.rglob("*.py")


def test_core_does_not_import_external_authority_layers():
    violations = []
    for path in core_python_files():
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_CORE_TOKENS:
            if token in text:
                violations.append(f"{path.relative_to(ROOT)} contains forbidden token: {token}")
    assert not violations, "\\n".join(violations)


def test_architecture_contracts_exist():
    required = (
        ROOT / "docs/CORE-CONTRACTS.md",
        ROOT / "docs/CORE-SCHEMAS.md",
        ROOT / "docs/CORE-TRUST-RULES.md",
        ROOT / "docs/DEPENDENCY-POLICY.md",
    )
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    assert not missing, f"Missing architecture contracts: {missing}"
