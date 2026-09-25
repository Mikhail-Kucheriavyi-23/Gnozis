# Gnozis Memory Registry

The Memory Registry is the catalog of Memory Sources available to the Gnozis ecosystem.

It records source identity, domain, protocol version, permissions, synchronization policy, pinned revision, verification state and revocation state.

## Lifecycle

```
DISCOVERED
  -> REGISTERED
  -> AUTHORIZED
  -> SYNCING
  -> VERIFIED
  -> ACTIVE
```

A source can become QUARANTINED, REVOKED or DISABLED without losing historical provenance.

## Important distinction

The Registry does not make every record trusted.

It authorizes a source to participate in the Memory Source Protocol. Individual revisions still require provenance, validation and verification before they may influence trusted Kernel state.

## Security rules

- Unknown sources cannot influence trusted state.
- Registration cannot bypass provenance validation.
- Mutable branch names are not sufficient trusted references.
- DELETE and history rewriting are not granted by default.
- Revocation preserves historical provenance.
- Registry metadata is policy metadata, not domain evidence.

The private Kernel can therefore maintain a stable map of its external memory network without importing the whole network into Kernel state.
