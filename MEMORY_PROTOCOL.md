# Gnozis Memory Protocol

Gnozis treats external memory as a controlled evidence source.

## Retrieval is not trust

Discover → Registry → Retrieve → Integrity → Schema → Provenance → Evidence → Consume.

Each step has a separate purpose.

## Safe synchronization

The preferred model is pull-based. A registered source may be read without receiving permission to mutate private Kernel state. Trusted synchronization references a specific revision and content digest.

## Fail closed

The system rejects unknown, revoked, corrupted, incompatible or unverifiable sources.

## Kernel boundary

A Memory Source cannot directly change Kernel state, policy or evolution. Even consumable memory enters through existing Kernel contracts: Candidate → Test → Select → Evolve → Verify → Commit.

## Revision safety

A newer repository revision is a new candidate for synchronization. It does not silently replace previously consumed memory.

## Auditability

Consumption records should preserve source identity, revision, digest, policy and verification results.
