# Target Public Architecture — Gnozis Evidence Boundary

**Status:** PROPOSED → migration baseline
**Date:** 2026-09-25

## Product identity

**Gnozis** is the public product/evidence surface.

The public surface exposes selected research, evidence, contracts, validated modules and opportunities. It is not the authority root for the protected Kernel or Genesis factory.

## Target ecosystem

```
Gnozis-Evidence
        ↓ candidate evidence / research
Gnozis-Kernel
        ↓ verified capability
Genesis
        ↓ bounded generated modules
Gnozis
        ↓ public selected outputs
partners / testers / users
```

The exact public/private direction of individual artifacts is governed by provenance, contract and authorization; repository visibility alone does not establish permission.

## Evidence Plane

The target **Gnozis-Evidence** role replaces the narrower transitional concept of **Gnozis-Research-Memory**.

It may contain:
- mathematical corpus;
- research records;
- evidence and provenance;
- counterexamples and negative results;
- historical project context;
- machine-readable AI context;
- audits and research experiments.

Evidence remains evidence. It does not become Kernel authority merely by being stored or referenced.

## Public Gnozis

The public Gnozis repository remains responsible for:
- inspectable opportunities;
- selected contracts;
- selected modules;
- evidence summaries;
- provenance references;
- research-facing public material;
- partner/tester entry points.

## Migration rule

Do not physically rename or split repositories until:
1. target ownership of current files is classified;
2. references and provenance are inventoried;
3. contracts are defined;
4. CI/package metadata are mapped;
5. the migration can be performed without silently losing historical evidence.

## Current transitional state

- `Gnozis` is the existing public repository.
- `Genezis` is the existing protected engineering repository.
- `Gnozis-Research-Memory` is the intended transitional evidence/context role; the physical repository has not yet been established by this step.
- Repository names are not yet treated as proof that the target split is implemented.

## Acceptance gate

The Evidence rename/split is complete only when the resulting repository has a coherent evidence-plane scope and all transferred artifacts retain provenance to their source history.
