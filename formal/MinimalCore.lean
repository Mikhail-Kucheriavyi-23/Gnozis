namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- K0 is an explicit protected predicate; the concrete Core predicate
    remains to be refined from root_invariant.py. -/
def K0 (P : Psi) : Prop :=
  ∃ witness : P.X → Prop, ∀ x, witness x → witness x

structure Transition (P : Psi) where
  next : Psi
  preserves_K0 : K0 P → K0 next

theorem accepted_transition_preserves_K0
    (t : Transition P)
    (h : K0 P) : K0 t.next := by
  exact t.preserves_K0 h

def Transition.compose (a : Transition P) (b : Transition a.next) : Transition P where
  next := b.next
  preserves_K0 := by
    intro h
    exact b.preserves_K0 (a.preserves_K0 h)

end Gnozis
