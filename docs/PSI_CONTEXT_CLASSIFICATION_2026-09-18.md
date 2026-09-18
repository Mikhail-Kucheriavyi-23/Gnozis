# Ψ Context Classification — 2026-09-18

This is a working classification, not a final mathematical axiom.

| Context type | Example in Gnozis | Candidate representation | Canonical effect |
|---|---|---|---|
| Intrinsic state | X elements, relation topology R | X / R | May affect F(Ψ) |
| Evolution history that is semantically part of the agent | prior accepted state/history-derived state | Explicit X/R representation if needed | May affect F only after being represented |
| Evaluation policy | invariant/test criteria | Explicit Test/Proof context | Must not silently become Ψ |
| Generation policy | candidate-generation strategy | Explicit Generator/Transition context | Must not be mistaken for intrinsic Ψ |
| Runtime resource | gas budget, execution quota | Explicit execution context | Controls admissibility/operation, not identity of Ψ |
| Safety/provenance metadata | authorization, provenance, audit evidence | Admission/commit layer | Must not silently alter Ψ semantics |
| Persistence/transport | database, bridge, GitHub, network | Infrastructure | Outside Ψ |
| Hidden mutable closure | undeclared external variable read by F | None until explicitly modeled | Violates strict Markov F(Ψ) |
| User/world observation | external information discovered through a bridge | First enters observation/input boundary | Must be represented before becoming canonical state |

## Important distinction

A value can influence an execution without being part of Ψ. The question is not whether information is used, but whether it is part of the semantic state whose transition is being claimed.

The canonical claim remains:

F: Ψ → Ψ

For any context C that changes F(Ψ), one of two things must be true:
1. C is explicitly part of the declared transition context and the claim is qualified accordingly; or
2. the semantically relevant portion of C is represented in Ψ.

Undeclared mutable closure remains inadmissible for a strict Markov claim.

## Planning implication

Do not expand Ψ merely to eliminate every dependency. First determine whether the dependency represents agent/world state, evaluation policy, generation policy, execution resources, or infrastructure.

This preserves architectural optionality while maintaining a testable semantic boundary.
