# Ψ Context Case Study: Memory — 2026-09-18

## Finding

`core/memory.py` separates `KernelMemory`, mutable `Workspace`, and `MemoryView`. This is a useful protection boundary, but the current memory model is not itself declared as part of Ψ.

## Classification

- KernelMemory: protected policy/knowledge boundary; not automatically X/R.
- Workspace: mutable operational context; not automatically X/R.
- MemoryView: access boundary combining the two; not semantic authority.
- A memory item that becomes part of the agent's represented world/self state is a candidate for X or R, but requires an explicit state-transition argument.

## Architectural consequence

Do not connect MemoryView directly to canonical `PsiTransition` merely because transitions may need memory. Doing so would silently turn memory into hidden state unless the memory contribution is explicitly represented in the transition contract or in Ψ.

A safer current flow is:

Memory / observation
  -> explicit context or candidate input
  -> transition/proof
  -> Ψ'
  -> commit

rather than:

MemoryView
  -> hidden closure
  -> F(Ψ)

## Superposition note

There are at least three plausible future models:

1. memory is external execution context;
2. selected memory is promoted into X/R;
3. memory remains separate but produces explicit observations/candidates.

No choice is finalized here.

## Status

OPEN research classification. No Core mutation performed.
