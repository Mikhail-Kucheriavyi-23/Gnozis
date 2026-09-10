from __future__ import annotations

"""External Evidence Contract (EEC) for the GNOSIS terminal bridge.

This module is intentionally a verification boundary, not a consensus engine.
It never upgrades unverifiable evidence into authority.
"""

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping


class ExecutionStatus(str, Enum):
    CONTINUE = "CONTINUE"
    REJECT = "REJECT"
    HALT = "HALT"
    REPLAY = "REPLAY"


class WitnessStatus(str, Enum):
    PREPARED = "PREPARED"
    DECIDED = "DECIDED"
    LINEARIZED = "LINEARIZED"
    COMMITTED = "COMMITTED"


@dataclass(frozen=True)
class EvidenceResult:
    execution_status: ExecutionStatus
    reason_code: str
    halt_trigger: bool = False


@dataclass(frozen=True)
class ExternalEvidence:
    epoch: int
    generation: int
    height: int
    command: str
    payload: Mapping[str, Any]
    previous_hash: str
    payload_hash: str
    gamma_authorization: str
    omega_ordering: str
    gamma_finality: str | None = None
    base_epoch: int | None = None
    base_height: int | None = None
    epoch_transition_proof: str | None = None
    durable_witness: Mapping[str, Any] | None = None


def hash_payload(payload: Any) -> str:
    """Return the canonical SHA-256 digest used for local evidence binding."""
    import json

    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_external_evidence(evidence: ExternalEvidence) -> EvidenceResult:
    """Validate the EEC without pretending to verify unavailable signatures.

    Cryptographic Γ/Ω/ΓF verification is deliberately an explicit boundary:
    non-empty serialized proofs are evidence to be handed to a real verifier,
    not proof that this structural validator can manufacture locally.
    """
    if evidence.command not in {"status", "inject", "step", "evolution"}:
        return EvidenceResult(ExecutionStatus.REJECT, "UNKNOWN_COMMAND")

    if not all(
        _nonnegative_int(v)
        for v in (evidence.epoch, evidence.generation, evidence.height)
    ):
        return EvidenceResult(ExecutionStatus.REJECT, "INVALID_IDENTIFIER")

    if not evidence.previous_hash or not evidence.payload_hash:
        return EvidenceResult(ExecutionStatus.REJECT, "MISSING_PROVENANCE")

    if hash_payload(evidence.payload) != evidence.payload_hash:
        return EvidenceResult(ExecutionStatus.REJECT, "PROVENANCE_HASH_MISMATCH")

    witness = evidence.durable_witness
    if witness is not None:
        status = witness.get("status")
        if status not in {s.value for s in WitnessStatus}:
            return EvidenceResult(ExecutionStatus.REJECT, "INVALID_WITNESS_STATUS")
        if status == WitnessStatus.PREPARED.value:
            return EvidenceResult(ExecutionStatus.REPLAY, "PREPARED_REQUIRES_RECOVERY")

    # No authority is granted merely because serialized proofs are present.
    if not evidence.gamma_authorization or not evidence.omega_ordering:
        return EvidenceResult(ExecutionStatus.REJECT, "UNVERIFIABLE_AUTHORIZATION")

    return EvidenceResult(ExecutionStatus.CONTINUE, "STRUCTURAL_EVIDENCE_VALID")


def classify_conflict(conflict: bool) -> EvidenceResult:
    """Apply the Ψ fail-closed rule to conflicting authority evidence."""
    if conflict:
        return EvidenceResult(ExecutionStatus.HALT, "CONFLICTING_AUTHORITY", True)
    return EvidenceResult(ExecutionStatus.CONTINUE, "NO_CONFLICT")
