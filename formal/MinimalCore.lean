namespace Gnozis

/-- Semantic core: Psi=(X,R). -/
structure Psi where
  X : Type
  R : X → X → Prop

/-- Kernel invariant as a predicate over semantic states.
    The concrete Gnozis K0 will refine this definition later. -/
def K0 (P : Psi) : Prop := True

/-- A transition is admitted only together with an invariant-preservation proof. -/
structure Transition (P : Psi) where
  next : Psi
  preserves_K0 : K0 P → K0 next

theorem accepted_transition_preserves_K0
    (t : Transition P)
    (h : K0 P) : K0 t.next := by
  exact t.preserves_K0 h

/-- Composition preserves K0 when both transitions carry preservation proofs. -/
def Transition.compose (a : Transition P) (b : Transition a.next) : Transition P where
  next := b.next
  preserves_K0 := by
    intro h
    exact b.preserves_K0 (a.preserves_K0 h)

end Gnozis
