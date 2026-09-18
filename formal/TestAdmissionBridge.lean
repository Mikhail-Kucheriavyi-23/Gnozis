namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def TestValid (passed : Bool) : Prop :=
  passed = true

structure ProofObligation (I : Psi → Prop) (candidate : Psi) where
  passed : Bool
  invariant_ok : I candidate
  viable : Prop

def ProofPasses
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate) : Prop :=
  proof.passed = true ∧ proof.invariant_ok ∧ proof.viable

def Admission
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate) : Prop :=
  ProofPasses I candidate proof

theorem proof_passes_implies_test_valid
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate)
    (h : ProofPasses I candidate proof) :
    TestValid proof.passed := by
  exact h.1

theorem admission_implies_test_valid
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate)
    (h : Admission I candidate proof) :
    TestValid proof.passed := by
  exact h.1

theorem admission_implies_invariant
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate)
    (h : Admission I candidate proof) :
    I candidate := by
  exact h.2.1

end Gnozis
