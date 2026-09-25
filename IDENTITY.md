# Gnozis Identity & Access

Gnozis supports people and organizations as separate identity subjects.

A person may act as a researcher, contractor, partner, investor, maintainer or user. Roles are contextual and do not automatically grant system authority.

## Core rule

```
Identity ≠ Role ≠ Capability ≠ Kernel Authority
```

A verified identity does not make its claims trusted, and a repository contributor does not receive access to private Kernel state.

## Privacy

Gnozis should expose only the identity information required for a contribution, capability or contract.

## Organization relationships

People may act for organizations through explicit, scoped relationships.

## Capability model

Access is bounded:

```
Subject → Capability → Scope → Permission
```

This allows researchers and contractors to work with Gnozis without exposing proprietary Kernel internals.
