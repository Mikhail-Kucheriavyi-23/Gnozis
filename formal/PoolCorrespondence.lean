namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

/-- A finite executable candidate pool is represented by membership. -/
def InPool (pool : List Psi) (p : Psi) : Prop :=
  p ∈ pool

def Viable
    (I : Psi → Prop)
    (candidate : Psi)
    (pool : List Psi) : Prop :=
  ∃ continuation : Psi,
    InPool pool continuation ∧
    continuation ≠ candidate ∧
    I continuation

/-- List membership gives the exact witness needed by the depth-1 proof. -/
theorem executable_pool_has_witness
    (I : Psi → Prop)
    (candidate continuation : Psi)
    (pool : List Psi)
    (hmem : InPool pool continuation)
    (hne : continuation ≠ candidate)
    (hinv : I continuation) :
    Viable I candidate pool := by
  exact ⟨continuation, hmem, hne, hinv⟩

end Gnozis
