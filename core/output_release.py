"""Final gate before an output may cross a destination boundary."""
from __future__ import annotations

from dataclasses import dataclass

from .destination_authorization import DestinationAuthorization
from .value_pipeline import OutputProposal, OutputStatus


@dataclass(frozen=True)
class ReleasedOutput:
    proposal: OutputProposal
    release_id: str


class OutputReleaseGate:
    def __init__(self, authorization: DestinationAuthorization) -> None:
        self.authorization = authorization

    def release(self, proposal: OutputProposal, *, release_id: str) -> ReleasedOutput:
        if proposal.status is not OutputStatus.PROPOSED:
            raise PermissionError("only proposed outputs can be released")
        if not release_id.strip():
            raise ValueError("release_id is required")
        self.authorization.require_allowed(proposal)
        return ReleasedOutput(proposal=proposal, release_id=release_id)
