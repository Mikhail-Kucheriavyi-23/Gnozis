# Value Pipeline v1

## Purpose

Transform authorized information into useful outputs without confusing value classification with permission.

## Pipeline

Information
-> Authorization
-> Structure
-> Analysis
-> Evidence
-> Value Classification
-> Output Proposal
-> Destination Authorization
-> Output

## Value classes

PUBLIC
COMMERCIAL
PERSONAL
MIXED
UNKNOWN

## Rules

1. Input authorization permits processing only within its authorized scope.
2. Output destination requires its own authorization; input authorization is not automatically output authorization.
3. Value classification describes the useful destination class; it does not grant publication or commercial permission.
4. UNKNOWN value remains unresolved and cannot be treated as permission.
5. An output proposal is not an executed external action.
6. External side effects require an explicit destination and operation authorization.
7. Evidence and provenance must remain attached through transformations.
8. Public value may be produced without making private source material public.

## Acceptance

A conforming implementation can take an authorized information object, produce a structured value classification and output proposal, and preserve provenance without performing an unauthorized external side effect.
