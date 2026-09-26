# Genesis Layer Matrix

This is the architectural classification boundary for the private Genesis repository.

| Layer | Responsibility | Public? | Trusted Core? |
|---|---|---:|---:|
| Core | immutable state, transition, verification, digest, persistence integrity, recovery, provenance, audit primitives | selected API | YES |
| Genesis Runtime | evolution orchestration, reflection, diagnostics, governed self-improvement, module-factory execution | NO | NO |
| Product | workspace, task/context continuity, user/project APIs, permissions, connectors | selected interfaces | NO |
| Knowledge | machine-readable research/evidence collections and retrieval interfaces | configurable | NO |
| Commercial | proposals, opportunity lifecycle, contracts, confidential collaboration | configurable/private | NO |
| Research | experiments, hypotheses, analysis and evidence production | configurable | NO |

## Classification rules

### KEEP IN Genesis
- proprietary orchestration;
- private module-factory logic;
- sensitive governance/evaluation;
- private diagnostics and evolution mechanisms;
- confidential commercial implementation;
- internal security controls.

### MOVE/EXPOSE THROUGH INTERFACES
- context continuity contracts;
- evidence/provenance schemas that users need to exchange;
- capability declarations;
- project/task interfaces;
- reusable knowledge connectors;
- public product APIs.

These must be exposed as stable contracts, not by exposing Genesis internals.

### MOVE TO Research-Memory
- machine-readable research records;
- mathematical, physical, historical and other domain knowledge;
- evidence packages intended for reuse;
- research provenance that is publishable.

### MOVE TO Gnozis PRODUCT
- user-facing workspace behavior;
- project connection;
- seamless context restoration;
- public documentation/examples;
- public discovery surfaces.

### MOVE TO COMMERCIAL BOUNDARY
- opportunity/proposal records;
- commercializable outputs;
- contract workflows;
- confidential partner/project workspaces.

## Critical rule

Genesis must not become a second hidden Core. If a function requires trusted state semantics, it calls the Core contract. Genesis may propose, orchestrate, evaluate and produce modules, but cannot silently bypass Core verification or persistence boundaries.

## Migration method

Do not move whole directories by name. Classify each module by responsibility, dependency direction, data sensitivity, and required trust level. Then migrate only after tests and provenance are preserved.
