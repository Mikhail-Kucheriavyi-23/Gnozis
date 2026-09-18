namespace Gnozis

/-- Minimal machine-checkable semantic core target.
    This file intentionally contains no external libraries or AI model. -/

structure Psi where
  X : Type
  R : X -> X -> Prop

structure Transition (P : Psi) where
  next : Psi
  preserves_K0 : Prop

def PreservesK0 (t : Transition P) : Prop := t.preserves_K0

theorem accepted_transition_preserves_K0
    (t : Transition P)
    (h : PreservesK0 t) : PreservesK0 t := by
  exact h

end Gnozis
