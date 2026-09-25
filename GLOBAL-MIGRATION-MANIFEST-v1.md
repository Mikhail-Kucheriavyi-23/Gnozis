# GNOZIS GLOBAL MIGRATION MANIFEST v1

Status: CONTROL PLANE / PRE-IMPLEMENTATION
Date: 2026-09-25
Source repository: Gnozis/main

## Canonical repository roles

| Repository | Role | Visibility |
|---|---|---|
| Gnozis-Core | operational self-evolving core | target / public status to verify |
| Gnozis-Research-Memory | machine-readable research, evidence, provenance, historical context | public |
| Gnozis-Exchange | external adapters and Internet boundary | public |
| Gnozis-Genesis | private Module Factory / commercial implementation | private |
| Gnozis | public product/discovery surface | public |

## Migration order

1. Research-Memory: research_machine and remaining evidence batches.
2. Exchange: reviewed external boundary batch.
3. Core: core/formal/tests/tools and Core-specific evidence.
4. Public Gnozis: retain only public product/discovery material.
5. Genesis: private implementation remains isolated; no automatic source import.
6. De-duplication/deletion: only after all target verification gates pass.

## Global invariants

- Source Gnozis is preserved until migration verification is complete.
- No credentials or private Genesis implementation cross a public boundary.
- Research-Memory is not a second operational Core.
- Exchange is not Core and cannot silently select Core transitions.
- Core retains deterministic selection, deep immutability, provenance/audit integrity, and trust-boundary constraints.
- GitHub state is not treated as runtime proof.
- Physical migration is distinct from semantic ownership.
- Every moved artifact has one canonical owner.

## Verification states

PLANNED -> TRANSFERRED -> CONTENT-VERIFIED -> STRUCTURE-VERIFIED -> TEST-VERIFIED -> CANONICAL

Failure at any gate -> HOLD; source remains intact.

## Current migration state

Research-Memory: PARTIAL (~72%).
Exchange: PREPARED, physical transfer blocked by target write/API access.
Core: PREPARED, physical transfer blocked until target is writable/available.
Genesis: PRIVATE BOUNDARY CONFIRMED.
Public Gnozis: not yet reduced to final public surface.

## No-deletion rule

No source file or directory is deleted from Gnozis solely because a manifest says it has a new owner. Deletion requires verified target content, structure, tests where applicable, and canonical-owner registration.

## Completion condition

Migration is 100% only when every in-scope artifact has:
- canonical target;
- verified content;
- verified structure;
- required test evidence;
- updated references/imports;
- provenance/migration record;
- no unresolved boundary violation.

Global percentage is orchestration progress, not test coverage or product readiness.
