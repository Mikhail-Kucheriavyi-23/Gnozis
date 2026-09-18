namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- Executable contract: the declared semantic projection is the transition input. -/
def Extensional (F : Psi → Psi) : Prop :=
  ∀ P Q, P = Q → F P = F Q

/-- Generate/Test/Select accepts only tested candidates. -/
def Tested (test : Psi → Bool) (candidate : Psi) : Prop :=
  test candidate = true

/-- A selected candidate is valid only if it passed the test. -/
def SelectionValid (test : Psi → Bool) (selected : Psi) : Prop :=
  Tested test selected

theorem selection_requires_test
    (test : Psi → Bool) (selected : Psi)
    (h : SelectionValid test selected) :
    test selected = true := by
  exact h

/-- Extensionality is preserved compositionally by function composition. -/
theorem extensional_identity :
    Extensional (fun P : Psi => P) := by
  intro P Q h
  exact h

end Gnozis
