# R2 ExecutionInput Runtime Binding — 2026-09-26

## Gap

Before this change, ExecutionInput existed only as a documented schema. CanonicalExecutor.step() accepted Psi and PsiTransition directly and did not verify the declared execution state identity or digest.

## Runtime contract

CanonicalExecutor.step(psi, transition, execution_input) now performs the following before invoking transition:

1. require ExecutionInput;
2. derive state_digest from the supplied canonical Psi;
3. derive deterministic state_id from that digest;
4. compare both declared values with the supplied Psi;
5. fail closed on mismatch;
6. invoke the transition only after successful binding.

State digest:

SHA256(repr((psi.x, psi.relations)))

State identity:

SHA256("gnozis-state-id-v1:" || state_digest)

Execution-input identity:

SHA256(input_type || state_id || state_digest || content_digest)

## Adversarial evidence

The runtime test suite now verifies:

- ExecutionInput is required by the canonical step API.
- An ExecutionInput created for S1 is rejected when execution is attempted with S2.
- The transition is not invoked after state substitution is detected.
- A tampered state_digest is rejected before history mutation.
- A valid ExecutionInput still permits the canonical transition and exactly one accepted history record.

## Scope

This closes the specific state-substitution gap at CanonicalExecutor.step(). It does not claim that content_digest alone proves content provenance, and it does not claim that all Recovery/Replay binding gaps are closed.

## Branch / PR

Branch: r2/execution-input-runtime-binding

PR: #18 — R2: enforce ExecutionInput state binding at runtime
