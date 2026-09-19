namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def Invariant (I : Psi → Prop) (p : Psi) : Prop := I p

structure ProofObligation (I : Psi → Prop) (candidate : Psi) where
  passed : Bool
  invariant_ok : I candidate
  viable : Prop

def FundamentalAdmission (I : Psi → Prop) (candidate : Psi) (proof : ProofObligation I candidate) : Prop :=
  proof.passed = true ∧ proof.invariant_ok

def EvolutionaryAdmission (I : Psi → Prop) (candidate : Psi) (proof : ProofObligation I candidate) : Prop :=
  proof.passed = true ∧ proof.invariant_ok ∧ proof.viable

def Admission (I : Psi → Prop) (candidate : Psi) (proof : ProofObligation I candidate) : Prop :=
  EvolutionaryAdmission I candidate proof

def SemanticCommit (I : Psi → Prop) (previous candidate : Psi)
    (proof : ProofObligation I candidate) : Prop :=
  Admission I candidate proof ∧ I previous

theorem commit_requires_admission
    (I : Psi → Prop)
    (previous candidate : Psi)
    (proof : ProofObligation I candidate)
    (h : SemanticCommit I previous candidate proof) :
    Admission I candidate proof := by
  exact h.1

theorem admitted_commit_preserves_invariant
    (I : Psi → Prop)
    (previous candidate : Psi)
    (proof : ProofObligation I candidate)
    (h : SemanticCommit I previous candidate proof) :
    I candidate := by
  exact h.2.2

end Gnozis
