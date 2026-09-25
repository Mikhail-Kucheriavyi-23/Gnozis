# Gnozis Federated Graph

Independent Memory Sources can publish machine-readable relations into a shared discovery graph.

## Relation format

`subject --predicate--> object`

Each relation carries source identity, source revision, provenance, evidence references and verification state.

Example: `Math/theorem-17 --supports--> Physics/model-42`.

The relation is a claim with provenance, not an automatic truth assertion. Contradictory relations may coexist.

Publishing a relation does not grant access to another repository or to the private Kernel.

The protocol is intentionally small so independent research repositories can implement it without adopting the rest of Gnozis.
