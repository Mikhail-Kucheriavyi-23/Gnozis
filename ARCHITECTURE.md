# Gnozis Architecture

## Product boundary

Gnozis is a modular infrastructure in which the trusted Core is deliberately small. Knowledge, research, user access, external connectors, discovery, and commercial workflows are separate layers.

## Trusted Core

`gnozis_core/` owns only:
- immutable state and transitions;
- transition validation and verification;
- deterministic state identity;
- persistence and fail-closed recovery;
- provenance;
- append-only audit primitives.

The Core does not contain domain knowledge, UI, commercial logic, external integrations, or model-specific code.

## Knowledge layer

Machine-readable knowledge repositories are external to Core. They can be public, private, or selectively shared. A user or project can attach a knowledge source without changing Core semantics.

## Research layer

Research sources and experiments remain separate from trusted runtime code. They can produce proposals/evidence consumed through explicit interfaces.

## Product layer

User-facing services provide seamless context restoration, project workspaces, connectors, permissions, discovery, and collaboration.

## Commercial layer

Commercial opportunities and contracts are product services above the Core. A discovered value proposition may become a public opportunity or a confidential/commercial workflow without exposing private Core or user data.

## Security boundary

Data access is explicit. Confidential project context, private knowledge, and commercial contracts must not become public merely because the Core can process them.

## Repository rule

Repositories are implementation boundaries, not architectural layers by themselves. The minimum useful number of repositories is preferred. A repository should exist only when it provides a meaningful security, ownership, release, or collaboration boundary.
