# Architecture Contract Tests v1

The following invariants must become executable tests before production acceptance:

1. Unauthorized context is never assembled.
2. Revoked rights do not authorize subsequent access.
3. AI/client identity has no implicit write authority.
4. Public visibility cannot expose a private implementation through an indirect relation.
5. Knowledge publication preserves provenance and license metadata.
6. Context continuity works across sessions without granting additional rights.
7. GitHub is an integration/source surface, not the runtime authority.
8. Commercial rights are represented explicitly rather than inferred from visibility.
