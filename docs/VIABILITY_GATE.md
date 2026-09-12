# Viability gate for endogenous reorganization

The Drosophila-inspired adapter now has a minimal structural viability diagnostic.

For the active set A, construct an undirected graph from positive-weight relations between active nodes. Viability is the fraction of active nodes reachable from one active node:

V(Ψ) = |Reach(A)| / |A|.

Thus:

- V=0: no active organization;
- V=1: all active nodes belong to one connected organization;
- 0<V<1: fragmented organization.

This metric is deliberately diagnostic. It does not choose a candidate graph, reward a transition, or act as an external selector. The next experiment compares V before damage, after damage, and after endogenous reorganization.

Important limitation: connectivity alone is not sufficient for autopoiesis. A later gate must test persistence of activity and whether the organization regenerates its own enabling conditions.
