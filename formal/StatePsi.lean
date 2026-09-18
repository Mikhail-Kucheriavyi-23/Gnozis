namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

structure State where
  psi : Psi

def toPsi (s : State) : Psi := s.psi

def fromPsi (p : Psi) : State := ⟨p⟩

theorem from_to_psi (s : State) :
    fromPsi (toPsi s) = s := by
  cases s
  rfl

theorem to_from_psi (p : Psi) :
    toPsi (fromPsi p) = p := by
  rfl

def SemanticExtensional (F : State → Psi) : Prop :=
  ∀ s, F s = toPsi s

theorem canonical_projection :
    SemanticExtensional toPsi := by
  intro s
  rfl

end Gnozis
