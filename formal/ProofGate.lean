namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def InPool (pool : List Psi) (p : Psi) : Prop := p ∈ pool

def Viable (I : Psi → Prop) (candidate : Psi) (pool : List Psi) : Prop :=
  ∃ continuation : Psi,
    InPool pool continuation ∧ continuation ≠ candidate ∧ I continuation

def ProofPasses (I : Psi → Prop) (candidate : Psi) (pool : List Psi) : Prop :=
  I candidate ∧ Viable I candidate pool

theorem proof_passes_implies_candidate_invariant
    (I : Psi → Prop) (candidate : Psi) (pool : List Psi)
    (h : ProofPasses I candidate pool) :
    I candidate := by
  exact h.1

theorem proof_passes_implies_viability
    (I : Psi → Prop) (candidate : Psi) (pool : List Psi)
    (h : ProofPasses I candidate pool) :
    Viable I candidate pool := by
  exact h.2

end Gnozis
