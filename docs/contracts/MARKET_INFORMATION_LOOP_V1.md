# Gnozis Market Information Loop v1

## Scope

Process information under explicit authorization boundaries and produce auditable outputs classified as PUBLIC, COMMERCIAL, PERSONAL, MIXED, or UNKNOWN.

## Core invariants

1. Interaction is information.
2. A result is information.
3. Incoming information requires authorization before use.
4. Output information has a value classification or remains UNKNOWN.
5. Repository priority is determined by market significance subject to current technical capability.
6. Task execution and opportunity discovery run in parallel.
7. Repositories are information surfaces, not authority sources for Core.
8. Access, copy, training, publication, and commercial reuse are separate permissions.
9. Behavioral evidence may support authorization but is not authorization authority.
10. Candidate information is not synonymous with state transition.

## Processing model

INPUT -> AUTHORIZATION -> STRUCTURING -> TASK -> PROCESSING -> EVIDENCE -> VALUE CLASSIFICATION -> OUTPUT -> OPPORTUNITY DISCOVERY -> REPOSITORY UPDATE

## Repository rule

Repository content is prioritized by market significance, bounded by current technical capability, and continuously expanded through task execution and opportunity discovery.

## Value classes

PUBLIC / COMMERCIAL / PERSONAL / MIXED / UNKNOWN

UNKNOWN is a safe intermediate state and is not permission to publish, reuse, train, or commercialize.

## Trust boundary

Research, user, partner, behavioral, and other repositories may provide candidate information or evidence. They do not acquire authority to modify protected Core behavior merely by storing information.

## Completion criterion

v1 is operational only when one concrete real-world task can reproducibly pass through authorization, structuring, processing, evidence capture, value classification, output, opportunity discovery, repository update, and replay.

## Explicit exclusions

- full mobile/personal application;
- broad plugin ecosystem;
- unrestricted external network access;
- automatic publication;
- automatic Core self-modification;
- full behavioral authorization engine;
- universal market ontology.

## Release gate

A feature enters the next release only when it identifies a concrete market task, required information, technical dependency, useful output, and testable acceptance criterion.
