"""Explicit conflict-resolution candidates and deferred outcomes."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .admission import Admission
from .branch import Branch
from .commit import SemanticCommit, commit
from .merge import Conflict
from .proof import ProofObligation
from .state import Psi


class ResolutionMode(str, Enum):
    COMMIT = "commit"
    DEFER = "defer"


@dataclass(frozen=True)
class ResolutionCandidate:
    conflict: Conflict
    candidate: Psi
    rationale: str
    kernel_version: str = "resolution"

    @property
    def source_branches(self) -> tuple[Branch, Branch]:
        return self.conflict.left, self.conflict.right

    @property
    def source_psis(self) -> tuple[Psi, Psi]:
        return self.conflict.source_psis


@dataclass(frozen=True)
class DeferredConflict:
    """Explicitly retained conflict; no branch is selected or mutated."""

    conflict: Conflict
    reason: str


def resolve(
    conflict: Conflict,
    candidate: Psi,
    rationale: str,
    *,
    kernel_version: str = "resolution",
) -> ResolutionCandidate:
    if not isinstance(conflict, Conflict):
        raise TypeError("resolve requires a Conflict.")
    if not isinstance(candidate, Psi):
        raise TypeError("resolution candidate must be Psi.")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("resolution requires a non-empty rationale.")
    if not kernel_version.strip():
        raise ValueError("kernel_version is required.")
    return ResolutionCandidate(
        conflict=conflict,
        candidate=candidate,
        rationale=rationale,
        kernel_version=kernel_version,
    )


def defer(conflict: Conflict, reason: str) -> DeferredConflict:
    if not isinstance(conflict, Conflict):
        raise TypeError("defer requires a Conflict.")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("deferred conflict requires a non-empty reason.")
    return DeferredConflict(conflict=conflict, reason=reason)


def admit_resolution(resolution: ResolutionCandidate, proof: ProofObligation) -> Admission:
    """Route a resolution proposal through the canonical admission gate."""
    if not isinstance(resolution, ResolutionCandidate):
        raise TypeError("admit_resolution requires ResolutionCandidate.")
    from .admission import admit
    return admit(resolution.candidate, proof)


def commit_resolution(
    previous: Psi,
    resolution: ResolutionCandidate,
    admission: Admission,
) -> SemanticCommit:
    """Create a semantic commit only from an admitted resolution candidate."""
    if not isinstance(resolution, ResolutionCandidate):
        raise TypeError("commit_resolution requires ResolutionCandidate.")
    if admission.candidate != resolution.candidate:
        raise ValueError("Admission candidate does not match resolution candidate.")
    return commit(previous, admission, kernel_version=resolution.kernel_version)
