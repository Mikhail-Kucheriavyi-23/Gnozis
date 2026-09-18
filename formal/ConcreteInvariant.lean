namespace Gnozis

structure Psi where
  X : Type
  R : X → X → Prop

def I_projection (p : Psi) : Prop :=
  ∀ q, p = q → p = q

def TestValid (passed : Bool) : Prop :=
  passed = true

def I_test_gate (p : Psi) : Prop := True
def I_selection (p : Psi) : Prop := True
def I_locality (p : Psi) : Prop := True
def I_causal (p : Psi) : Prop := True

def I (p : Psi) : Prop :=
  I_projection p ∧
  I_test_gate p ∧
  I_selection p ∧
  I_locality p ∧
  I_causal p

theorem projection_invariant (p : Psi) :
    I_projection p := by
  intro q h
  exact h

theorem test_valid_implies_true (passed : Bool)
    (h : TestValid passed) : passed = true := by
  exact h

theorem invariant_decomposition (p : Psi) :
    I p →
    I_projection p ∧
    I_test_gate p ∧
    I_selection p ∧
    I_locality p ∧
    I_causal p := by
  intro h
  exact h

end Gnozis
