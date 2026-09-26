# Gnozis Architecture — Clean-Room Rewrite

## Product boundary
Gnozis is the public platform for knowledge, research, discovery, opportunities, capabilities, solutions, products, and contracts.

## Canonical repositories
- Gnozis — public platform
- Gnozis-Core — private trusted runtime
- Gnozis-Genesis — private value/development factory
- Gnozis-Research-Memory — private research and machine-readable memory

## Core principles
1. Seamless user context across devices, sessions, interfaces, and projects.
2. Context is owned by the user's authorized workspace, not by an AI session.
3. Least-privilege access: an AI/client receives only the context required for the current task.
4. Provenance, integrity, licensing, and authorization travel with meaningful objects.
5. Knowledge can progress through Research → Discovery → Opportunity → Capability → Solution → Product → Contract.
6. Public interfaces expose useful results and capabilities without exposing private implementation or confidential data.
7. Core is the authority for trusted state transitions and is not coupled to UI, GitHub, LLMs, payments, or domain-specific research.
8. Rewrite is clean-room: old code is evidence/source material, not the new architecture.

## Initial public modules
identity, projects, knowledge, research, discovery, opportunities, capabilities, solutions, products, contracts, evidence, provenance, API, SDK, integrations.

## Non-goals
- No separate Exchange core.
- No microservice split without demonstrated need.
- No AI authority over commits.
- No GitHub-as-runtime-database assumption.
