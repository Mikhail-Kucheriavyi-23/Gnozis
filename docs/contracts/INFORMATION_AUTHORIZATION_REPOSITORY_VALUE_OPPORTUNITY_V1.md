# Gnozis Information Contracts v1

## Information
Information is any input, interaction, observation, transformation result, or output that can be represented, related, evidenced, or routed.
Required fields: information_id, source, content_reference, provenance, timestamp_or_sequence, authorization_status, value_class.
UNKNOWN authorization or value does not imply permission.

## Authorization
Authorization precedes operational use.
Authorization states: UNKNOWN, ALLOWED, DENIED, EXPIRED, REVOKED.
Authorization is scoped by source, purpose, operation, destination, and validity.
Access, copy, transformation, training, publication, and commercial reuse are distinct permissions.
Fail-closed rule: UNKNOWN or expired authorization cannot authorize restricted use.
Behavioral evidence may support a decision but is not authority.

## Repository
A repository is an information surface, not Core authority.
Repository priority = market significance intersect current technical capability.
Repository updates require provenance and authorization.
Repositories may contain research, market, commercial, personal, or behavioral evidence.
Repository content cannot directly mutate protected Core behavior.

## Value
Value classes: PUBLIC, COMMERCIAL, PERSONAL, MIXED, UNKNOWN.
Classification describes intended/useful value; it is not itself permission.
UNKNOWN remains non-publishable/non-commercializable until separately authorized.
A single information item may have multiple authorized destination-specific value views.

## Opportunity
Opportunity is a derived information object, not an automatic fact.
Minimum states: OBSERVED, CANDIDATE, RESEARCHING, PROTOTYPING, VALIDATED, REJECTED.
An opportunity requires evidence references and a derivation/provenance link to its inputs.
Task execution and opportunity discovery occur in parallel.
Opportunity state must never grant authority by itself.

## Processing invariant
INPUT -> AUTHORIZATION -> STRUCTURING -> TASK -> PROCESSING -> EVIDENCE -> VALUE -> OUTPUT -> OPPORTUNITY -> REPOSITORY UPDATE

## Acceptance
A conforming implementation must preserve provenance, authorization scope, value classification, and repository trust boundaries across the complete processing path.
