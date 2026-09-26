# Core Schema Minimums

Required schema concepts:

- State: state_id, version, canonical_payload, state_digest, provenance.
- Candidate: candidate_id, source_state_id, proposed_payload, provenance.
- ExecutionInput: input_type, state_id, state_digest, content_digest.
- Evidence: evidence_id, evidence_type, subject_id, content_digest, provenance, verification_status.
- Context: context_id, identity_ref, project_ref, task_ref, permissions, references, version, provenance.
- ExternalUpdate: update_id, target_surface, payload_digest, requested_by, authorization, status, evidence_ref.

Schemas are contracts, not implementations. Concrete serialization may be JSON, database records, or another deterministic representation, provided canonicalization and digest rules remain explicit.
