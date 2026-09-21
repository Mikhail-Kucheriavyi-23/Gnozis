# Gnozis Archive

## Role

Gnozis Archive is the machine-readable development memory and evidence base for Gnozis.

It is not the current Gnozis Core, not an alternative implementation, and not an authority source for Core mutation.

## Authority boundary

```
Archive → retrieve / inform / provide provenance
Archive -X→ direct Core mutation or authorization
```

Any influence on Gnozis Core must pass through the explicit engineering admission path:

```
Archive record
→ scope/evidence review
→ engineering consequence
→ requirement
→ bounded task
→ implementation
→ test/CI
→ audit
→ acceptance
```

## Record identity

Every canonical archive record has a permanent unique ID. IDs are never reused.

Record content may be superseded, but historical identity and provenance are preserved.

## Canonical record classes

- R — research
- C — claim
- E — evidence
- X — counterexample
- D — decision
- A — audit
- T — transition

The schema is defined in `archive/schema/record.schema.json`.

## Historical artifacts

Historical source files, implementations, commits and other artifacts may be retained for provenance. They are evidence sources/artifacts, not current Core authority.

## Current Core

The current executable and verified system is maintained separately in the Gnozis Core repository.

## Integrity rule

Archive records must distinguish:

```
stored ≠ canonical
canonical ≠ verified
verified ≠ accepted
```

A record must never claim a stronger evidence state than its recorded evidence supports.
