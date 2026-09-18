namespace Gnozis

/-- Canonical semantic state. -/
structure Psi where
  X : Type
  R : X → X → Prop

/-- Protected kernel state is kept distinct from mutable workspace state. -/
structure Sigma where
  psi : Psi
  W : Type
  K : Type

/-- Root predicate over the protected kernel. -/
def Root (r : K → Prop) (k : K) : Prop := r k

/-- Semantic invariant I over Psi and protected-root invariant Root(K). -/
def J (I : Psi → Prop) (r : K → Prop) (s : Sigma) (k : K) : Prop :=
  I s.psi ∧ Root r k

/-- Admission is an abstract predicate; authority belongs to the proof
    carried by the transition, not to an external selector. -/
def Adm (A : Sigma → Prop) (s : Sigma) : Prop := A s

/-- A transition preserves the full system invariant J. -/
structure CertifiedTransition
    (I : Psi → Prop) (r : K → Prop)
    (s : Sigma) where
  next : Sigma
  nextK : K
  preserves_J : J I r s nextK → J I r nextK

/-- Central preservation obligation. -/
theorem certified_preservation
    (I : Psi → Prop) (r : K → Prop)
    (s : Sigma) (t : CertifiedTransition I r s)
    (h : J I r s t.nextK) :
    J I r t.nextK := by
  exact t.preserves_J h

end Gnozis
