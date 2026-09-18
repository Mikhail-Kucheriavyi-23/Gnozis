namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

structure Sigma where
  psi : Psi
  W : Type
  K : Type

/-- Current semantic obligations are documented separately from the
    protected-root predicate. Concrete I(Psi) remains to be refined from
    executable contracts; no hidden state is admitted here. -/
def I (P : Psi) : Prop := True

def Root (r : K → Prop) (k : K) : Prop := r k

def J (Inv : Psi → Prop) (r : K → Prop) (s : Sigma) (k : K) : Prop :=
  Inv s.psi ∧ Root r k

def Adm (A : Sigma → Prop) (s : Sigma) : Prop := A s

structure CertifiedTransition
    (Inv : Psi → Prop) (r : K → Prop)
    (s : Sigma) where
  next : Sigma
  nextK : K
  preserves_J : J Inv r s s.K → J Inv r next nextK

theorem certified_preservation
    (Inv : Psi → Prop) (r : K → Prop)
    (s : Sigma) (t : CertifiedTransition Inv r s)
    (h : J Inv r s s.K) :
    J Inv r t.next t.nextK := by
  exact t.preserves_J h

end Gnozis
