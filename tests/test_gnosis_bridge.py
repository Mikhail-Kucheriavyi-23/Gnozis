from gnosis_bridge import (
    ExecutionStatus,
    ExternalEvidence,
    classify_conflict,
    hash_payload,
    validate_external_evidence,
)


def evidence(**overrides):
    payload = {"transition": "W1"}
    values = dict(
        epoch=0,
        generation=0,
        height=1,
        command="inject",
        payload=payload,
        previous_hash="h0",
        payload_hash=hash_payload(payload),
        gamma_authorization="serialized-gamma-proof",
        omega_ordering="serialized-omega-proof",
    )
    values.update(overrides)
    return ExternalEvidence(**values)


def test_valid_structural_evidence_continues():
    result = validate_external_evidence(evidence())
    assert result.execution_status is ExecutionStatus.CONTINUE
    assert result.reason_code == "STRUCTURAL_EVIDENCE_VALID"


def test_provenance_hash_mismatch_rejects():
    result = validate_external_evidence(evidence(payload={"transition": "forged"}))
    assert result.execution_status is ExecutionStatus.REJECT
    assert result.reason_code == "PROVENANCE_HASH_MISMATCH"


def test_missing_authorization_never_becomes_authority():
    result = validate_external_evidence(evidence(gamma_authorization=""))
    assert result.execution_status is ExecutionStatus.REJECT
    assert result.reason_code == "UNVERIFIABLE_AUTHORIZATION"


def test_prepared_witness_requires_replay():
    result = validate_external_evidence(
        evidence(durable_witness={"status": "PREPARED", "token": "t"})
    )
    assert result.execution_status is ExecutionStatus.REPLAY
    assert result.reason_code == "PREPARED_REQUIRES_RECOVERY"


def test_conflicting_authority_fails_closed():
    result = classify_conflict(True)
    assert result.execution_status is ExecutionStatus.HALT
    assert result.halt_trigger is True
