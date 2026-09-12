# Endogenous topology generation

This is the next research gate after damage/recovery and unseen-damage testing.

The adapter now permits a new relation to arise from a local condition: two currently active nodes that are not already connected can form a weak directed relation.

Formally, for active `x,y`:

`(x,y) ∉ R  and active(x), active(y)  =>  (x,y) may enter R'`

The rule is intentionally local and bounded. It does not contain a target graph, repair oracle, global selector, reward model, or precomputed list of correct new edges.

This is **not yet autopoiesis**. Relation creation alone can generate arbitrary growth. The next test must therefore combine creation with decay/extinction and ask whether a viable organization can emerge and persist after damage.

Required criterion:

`R' != R` and `C(Ψ') != ∅`

where `C` denotes the chosen viability/autopoietic-closure condition. A positive result must be reproducible without an external selector.
