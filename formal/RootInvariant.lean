namespace Gnozis

/-- The mathematical Psi representation mirrors core/state.py. -/
structure Psi where
  X : Type
  R : X → X → Prop

/-- An invariant is a predicate on semantic Psi states. -/
def RootInvariant (K : Psi → Prop) : Prop := ∀ P, K P → K P

/-- A transition is admitted with an explicit preservation proof. -/
structure Transition (K : Psi → Prop) (P : Psi) where
  next : Psi
  preserves : K P → K next

/-- Root invariant preservation for an admitted transition. -/
theorem preserve_root
    (K : Psi → Prop)
    (t : Transition K P)
    (h : K P) : K t.next := by
  exact t.preserves h

/-- Preservation composes across sequential admitted transitions. -/
def Transition.compose
    (a : Transition K P)
    (b : Transition K a.next) : Transition K P where
  next := b.next
  preserves := by
    intro h
    exact b.preserves (a.preserves h)

theorem compose_preserves_root
    (K : Psi → Prop)
    (a : Transition K P)
    (b : Transition K a.next)
    (h : K P) :
    K (Transition.compose a b).next := by
  exact (Transition.compose a b).preserves h

end Gnozis
