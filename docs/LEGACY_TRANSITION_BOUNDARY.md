# Legacy Transition Boundary

## Status

The canonical fundamental transition path is `PsiTransition`:

`State -> Psi -> PsiTransition -> Psi' -> State`

`Engine` retains a `State -> State` callable only as an explicit compatibility boundary for existing clients. It is not the canonical Ψ evolution path.

## Rules

1. New core evolution code MUST use `PsiTransition`.
2. Legacy `State -> State` callables MUST NOT be presented as proof of the canonical Ψ semantics.
3. The compatibility path remains temporarily while existing callers and tests are audited.
4. Removal requires evidence that no supported caller depends on it and a regression pass after removal.
5. Any future mutation of the compatibility path must preserve the Engine contract: the transition must return a `State`.

## Evidence

Current `Engine` implementation explicitly distinguishes `PsiTransition` from the compatibility callable and validates the returned state type.

## Next gate

Audit all repository callers of `Engine(transition=...)`, classify them as canonical Ψ usage or legacy compatibility usage, then decide whether the compatibility path can be removed.
