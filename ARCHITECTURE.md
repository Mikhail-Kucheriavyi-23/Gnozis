# Gnozis Architecture — Core Boundary

## Rule

The Core is the smallest trusted execution boundary. It owns state transition, verification, persistence integrity, recovery, provenance, and audit primitives.

## Outside Core

Knowledge, research domains, user interfaces, connectors, commercial contracts, discovery, external models, and integrations are adapters/services. They may propose or consume information but cannot silently alter Core state.

## Migration rule

gnozis_core is the active clean-room namespace. platform/core is legacy and receives no new runtime features until migration evidence is complete.
