# External/Internal Execution Boundary v1

## Purpose

Define which execution paths may receive external information.

## External path

External information MUST enter through an authorized information boundary before canonical processing:

External Information -> Information Authorization -> AuthorizedExecution -> CanonicalExecutor.

The external bridge is responsible for authorization. CanonicalExecutor remains responsible for state identity, proof, admission, selection where applicable, and commit.

## Internal canonical paths

CanonicalExecutor.step/evolve and Uroboros.canonical are internal Core execution surfaces. They are not external-information APIs. Existing internal callers may use them when their inputs are already inside the protected Core contract.

Uroboros.evolutionary and LegacyEngine are compatibility surfaces and are not canonical external-information authority.

## Non-bypass rule

No external adapter, repository, plugin, or evidence store may call canonical transition execution while bypassing the authorization boundary.

A future external integration MUST terminate at AuthorizedExecution or an equivalent contract that proves the same authorization invariant.

## Evidence requirement

A claim of global non-bypass requires an adversarial inventory of all external adapters and reachable execution entry points. This document defines the contract but does not by itself prove global non-bypass.

## Acceptance

- external-information tests use AuthorizedExecution;
- unauthorized statuses cannot invoke a transition;
- canonical executor contracts remain unchanged;
- compatibility paths are not reclassified as external authority.
