# GNOZIS Migration Root Matrix v1

Baseline: 03b92113e6d2cc2801e4f59a2a8f1c4fc285ccc3
Manifest: GNOZIS-MIGRATION-MANIFEST-V1-2026-09-25
Status: CLASSIFICATION FREEZE FOR REVIEW

| Source | Target | Action | Visibility | Gate |
|---|---|---|---|---|
| README.md | Gnozis | REWRITE | Public | product scope |
| CHANGELOG | split: Gnozis/Core/Research-Memory | SPLIT | Public/controlled | history ownership |
| CITATION | Gnozis | REWRITE | Public | product citation |
| CLAIMS.md | Research-Memory; approved subset to Gnozis | SPLIT | Controlled/Public subset | evidence |
| COMMERCIAL-LICENSE | Legal scope / Genesis + applicable public terms | REVIEW, DO NOT COPY | Controlled | legal |
| COMMERCIAL-LICENSE.md | Legal scope | REVIEW | Controlled | legal |
| CONTRIBUTING | each public repo | SPLIT/REWRITE | Public | repo-specific contribution policy |
| COPYRIGHT.md | legal master + repo notices | SPLIT/REWRITE | Controlled/Public notices | legal |
| DISCOVERY-POLICY | Gnozis | REWRITE | Public | public discovery |
| EVOLUTION.md | Core + Research-Memory + Gnozis | SPLIT/REWRITE | Mixed | canonical ownership |
| GNOZIS_MASTER_AUDIT.md | Research-Memory | MOVE | Controlled | provenance |
| LICENSE-RESEARCH | Research-Memory | REVIEW/REWRITE | Public/controlled | legal |
| LICENSE-RESEARCH.md | Research-Memory | REVIEW/REWRITE | Public/controlled | legal |
| PHILOSOPHY.md | Research-Memory | MOVE | Controlled/Public as approved | research |
| PROJECT_STATE.md | Research-Memory | MOVE | Controlled | historical state |
| RECOVERY_GAPS_2026-09-10.md | Research-Memory | MOVE | Controlled | historical audit |
| RESEARCH_SOURCES.md | Research-Memory | MOVE | Controlled/Public as approved | source provenance |
| ROADMAP.md | Gnozis + Core + Research-Memory + Genesis | SPLIT/REWRITE | Mixed | scope |
| STATE.md | Research-Memory/archive | MOVE/DEPRECATE | Controlled | avoid duplicate authority |
| TRADEMARKS | legal master + repo notices | SPLIT/REWRITE | Controlled/Public notices | legal |
| TRADEMARKS.md | legal master + repo notices | SPLIT/REWRITE | Controlled/Public notices | legal |
| AI_CONTEXT.md | Research-Memory | MOVE | Controlled | machine context |
| bot.py | Exchange | MOVE/REWRITE | Public only after security review | external boundary |
| .gitignore | each repo | REWRITE | Public | repo-specific |
| MIGRATION-MANIFEST-v1.md | source migration control | KEEP TEMPORARILY | Public/controlled | remove/archive after migration |

## Quarantine / no automatic publication

Any content discovered inside a root artifact that contains:
- credentials or secrets;
- proprietary algorithms;
- private datasets;
- private commercial strategy;
- unapproved commercial module implementation;
- legally ambiguous third-party material

must be QUARANTINE/PRIVATE until separately classified.

## Canonicality rule

No migrated repository may retain a second authoritative copy of:
- Core state semantics;
- Core transition/admission/selection/commit contract;
- canonical commercial implementation;
- canonical research-memory history.

References may remain; duplicate authority may not.

## Current unresolved gates

1. Legal wording/scope must be reviewed before final license publication.
2. CHANGELOG/EVOLUTION/ROADMAP require historical vs current split.
3. bot.py requires external-boundary security review.
4. Genesis has no automatic extraction path from the public repository.

## Exit condition

Root classification is implementation-ready when all legal gates are explicitly assigned and every split artifact has a canonical owner.
