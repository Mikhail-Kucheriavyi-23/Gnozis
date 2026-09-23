"""Strict durable-witness validation for the Ψ-GNR terminal bridge.

This module is deliberately not a consensus implementation.  It verifies the
local structural contract around J_Ψ and delegates cryptographic proof
verification to an injected verifier.  Missing evidence is never upgraded to
authority; malformed or conflicting evidence fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

ProofVerifier = Callable[[str], bool]

STATUSES = {"PREPARED", "DECIDED", "LINEARIZED", "COMMITTED"}
AUTHORITATIVE_STATUSES = {"DECIDED", "LINEARIZED", "COMMITTED"}


@dataclass(frozen=True)
class WitnessValidation:
    status: str
    reason_code: str
    authoritative: bool = False


def _int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _pointer(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    integer_fields = ("epoch", "generation", "height", "finality_height")
    string_fields = ("state_hash", "finality_hash")
    return all(_int(value.get(k)) for k in integer_fields) and all(
        _nonempty(value.get(k)) for k in string_fields
    )


def validate_witness(
    witness: Mapping[str, Any],
    expected_old: Mapping[str, Any],
    *,
    verify_proof: ProofVerifier,
) -> WitnessValidation:
    """Validate one J_Ψ record against the currently reconstructed pointer."""
    status = witness.get("status")
    if status not in STATUSES:
        return WitnessValidation("HALT", "INVALID_WITNESS_STATUS")

    if status == "PREPARED":
        return WitnessValidation("REPLAY", "PREPARED_ABORT", authoritative=False)

    required = (
        "pi_old", "pi_new", "gamma_w", "gamma_f", "omega",
        "g_old", "g_new", "token",
    )
    if any(k not in witness for k in required):
        return WitnessValidation("HALT", "INCOMPLETE_WITNESS")

    if not _pointer(expected_old) or not _pointer(witness.get("pi_old")):
        return WitnessValidation("HALT", "INVALID_OLD_STATE")
    if dict(witness["pi_old"]) != dict(expected_old):
        return WitnessValidation("HALT", "WITNESS_OLD_STATE_MISMATCH")
    if not _pointer(witness.get("pi_new")):
        return WitnessValidation("HALT", "INVALID_NEW_STATE")

    if not _int(witness["g_old"]) or not _int(witness["g_new"]):
        return WitnessValidation("HALT", "INVALID_WITNESS_GENERATION")
    if witness["g_new"] != witness["g_old"] + 1:
        return WitnessValidation("HALT", "WITNESS_GENERATION_GAP")
    if witness["g_old"] != expected_old["generation"]:
        return WitnessValidation("HALT", "WITNESS_GENERATION_BASE_MISMATCH")
    if not _nonempty(witness.get("token")):
        return WitnessValidation("HALT", "MISSING_WITNESS_TOKEN")

    new_state = witness["pi_new"]
    if new_state["generation"] != witness["g_new"]:
        return WitnessValidation("HALT", "NEW_STATE_GENERATION_MISMATCH")
    if new_state["height"] != expected_old["height"] + 1:
        return WitnessValidation("HALT", "RECOVERY_HEIGHT_GAP")
    if new_state["epoch"] != expected_old["epoch"]:
        return WitnessValidation("HALT", "RECOVERY_EPOCH_MISMATCH")
    if new_state["finality_height"] < expected_old["finality_height"]:
        return WitnessValidation("HALT", "RECOVERY_FINALITY_ROLLBACK")
    if (
        new_state["finality_height"] == expected_old["finality_height"]
        and new_state["finality_hash"] != expected_old["finality_hash"]
    ):
        return WitnessValidation("HALT", "RECOVERY_FINALITY_CONFLICT")

    if not all(_nonempty(witness.get(k)) for k in ("gamma_w", "gamma_f", "omega")):
        return WitnessValidation("HALT", "UNVERIFIABLE_WITNESS_PROOFS")
    if not all(verify_proof(witness[k]) for k in ("gamma_w", "gamma_f", "omega")):
        return WitnessValidation("HALT", "INVALID_WITNESS_PROOF")

    return WitnessValidation("CONTINUE", "VALID_WITNESS", authoritative=True)


def detect_generation_conflict(witnesses: list[Mapping[str, Any]]) -> WitnessValidation | None:
    """Return HALT if two authoritative witnesses disagree for one generation."""
    seen: dict[int, Mapping[str, Any]] = {}
    for witness in witnesses:
        if witness.get("status") not in AUTHORITATIVE_STATUSES:
            continue
        g_old = witness.get("g_old")
        if not _int(g_old):
            return WitnessValidation("HALT", "INVALID_WITNESS_GENERATION")
        previous = seen.get(g_old)
        if previous is not None:
            same = (
                previous.get("token") == witness.get("token")
                and previous.get("pi_old") == witness.get("pi_old")
                and previous.get("pi_new") == witness.get("pi_new")
            )
            if not same:
                return WitnessValidation("HALT", "CONFLICTING_WITNESS")
        else:
            seen[g_old] = witness
    return None
