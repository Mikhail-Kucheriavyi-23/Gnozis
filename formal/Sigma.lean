namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

structure Sigma where
  psi : Psi
  W : Type
  K : Type

def Root (r : K → Prop) (k : K) : Prop := r k

def J (I : Psi → Prop) (r : K → Prop) (s : Sigma) (k : K) : Prop :=
  I s.psi ∧ Root r k

def Adm (A : Sigma → Prop) (s : Sigma) : Prop := A s

structure CertifiedTransition
    (I : Psi → Prop) (r : K → Prop)
    (s : Sigma) where
  next : Sigma
  nextK : K
  preserves_J : J I r s s.K → J I r next nextK

theorem certified_preservation
    (I : Psi → Prop) (r : K → Prop)
    (s : Sigma) (t : CertifiedTransition I r s)
    (h : J I r s s.K) :
    J I r t.next t.nextK := by
  exact t.preserves_J h

end Gnozis
