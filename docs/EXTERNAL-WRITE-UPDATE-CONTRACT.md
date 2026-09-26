# External Write / Update Contract

## Purpose

Core and governed higher layers may generate or update useful material in downstream repositories and public/work surfaces without making those surfaces trusted authorities.

## Flow

Request → authorize → validate → produce deterministic payload → write/update downstream → capture result → record provenance/evidence.

## Required fields

- update_id
- target_surface
- target_reference
- payload_digest
- requested_by
- authorization_scope
- validation_status
- result_reference
- provenance_id
- rollback_reference

## Rules

1. No downstream surface may directly mutate trusted Core state.
2. A successful external write is not proof that the content is correct.
3. Every update is attributable and versioned.
4. Failed or partial writes remain observable evidence.
5. Updates must be replayable or explicitly marked non-replayable.
6. Rollback information is retained when the target supports it.
7. Connectors remain replaceable adapters behind the contract.
