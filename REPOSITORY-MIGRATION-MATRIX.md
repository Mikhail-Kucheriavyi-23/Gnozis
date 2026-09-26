# Repository Migration Matrix

Status: audit-first. No repository is deleted by this document.

| Repository | Role found | Decision | Reason |
|---|---|---|---|
| Gnozis | public product/Core candidate | KEEP | public entry point and open development |
| Gnozis-Genesis | private evolution/module-factory system | KEEP PRIVATE | proprietary orchestration, diagnostics, governance and commercial-sensitive logic |
| Gnozis-Research-Memory | machine-readable research/knowledge | KEEP | reusable knowledge source for projects |
| Gnozis-Exchange | empty | HOLD / likely DELETE | no demonstrated independent boundary |
| Thoth | empty | HOLD / likely DELETE | no demonstrated independent boundary |
| Athena | empty | HOLD / likely DELETE | no demonstrated independent boundary |
| Hephaestus | empty | HOLD / likely DELETE | no demonstrated independent boundary |
| Daedalus | empty | HOLD / likely DELETE | no demonstrated independent boundary |
| Prometheus | near-empty | AUDIT THEN DELETE/MERGE | insufficient evidence for independent boundary |

## Migration rules

1. Preserve unique IP, research records, provenance, history and contracts before deletion.
2. Do not copy private Genesis implementation into public Gnozis.
3. Do not move research data into trusted Core merely for convenience.
4. Knowledge must remain attachable as an explicit source with provenance and permissions.
5. Commercial workflows must not expose confidential project context.
6. Repository count is optimized only after security, ownership, release and collaboration boundaries are proven.
7. Empty repositories are not product features.

## Target topology

Minimum expected topology:

- Gnozis — public product and open development.
- Gnozis-Genesis — private protected engine/module factory.
- Gnozis-Research-Memory — reusable machine-readable knowledge/evidence.
- Gnozis-Exchange — optional separate boundary only if contract/marketplace security or ownership requires it.

The final decision for Exchange remains open until the commercial workflow is specified.
