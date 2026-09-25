# Standard Memory Repository Structure

```
<repository>/
├── README.md
├── manifest.yaml
├── knowledge/
├── research/
├── open-problems/
├── connections/
├── provenance/
├── schema/
├── validation/
└── LICENSE
```

## Directory semantics

- `knowledge/` — structured domain records.
- `research/` — experiments, methods and research records.
- `open-problems/` — unresolved questions and challenges.
- `connections/` — cross-domain relationships with source provenance.
- `provenance/` — source and revision evidence.
- `schema/` — machine-readable record definitions.
- `validation/` — repository-level validation rules and fixtures.

Domain-specific subdirectories may be added without changing the common protocol.
