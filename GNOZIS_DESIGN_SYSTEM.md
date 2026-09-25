# Gnozis Design System & Information Architecture

**Status:** PRODUCT BASELINE v0.1  
**Date:** 2026-09-25

## Core principle

Gnozis must feel like one ecosystem even when knowledge, research, libraries and capabilities live in many repositories.

The public experience is human-first. Machine-readable contracts remain available without making the user interface feel like developer infrastructure.

## Experience layers

### 1. Human layer

Primary navigation:

- Explore
- Knowledge
- Research
- Connections
- Open Problems
- Capabilities
- Libraries

Users should encounter concepts, questions, relationships and useful results before schemas, manifests and repository internals.

### 2. Developer layer

Secondary technical access:

- GitHub repositories
- SDKs
- APIs
- schemas
- datasets
- validation tools
- contribution guides

### 3. Machine layer

Canonical structured records:

- identifiers
- types
- statuses
- provenance
- revisions
- content digests
- relationships
- verification state

The machine layer must remain deterministic and independently consumable.

## Repository naming

Use:

`gnozis-<domain>` for domain memory repositories.

Examples:

- gnozis-mathematics
- gnozis-physics
- gnozis-biology
- gnozis-engineering

Use:

`gnozis-<function>` for ecosystem infrastructure.

Examples:

- gnozis-sdk
- gnozis-schemas
- gnozis-tools

Use capability names only when a repository exposes a bounded reusable capability.

The private proprietary Kernel is not named as an open domain repository.

## Standard README order

Every public Gnozis repository should prefer this order:

1. What this is
2. Explore / useful entry points
3. What is contained
4. How knowledge is structured
5. Current status
6. How to contribute
7. Machine-readable resources
8. Provenance and licensing
9. Technical documentation

Technical implementation details should not obscure the purpose of the repository.

## Knowledge card model

Human-facing records should expose, where applicable:

- title;
- concise statement;
- domain;
- status;
- relationships;
- evidence count or source references;
- revision;
- update date;
- actions such as Explore, Evidence, Relations.

The exact UI may evolve, but the semantic fields must remain compatible with machine-readable records.

## Status vocabulary

Use a common vocabulary across the ecosystem:

- DISCOVERED
- PROPOSED
- SUPPORTED
- VERIFIED
- CONNECTED
- OPEN
- QUARANTINED
- REJECTED

Status describes evidence or processing state. It must not silently imply scientific certainty where the underlying record is a hypothesis, interpretation or unresolved question.

## Visual language

The ecosystem should use a consistent visual identity across domain repositories and future web interfaces:

- restrained;
- scientific;
- modern;
- information-dense but readable;
- recognizable Gnozis hierarchy;
- consistent typography and terminology;
- clear separation of human content and machine infrastructure.

Do not use mystical or pseudo-scientific language in public product documentation.

## Information hierarchy

Preferred conceptual hierarchy:

```
Domain
  -> Topic
    -> Concept
      -> Evidence / Model / Question
        -> Relationships
          -> Research
            -> Capability
```

Cross-domain relationships are first-class objects.

## Public/private boundary

Public surfaces explain what Gnozis provides and expose reusable open resources.

They must not expose proprietary Kernel internals, protected state, private governance mechanisms or confidential commercial algorithms.

## Contribution model

A contributor should be able to:

1. discover a domain;
2. understand its purpose;
3. clone or fork the repository;
4. find the machine-readable schema;
5. make a contribution;
6. preserve provenance;
7. validate the contribution;
8. submit it for review.

## Design objective

The ecosystem should be recognizable as Gnozis whether a person enters through a knowledge page, a research repository, a GitHub project, an SDK or a capability.

**One ecosystem. Multiple surfaces. One information language.**
