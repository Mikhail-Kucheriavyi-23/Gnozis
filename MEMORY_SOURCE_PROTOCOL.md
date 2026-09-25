# Gnozis Memory Source Protocol

The Gnozis ecosystem uses a common protocol for connecting domain knowledge repositories to the private Kernel.

## Lifecycle

```
discover → register → authenticate → sync → validate
→ candidate/quarantine → evaluate → verify
→ accept/reject → optional incorporation
```

## Core rule

A Git repository is a versioned knowledge source, not trusted Kernel state.

Every connected source is identified by a stable source ID, owner, repository revision, content digest, schema version and provenance.

## Permissions

The protocol supports bounded capabilities such as:

- READ
- ANNOTATE
- PROPOSE
- PUBLISH

Deletion and history rewriting are not granted by default.

## Verification

New revisions can be quarantined until identity, integrity, schema, provenance and policy checks succeed.

Evidence classes remain distinct: evidence, observation, model, hypothesis, conjecture, interpretation, unresolved question and counterexample.

## Kernel boundary

```
Memory Repository
      ↓
Candidate
      ↓
Kernel evaluation
      ↓
Verified evidence
      ↓
Authorized transition
      ↓
Kernel state
```

A repository cannot directly mutate the Kernel.

## Reproducibility

Meaningful memory consumption records the source revision and content digest so that the exact input can be reconstructed.

The same protocol can serve mathematics, physics, philosophy, engineering, biology and future knowledge domains.
