namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def K0 (K : Psi → Prop) : Prop := ∀ P, K P → K P

/-- Exact logical shape of Python preserve_root:
    the protected predicate holds before and after. -/
def preserves (K : Psi → Prop) (before after : Psi) : Prop :=
  K before ∧ K after

structure Transition (K : Psi → Prop) (P : Psi) where
  next : Psi
  preserves_proof : K P → K next

theorem preserve_root
    (K : Psi → Prop)
    (t : Transition K P)
    (h : K P) : K t.next := by
  exact t.preserves_proof h

def Transition.compose
    (a : Transition K P)
    (b : Transition K a.next) : Transition K P where
  next := b.next
  preserves_proof := by
    intro h
    exact b.preserves_proof (a.preserves_proof h)

theorem compose_preserves_root
    (K : Psi → Prop)
    (a : Transition K P)
    (b : Transition K a.next)
    (h : K P) :
    K (Transition.compose a b).next := by
  exact (Transition.compose a b).preserves_proof h

end Gnozis
