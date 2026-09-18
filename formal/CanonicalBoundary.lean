namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- Canonical semantic transition surface. -/
structure CanonicalTransition where
  run : Psi → Psi

/-- Generic compatibility transitions are intentionally a different type. -/
structure CompatibilityTransition where
  run : Psi → Psi

def IsCanonical (t : CanonicalTransition) : Prop := True

def SemanticCommitPath
    (t : CanonicalTransition) (before after : Psi) : Prop :=
  t.run before = after

/-- A compatibility transition is not itself a canonical semantic proof. -/
theorem compatibility_not_canonical_by_type
    (t : CompatibilityTransition) :
    ¬ (CanonicalTransition := ⟨t.run⟩) = t := by
  intro h
  cases h

end Gnozis
