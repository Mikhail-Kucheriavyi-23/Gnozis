# Core Schema Minimums

Required schema concepts:

- State: state_id, version, canonical_payload, state_digest, provenance.
- Candidate: candidate_id, source_state_id, proposed_payload, provenance.
- ExecutionInput: input_type, state_id, state_digest, content_digest.
- Evidence: evidence_id, evidence_type, subject_id, content_digest, provenance, verification_status.
- Context: context_id, identity_ref, project_ref, task_ref, permissions, references, version, provenance.
- ExternalUpdate: update_id, target_surface, payload_digest, requested_by, authorization, status, evidence_ref.

## Runtime ExecutionInput contract

ExecutionInput is not schema-only. CanonicalExecutor.step() requires it at runtime.

For the supplied Psi:

- state_digest = SHA256(repr((psi.x, psi.relations)))
- state_id = SHA256("gnozis-state-id-v1:" || state_digest)

The executor must compare both values before transition execution and fail closed on mismatch. Therefore an ExecutionInput issued for S1 cannot be executed against S2.

content_digest participates in the deterministic execution-input identity:

ID(E) = SHA256(input_type || state_id || state_digest || content_digest).

Schemas are contracts, not implementations. Concrete serialization may be JSON, database records, or another deterministic representation, provided canonicalization and digest rules remain explicit.
