namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def K0 (P : Psi) : Prop :=
  ∃ witness : P.X → Prop, ∀ x, witness x → witness x

structure RefinementProof (K : Psi → Prop) (P Q : Psi) where
  statement : Prop
  preserves : K P → K Q

def admitted {K : Psi → Prop} {P Q : Psi}
    (proof : RefinementProof K P Q) (h : K P) : Prop :=
  K Q

theorem meta_admission_preserves_K0
    (K : Psi → Prop)
    (proof : RefinementProof K P Q)
    (h : K P) :
    K Q := by
  exact proof.preserves h

end Gnozis
