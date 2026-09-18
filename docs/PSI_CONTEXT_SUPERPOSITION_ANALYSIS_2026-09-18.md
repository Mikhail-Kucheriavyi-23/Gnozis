# Ψ Context Closure and Superposition Analysis — 2026-09-18

## Working hypothesis

The canonical fundamental state remains Ψ=(X,R). A transition may require contextual information, but the semantic question is whether that information is part of Ψ or is an undeclared external variable.

Distinguish three cases:

1. Intrinsic state — information already represented by X or R. It is legitimately available to F(Ψ).
2. Declared transition context — information intentionally supplied as part of a higher-level execution protocol. It is not automatically part of the fundamental Ψ and must not silently alter claims about F:Ψ→Ψ.
3. Undeclared mutable closure/external state — information that can change F(Ψ) while declared Ψ is unchanged. This breaks a strict Markov interpretation of F.

## Superposition hypothesis

For planning purposes, do not immediately collapse every useful contextual variable into X/R, and do not immediately ban every closure. Preserve a set of candidate representations until the semantic role is understood.

Let C be contextual information relevant to a transition. Possible representations are:
- C contained in X
- C encoded in R
- C supplied as explicit higher-level context
- C excluded as hidden state

The architectural choice should minimize premature loss of viable future representations while preserving a testable canonical boundary.

## Current implication

PsiTransition(function) is intentionally minimal, but its callable can currently close over arbitrary mutable state. Therefore the wrapper establishes the data boundary Ψ=(X,R), not yet the full purity/Markov theorem.

The current adversarial test demonstrates this distinction.

## Decision status

OPEN. No new state component is added to Ψ from this hypothesis yet.

## Next evidence

Before changing the mathematical model, classify concrete context examples:
- context that changes the physical/logical state itself;
- context that only changes evaluation;
- context that changes generation policy;
- context that is merely infrastructure;
- context that should remain inaccessible.

For each class, determine whether it belongs in X, R, explicit execution context, or nowhere in the canonical transition.

This analysis should precede any blanket closure ban or expansion of Ψ.
