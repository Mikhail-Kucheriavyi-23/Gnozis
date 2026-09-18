namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- A candidate is viable at depth 1 when the supplied pool contains
    a distinct continuation satisfying the same invariant. -/
def DistinctContinuation
    (candidate continuation : Psi) : Prop :=
  continuation ≠ candidate

def Viable
    (I : Psi → Prop)
    (candidate : Psi)
    (pool : Psi → Prop) : Prop :=
  ∃ continuation : Psi,
    pool continuation ∧
    DistinctContinuation candidate continuation ∧
    I continuation

/-- A proof-passing candidate must itself satisfy the invariant and have
    an invariant-valid distinct continuation. -/
def ProofPasses
    (I : Psi → Prop)
    (candidate : Psi)
    (pool : Psi → Prop) : Prop :=
  I candidate ∧ Viable I candidate pool

theorem viable_witness
    (I : Psi → Prop)
    (candidate : Psi)
    (pool : Psi → Prop)
    (h : Viable I candidate pool) :
    ∃ continuation : Psi,
      pool continuation ∧
      continuation ≠ candidate ∧
      I continuation := by
  exact h

end Gnozis
