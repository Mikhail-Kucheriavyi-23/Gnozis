"""Fail-closed terminal bridge for the Ψ-GNR architectural contract.

The bridge validates structural evidence only. Cryptographic verification is
injected as a callable; opaque proof strings are never treated as self-proving.
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

        target_height = request["height"]
        if target_height != self.canonical.height + 1:
            return self._result("REJECT", "HEIGHT_NOT_CONTIGUOUS")

        target_finality_height = self.canonical.finality_height
        target_finality_hash = self.canonical.finality_hash
        finality = authorization.get("gamma_finality")
        if finality is not None:
            if not isinstance(finality, str) or not self.verify_proof(finality):
                return self._result("REJECT", "INVALID_FINALITY_PROOF")
            finality_height = request.get("finality_height")
            finality_hash = request.get("finality_hash")
            if not isinstance(finality_height, int) or finality_height < 0:
                return self._result("REJECT", "MISSING_FINALITY_HEIGHT")
            if not isinstance(finality_hash, str) or not finality_hash:
                return self._result("REJECT", "MISSING_FINALITY_HASH")
            if finality_height < self.canonical.finality_height:
                return self._result("REJECT", "FINALITY_ROLLBACK")
            if finality_height > target_height:
                return self._result("REJECT", "FINALITY_AHEAD_OF_STATE")
            if finality_height == self.canonical.finality_height:
                if finality_hash != self.canonical.finality_hash:
                    raise BridgeHalt("CONFLICTING_FINALITY_AT_SAME_HEIGHT")
            else:
                target_finality_height = finality_height
                target_finality_hash = finality_hash

        candidate = CanonicalPointer(
            epoch=request["epoch"],
            generation=request["generation"],
            height=target_height,
            state_hash=h_next,
            finality_height=target_finality_height,
            finality_hash=target_finality_hash,
        )
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
                if not isinstance(g_old, int) or g_old < 0:
                    return self._result("HALT", "INVALID_WITNESS_GENERATION")
                previous = candidates.get(g_old)
                if previous is not None and not self._same_witness(previous, witness):
                    return self._result("HALT", "CONFLICTING_WITNESS")
                candidates[g_old] = witness

            expected = self.canonical.generation
            for g_old in sorted(candidates):
                if g_old != expected:
                    return self._result("HALT", "WITNESS_GENERATION_GAP")
                witness = candidates[g_old]
                new_state = witness.get("pi_new")
                if not isinstance(new_state, Mapping):
                    return self._result("HALT", "MISSING_NEW_STATE")
                if not self._valid_pointer_mapping(new_state):
                    return self._result("HALT", "INVALID_NEW_STATE")
                if new_state["generation"] != g_old + 1:
                    return self._result("HALT", "WITNESS_GENERATION_GAP")
                if new_state["epoch"] != self.canonical.epoch:
                    return self._result("HALT", "RECOVERY_EPOCH_MISMATCH")
                if new_state["height"] != self.canonical.height + 1:
                    return self._result("HALT", "RECOVERY_HEIGHT_GAP")
                if new_state["finality_height"] < self.canonical.finality_height:
                    return self._result("HALT", "RECOVERY_FINALITY_ROLLBACK")
                if (
                    new_state["finality_height"] == self.canonical.finality_height
                    and new_state["finality_hash"] != self.canonical.finality_hash
                ):
                    return self._result("HALT", "RECOVERY_FINALITY_CONFLICT")
                self.canonical = CanonicalPointer(**new_state)
                expected += 1

            return self._result("REPLAY", "RECOVERY_REPLAYED")
        finally:
            self.recovering = False

    @staticmethod
    def _same_witness(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
        return (
            a.get("token") == b.get("token")
            and a.get("pi_new") == b.get("pi_new")
        )

    @staticmethod
    def _valid_pointer_mapping(value: Mapping[str, Any]) -> bool:
        return all(
            isinstance(value.get(key), int if key in {"epoch", "generation", "height", "finality_height"} else str)
            for key in (
                "epoch",
                "generation",
                "height",
                "state_hash",
                "finality_height",
                "finality_hash",
            )
        ) and all(
            value[key] >= 0 for key in ("epoch", "generation", "height", "finality_height")
        )

    def _generation_matches(self, request: Mapping[str, Any]) -> bool:
        return request.get("generation") == self.canonical.generation + 1

    def _epoch_matches(self, request: Mapping[str, Any]) -> bool:
        return request.get("epoch") == self.canonical.epoch

    @staticmethod
    def _valid_nonnegative_ids(request: Mapping[str, Any]) -> bool:
        return all(
            isinstance(request.get(key), int) and not isinstance(request.get(key), bool) and request[key] >= 0
            for key in ("epoch", "generation", "height")
        )

    def _result(self, status: str, reason: str) -> BridgeResult:
        return BridgeResult(status, reason, self.canonical)
