# Authorization Contract-to-Code Gap — v1

## Audit result

Existing Core already has explicit trust-boundary components:
- Context contains permissions.
- ExternalUpdate contains authorization.
- Core trust rules require explicit authority boundaries.
- Foreign evidence is explicitly non-authoritative.
- Canonical transitions require admission, provenance, safety, and persistence checks.

## Gaps against MARKET_INFORMATION_LOOP_V1

1. No canonical runtime Information object binds source, content reference, provenance, authorization status, and value class.
2. No canonical Authorization object defines scoped permissions for source, purpose, operation, destination, and validity.
3. No runtime enforcement currently maps the new UNKNOWN/ALLOWED/DENIED/EXPIRED/REVOKED states to processing admission.
4. Value classification is documented but not yet a Core runtime contract.
5. Opportunity is documented but not yet a Core runtime contract.
6. Existing Provenance is transition-focused (candidate/evidence/kernel) and does not yet carry the full information-flow provenance required by Market Information Loop v1.

## Existing controls retained

Do not replace existing admission/provenance/commit machinery. Extend it at the information boundary.

## Implementation boundary

Phase A.2 must add the smallest typed contracts needed for Information and Authorization, with fail-closed behavior for UNKNOWN/expired authorization. It must not redesign the canonical state machine or introduce external authority.

## Acceptance

The implementation must be able to reject an unauthorized information item before task processing, while preserving existing canonical transition authority and provenance rules.
