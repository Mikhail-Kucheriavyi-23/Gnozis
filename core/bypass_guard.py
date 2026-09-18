"""Static audit contract for the canonical transition boundary."""
from __future__ import annotations

CANONICAL_ENTRYPOINT = "core.canonical_chain.admit_transition"
FORBIDDEN_DIRECT_COMMIT = (
    "AppendOnlyHistory.append",
    "SemanticCommit",
    "commit_once",
)

def canonical_entrypoint() -> str:
    return CANONICAL_ENTRYPOINT

def forbidden_direct_commit_symbols() -> tuple[str, ...]:
    return FORBIDDEN_DIRECT_COMMIT
