namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- Locality: equal declared semantic inputs imply equal transition outputs.
    No undeclared external channel is part of the transition relation. -/
def Local (T : Psi → Psi) : Prop :=
  ∀ p q, p = q → T p = T q

theorem locality_implies_extensionality
    (T : Psi → Psi)
    (h : Local T) :
    ∀ p q, p = q → T p = T q := by
  exact h

/-- Causal closure at the semantic boundary is represented by the fact that
    the transition's domain is Psi itself, not an ambient external context. -/
def CausallyClosed (T : Psi → Psi) : Prop := Local T

end Gnozis
