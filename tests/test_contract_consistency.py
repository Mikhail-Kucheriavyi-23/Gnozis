from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TERMS = {
    "docs/CORE-CONTRACTS.md": ("State", "Transition", "Context", "Evidence", "External update", "Authority"),
    "docs/CORE-SCHEMAS.md": ("State:", "Candidate:", "ExecutionInput:", "Evidence:", "Context:", "ExternalUpdate:"),
    "docs/CORE-TRUST-RULES.md": ("trusted state", "Research-Memory", "Genesis", "LLM/AI", "Persistence, retrieval"),
    "docs/DEPENDENCY-POLICY.md": ("Allowed", "Forbidden", "Core -> Genesis", "Core -> Research-Memory"),
    "docs/CONTEXT-CONTINUITY-CONTRACT.md": ("Identity", "Project", "Task", "Knowledge", "Session", "Provenance"),
    "docs/PROVENANCE-CONTRACT.md": ("provenance_id", "source_reference", "content_digest", "schema_version"),
    "docs/EXTERNAL-WRITE-UPDATE-CONTRACT.md": ("update_id", "target_surface", "payload_digest", "authorization_scope", "provenance_id", "rollback_reference"),
}


def test_contract_documents_are_consistent_and_present():
    failures = []
    for relative, terms in REQUIRED_TERMS.items():
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                failures.append(f"{relative}: missing term {term!r}")

    assert not failures, "\n".join(failures)


def test_architecture_index_exists():
    index = ROOT / "docs/ARCHITECTURE-CONTRACT-INDEX.md"
    assert index.exists()
    text = index.read_text(encoding="utf-8")
    assert "Core owns trusted state" in text
