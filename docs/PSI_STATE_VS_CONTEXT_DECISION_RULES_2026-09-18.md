# Ψ State vs Context Decision Rules — 2026-09-18

Working decision rules for future architecture reviews.

## Rule 1 — State identity

A datum belongs to canonical Ψ when changing it changes what the agent/world state is, not merely how the system evaluates or executes a transition.

## Rule 2 — Transition context

A datum may remain outside Ψ when it specifies how a transition is generated, tested, bounded, authorized, or executed. Such context must be explicit at the layer where it is used.

## Rule 3 — State-relevant observation

External observations are not automatically Ψ. They become candidate Ψ state only after the system accepts them as semantically represented information.

## Rule 4 — Hidden dependence

If an undeclared mutable datum can change F(Ψ) while Ψ is unchanged, the implementation cannot claim strict Markov sufficiency.

## Rule 5 — No inflation

Do not add a datum to X/R merely because a function reads it. State expansion requires a semantic argument.

## Rule 6 — No concealment

Do not leave a semantically state-defining datum in an opaque closure merely to preserve a clean type signature.

## Rule 7 — Preserve optionality

When two representations remain semantically plausible, defer irreversible architecture and record both hypotheses.

## Rule 8 — Evidence before axiom

A classification becomes a core invariant only after concrete examples, adversarial tests, and transition semantics support it.

## Current consequence

No change to Psi is justified by the closure finding alone. The current canonical state remains exactly Psi = (X, R).

The next useful work is to test these decision rules against actual Gnozis flows: world observation, learning/memory, multi-agent interaction, and autonomous evolution.
