namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

structure ProofObligation (I : Psi → Prop) (candidate : Psi) where
  passed : Bool
  invariant_ok : I candidate
  viable : Prop

def Admission
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate) : Prop :=
  proof.passed = true ∧ proof.invariant_ok ∧ proof.viable

/-- Selection is represented as choosing one member of the admitted candidate
    relation; it cannot independently manufacture an unadmitted candidate. -/
def Selected
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate) : Prop :=
  Admission I candidate proof

structure SelectionCommit
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate) where
  selected : Selected I candidate proof
  committed : Psi
  commit_eq : committed = candidate

theorem selection_requires_admission
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate)
    (s : SelectionCommit I candidate proof) :
    Admission I candidate proof := by
  exact s.selected

theorem commit_is_selected_candidate
    (I : Psi → Prop)
    (candidate : Psi)
    (proof : ProofObligation I candidate)
    (s : SelectionCommit I candidate proof) :
    s.committed = candidate := by
  exact s.commit_eq

end Gnozis
