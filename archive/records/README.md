# Archive Records

Canonical machine-readable records live under this directory.

## Naming

Use the immutable record ID as the filename:

```
R-0001.yaml
C-0001.yaml
E-0001.yaml
X-0001.yaml
D-0001.yaml
A-0001.yaml
T-0001.yaml
```

## Rules

1. Never reuse an ID.
2. Never silently rewrite historical meaning.
3. Supersession creates a new record and explicit relations.
4. Every record declares its scope.
5. Evidence references are typed.
6. Engineering consequence is explicit, including `null`.
7. Archive records never directly authorize Core mutation.
8. A record may remain unresolved; `OPEN`, `UNVERIFIED` and `EVIDENCE_PENDING` are valid states.
9. Historical artifacts are referenced through provenance rather than treated as current implementation.
