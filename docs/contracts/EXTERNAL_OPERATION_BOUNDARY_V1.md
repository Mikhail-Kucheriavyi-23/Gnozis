# External Operation Boundary v1

External transport type does not select a Core state transition.

Transport types:
- observation
- hypothesis
- request
- candidate

They are mapped to typed information operations:
- observation -> observe
- hypothesis -> propose
- request -> request
- candidate -> candidate

The operation is metadata for authorization and routing only. It MUST NOT choose a Psi transition, selector, commit, or authority decision.

Canonical transition selection remains inside protected Core execution.

For v1, an external operation may be admitted as information without automatically causing a state transition. Execution requires an explicit internal operation mapping and the existing canonical proof/admission path.

Acceptance:
1. unsupported operation is rejected;
2. authorization is checked before any execution;
3. transport metadata cannot directly select a Core transition;
4. admitted information can be stored/analysed without implying state mutation.
