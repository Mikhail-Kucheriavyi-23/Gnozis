# Hidden-State / Markov Sufficiency Audit — 2026-09-18

## Question

Does the canonical transition depend only on the declared current state and explicit candidate/test inputs, or can hidden closure/external memory alter the result?

## Findings

The current canonical execution path passes current, generated candidates, and the explicit test into proof/admission/selection. core/proof.py contains no module-level mutable state and does not read external memory.

The existing tests/test_memory_independence.py exercises the legacy compatibility transition, not the canonical CanonicalExecutor path. Therefore those tests are useful evidence but are insufficient to close the canonical hidden-state claim.

## Required adversarial contract

For fixed declared inputs (current, candidate_pool, test):

1. repeated execution must produce the same accepted set;
2. changing unrelated external memory must not change the accepted set or selected Psi;
3. a test closure is allowed to carry behavior only insofar as that behavior is part of the explicit Test contract; it must not silently read undeclared mutable state and still be called Markov-sufficient;
4. the canonical proof layer must not introduce hidden global/operator state.

## Status

OPEN — canonical-path adversarial coverage is still required.

This is a semantic gate, not a claim that hidden-state dependence has been observed in production code.
