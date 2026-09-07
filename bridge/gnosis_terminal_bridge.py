"""Fail-closed terminal bridge for the Ψ-GNR architectural contract.

This module deliberately validates structural evidence only. Cryptographic quorum
verification is injected as a callable; the bridge never treats an opaque proof
string as cryptographically valid by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


ProofVerifier = Callable[[str], bool]


@dataclass(frozen=True)
class CanonicalPointer:
    epoch: int
    generation: int
    height: int
    state_hash: str
    finality_height: int
    finality_hash: str


@dataclass(frozen=True)
class BridgeResult:
    execution_status: str
    reason_code: str
    canonical_pointer: CanonicalPointer


class BridgeHalt(RuntimeError):
    """Raised when conflicting authority evidence is detected."""


class GnosisTerminalBridge:
    """Structural Ψ bridge with explicit fail-closed semantics."""

    def __init__(self, canonical: CanonicalPointer, *, verify_proof: ProofVerifier):
        self.canonical = canonical
        self.verify_proof = verify_proof
        self.recovering = False

    def execute(self, command: str, request: Mapping[str, Any]) -> BridgeResult:
        if self.recovering:
            return self._result("REPLAY", "RECOVERY_IN_PROGRESS")

        if command == "status":
            return self._result("CONTINUE", "STATUS")
        if command not in {"inject", "step", "evolution"}:
            return self._result("REJECT", "UNKNOWN_COMMAND")

        if not self._valid_nonnegative_ids(request):
            return self._result("REJECT", "INVALID_IDENTIFIER")

        if not self._generation_matches(request):
            return self._result("REJECT", "GENERATION_FENCE_MISMATCH")

        if not self._epoch_matches(request):
            return self._result("REJECT", "EPOCH_MISMATCH")

        provenance = request.get("provenance")
        if not isinstance(provenance, Mapping):
            return self._result("REJECT", "MISSING_PROVENANCE")
        if provenance.get("h_prev") != self.canonical.state_hash:
            return self._result("REJECT", "PROVENANCE_DISCONTINUITY")
        h_next = provenance.get("h_next")
        if not isinstance(h_next, str) or not h_next:
            return self._result("REJECT", "INVALID_NEXT_HASH")

        authorization = request.get("authorization")
        if not isinstance(authorization, Mapping):
            return self._result("REJECT", "MISSING_AUTHORIZATION")

        gamma = authorization.get("gamma_signature")
        omega = authorization.get("omega_order")
        if not isinstance(gamma, str) or not self.verify_proof(gamma):
            return self._result("REJECT", "INVALID_GAMMA")
        if not isinstance(omega, str) or not self.verify_proof(omega):
            return self._result("REJECT", "INVALID_OMEGA")

        target_height = int(request["height"])
        if target_height != self.canonical.height + 1:
            return self._result("REJECT", "HEIGHT_NOT_CONTIGUOUS")

        finality = authorization.get("gamma_finality")
        target_finality_height = self.canonical.finality_height
        target_finality_hash = self.canonical.finality_hash
        if finality is not None:
            if not isinstance(finality, str) or not self.verify_proof(finality):
                return self._result("REJECT", "INVALID_FINALITY_PROOF")
            target_finality_height = max(target_finality_height, target_height)
            if target_finality_height == target_height:
                target_finality_hash = h_next

        if target_finality_height > target_height:
            return self._result("REJECT", "FINALITY_AHEAD_OF_STATE")

        candidate = CanonicalPointer(
            epoch=int(request["epoch"]),
            generation=int(request["generation"]),
            height=target_height,
            state_hash=h_next,
            finality_height=target_finality_height,
            finality_hash=target_finality_hash,
        )

        if candidate.generation != self.canonical.generation + 1:
            return self._result("REJECT", "GENERATION_NOT_CONTIGUOUS")
        if candidate.finality_height < self.canonical.finality_height:
            return self._result("REJECT", "FINALITY_ROLLBACK")
        if (
            candidate.finality_height == self.canonical.finality_height
            and candidate.finality_hash != self.canonical.finality_hash
        ):
            raise BridgeHalt("CONFLICTING_FINALITY_AT_SAME_HEIGHT")

        self.canonical = candidate
        return self._result("CONTINUE", "CANONICAL_ADVANCED")

    def recover(self, witnesses: list[Mapping[str, Any]]) -> BridgeResult:
        self.recovering = True
        try:
            candidates: dict[int, Mapping[str, Any]] = {}
            for witness in witnesses:
                status = witness.get("status")
                if status == "PREPARED":
                    continue
                if status not in {"DECIDED", "LINEARIZED", "COMMITTED"}:
                    return self._result("HALT", "INVALID_WITNESS_STATUS")
                g_old = witness.get("g_old")
                if not isinstance(g_old, int):
                    return self._result("HALT", "INVALID_WITNESS_GENERATION")
                previous = candidates.get(g_old)
                if previous is not None and previous.get("token") != witness.get("token"):
                    return self._result("HALT", "CONFLICTING_WITNESS")
                candidates[g_old] = witness

            for g_old in sorted(candidates):
                witness = candidates[g_old]
                new_state = witness.get("pi_new")
                if not isinstance(new_state, Mapping):
                    return self._result("HALT", "MISSING_NEW_STATE")
                if new_state.get("generation") != g_old + 1:
                    return self._result("HALT", "WITNESS_GENERATION_GAP")
                if int(new_state.get("finality_height", -1)) < self.canonical.finality_height:
                    return self._result("HALT", "RECOVERY_FINALITY_ROLLBACK")
                self.canonical = CanonicalPointer(
                    epoch=int(new_state["epoch"]),
                    generation=int(new_state["generation"]),
                    height=int(new_state["height"]),
                    state_hash=str(new_state["state_hash"]),
                    finality_height=int(new_state["finality_height"]),
                    finality_hash=str(new_state["finality_hash"]),
                )

            return self._result("REPLAY", "RECOVERY_REPLAYED")
        finally:
            self.recovering = False

    def _generation_matches(self, request: Mapping[str, Any]) -> bool:
        return request.get("generation") == self.canonical.generation + 1

    def _epoch_matches(self, request: Mapping[str, Any]) -> bool:
        return request.get("epoch") == self.canonical.epoch

    @staticmethod
    def _valid_nonnegative_ids(request: Mapping[str, Any]) -> bool:
        return all(
            isinstance(request.get(key), int) and request[key] >= 0
            for key in ("epoch", "generation", "height")
        )

    def _result(self, status: str, reason: str) -> BridgeResult:
        return BridgeResult(status, reason, self.canonical)
