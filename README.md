# GNOSIS

## Autopoietic Systems for Scientific Discovery & Intelligence

### Universal Computational Research Platform

**UROBOROS — Ψ-Core v33**

> A general computational architecture for studying autopoietic systems, modeling, reasoning, evolution, scientific research and discovery.

**Copyright © 2026 Mikhail Kucheriavyi. All rights reserved except where expressly granted by the applicable project license.**

**Public Research Release: 3 September 2026**

Research and qualifying non-commercial use is permitted under `LICENSE-RESEARCH.md`.

Commercial use requires a separate commercial license. See `COMMERCIAL-LICENSE.md`.

Project names including GNOSIS, UROBOROS and Ψ-Core are project identifiers and are not automatically licensed for unrestricted commercial branding. See `TRADEMARKS.md`.

---

## Overview

GNOSIS is a public research platform built around **UROBOROS — Ψ-Core v33**.

The repository contains a minimal computational core together with tests, examples, documentation and research materials intended to support reproducible investigation.

The current implementation provides fundamental computational primitives for:

* state representation;
* relations;
* deterministic state transitions;
* recursive execution;
* reproducible examples;
* automated testing.

The broader Ψ-Core architecture remains a subject of research and validation.

GNOSIS is therefore intentionally divided into two levels:

```text
Implemented Core
       ↓
Research Architecture
```

The implemented software should not be interpreted as proof that every theoretical component of Ψ-Core has been validated.

---

## Project Structure

```text
GNOSIS
│
├── core/
│   ├── __init__.py
│   ├── state.py
│   ├── relation.py
│   ├── engine.py
│   └── uroboros.py
│
├── examples/
│   └── basic.py
│
├── tests/
│   └── test_core.py
│
├── research/
│   └── README.md
│
└── .github/
    └── workflows/
        └── test.yml
```

### Conceptual layers

| Layer      | Role                                      |
| ---------- | ----------------------------------------- |
| GNOSIS     | Research platform                         |
| UROBOROS   | Recursive computational core              |
| Ψ-Core v33 | Public reference architecture             |
| Research   | Experimental and scientific investigation |
| Tests      | Verification of implemented behavior      |
| Examples   | Minimal executable demonstrations         |

The exact repository structure may evolve.

---

## Scientific Purpose

GNOSIS investigates whether a relatively compact computational architecture can provide useful primitives for studying:

* autopoietic systems;
* recursive systems;
* artificial intelligence;
* machine reasoning;
* scientific discovery;
* hypothesis generation;
* model construction;
* simulation;
* optimization;
* complex systems;
* autonomous computation.

A conceptual research cycle is:

```text
Represent
    ↓
Reason
    ↓
Explore
    ↓
Generate
    ↓
Test
    ↓
Select
    ↓
Evolve
    ↓
Repeat
```

This cycle is a research hypothesis and architectural direction, not a claim of established scientific fact.

---

## Core Research Principle

GNOSIS follows:

```text
Open Investigation
        +
Transparent Provenance
        +
Independent Validation
        +
Reproducible Computation
```

Scientific usefulness is evaluated through evidence rather than acceptance of project assumptions.

Researchers are encouraged to:

* reproduce results;
* identify weaknesses;
* construct counterexamples;
* test boundary conditions;
* publish negative results;
* compare competing architectures;
* propose alternative explanations;
* replace components;
* develop independent implementations.

---

## Scientific Status

GNOSIS is a **research platform**.

The software implementation, architectural hypotheses and research mechanisms are subject to independent examination.

Publication of the project does not establish that every hypothesis, mechanism or result is scientifically validated.

The project distinguishes:

```text
Implementation
      ↓
Observation
      ↓
Hypothesis
      ↓
Experimental Test
      ↓
Independent Validation
      ↓
Scientific Result
```

A computational output should not automatically be interpreted as a scientific fact, proof or validated discovery.

---

## Current Implementation

The current core provides four primary components:

### State

Immutable state representation used by the computational engine.

### Relation

Immutable representation of a relation between two entities.

### Engine

Deterministic state-transition mechanism supporting:

* single-step evolution;
* finite execution;
* trajectory generation.

### UROBOROS

A recursive computational wrapper combining state and engine execution.

The current implementation is intentionally small.

The purpose of this minimal core is to provide a stable computational substrate that can be tested and extended without unnecessarily increasing fundamental complexity.

---

## Reproducibility

Reproducibility is a primary development principle.

Research involving GNOSIS should identify, where practical:

* GNOSIS version;
* UROBOROS version;
* Ψ-Core version;
* Git commit;
* experiment configuration;
* relevant parameters;
* datasets or data sources;
* software dependencies;
* computational environment;
* random seeds where applicable.

Repository history provides a technical provenance record for corresponding source states.

---

## Reference Baseline

The public reference baseline is:

```text
GNOSIS
└── UROBOROS
    └── Ψ-Core v33
```

**Reference release:** 3 September 2026

The v33 baseline should remain identifiable and reproducible.

Experimental changes that materially alter the conceptual architecture should be explicitly identified as experimental or assigned a later version.

---

## Testing

Tests are an essential part of the project.

The repository currently includes automated core tests executed through GitHub Actions.

Testing may be expanded to include:

* unit tests;
* integration tests;
* regression tests;
* property-based tests;
* reproducibility tests;
* stress tests;
* benchmark tests;
* architectural consistency checks.

A passing software test establishes behavior covered by that test. It does not by itself establish the scientific validity of the underlying architecture.

---

## Examples

The repository contains minimal executable examples demonstrating the core API.

Examples are demonstrations of implementation behavior and should not automatically be interpreted as validated scientific models.

Researchers are encouraged to modify examples, construct alternative implementations and use them as starting points for independent experiments.

---

## Scientific Criticism

GNOSIS explicitly welcomes scientific criticism.

Researchers may attempt to:

* falsify assumptions;
* identify contradictions;
* construct counterexamples;
* demonstrate failure modes;
* reproduce negative results;
* compare competing models;
* challenge theoretical claims;
* identify limitations.

A result demonstrating a limitation or failure of GNOSIS is scientifically valuable.

The project does not require contributors to support its hypotheses.

---

## Independent Research

Researchers may conduct independent research using GNOSIS according to the applicable Research License.

Independent work may include:

* scientific papers;
* mathematical analyses;
* simulations;
* datasets;
* algorithms;
* alternative implementations;
* engineering designs;
* theoretical models;
* experimental results;
* competing architectures.

Independent research should accurately identify material use of GNOSIS where scientifically relevant.

Recommended attribution:

> This work was conducted using GNOSIS — UROBOROS Ψ-Core v33, developed by Mikhail Kucheriavyi.

---

## Discovery and Attribution

GNOSIS distinguishes between the underlying technology and new research results.

```text
GNOSIS Technology
        ≠
Every Result Produced With GNOSIS
```

Use of GNOSIS does not automatically transfer ownership of every independent scientific result to the project author.

Questions concerning:

* authorship;
* inventorship;
* patents;
* copyright;
* ownership;
* commercialization;

are governed by applicable law, agreements and actual contribution.

See `DISCOVERY-POLICY.md`.

---

## Intellectual Property

The project contains multiple forms of intellectual property and associated rights.

### Project

**GNOSIS**

### Core

**UROBOROS**

### Architecture

**Ψ-Core v33**

### Author

**Mikhail Kucheriavyi**

Original source code, documentation and other copyrightable project materials are protected to the extent provided by applicable law.

Copyright does not automatically provide exclusive ownership over abstract mathematical ideas, scientific facts, discoveries, methods or concepts where those subjects are not protected by copyright.

Different forms of intellectual property may be governed by different legal rules.

See:

* `COPYRIGHT.md`
* `TRADEMARKS.md`
* `DISCOVERY-POLICY.md`

---

## Licensing

GNOSIS separates research access from commercial authorization.

| Use                                     | Applicable status           |
| --------------------------------------- | --------------------------- |
| Source inspection                       | Research License            |
| Academic research                       | Research License            |
| Education                               | Research License            |
| Non-commercial experimentation          | Research License            |
| Independent research                    | Research License            |
| Non-commercial derivative research      | Research License            |
| Commercial software                     | Commercial License required |
| Commercial SaaS                         | Commercial License required |
| Commercial API                          | Commercial License required |
| Commercial cloud deployment             | Commercial License required |
| Enterprise commercial deployment        | Commercial License required |
| Commercial redistribution               | Commercial License required |
| Commercial product incorporating GNOSIS | Commercial License required |
| Unrestricted commercial branding        | Not automatically granted   |

See:

* `LICENSE-RESEARCH.md`
* `COMMERCIAL-LICENSE.md`
* `COPYRIGHT.md`
* `TRADEMARKS.md`
* `DISCOVERY-POLICY.md`
* `CONTRIBUTING.md`

### Fundamental Licensing Principle

```text
Public Source
      ≠
Unrestricted Commercial Permission
```

---

## Trademarks and Project Identity

Project identifiers include:

* **GNOSIS**
* **UROBOROS**
* **Ψ-Core**
* **Ψ-Core v33**

These names may be used descriptively to accurately identify the project and its technology.

Third-party implementations, forks and derivative projects should clearly distinguish themselves from official GNOSIS releases where necessary.

Use of project names does not automatically imply:

* endorsement;
* certification;
* sponsorship;
* partnership;
* authorization;
* scientific validation.

See `TRADEMARKS.md`.

---

## Contributions

Contributions are welcome from:

* researchers;
* developers;
* engineers;
* students;
* independent investigators;
* organizations.

Possible contributions include:

* code;
* tests;
* documentation;
* research;
* benchmarks;
* security reports;
* alternative implementations;
* reproducibility studies;
* scientific criticism.

Contributors should distinguish between:

```text
Bug Fix
Optimization
Research
Experiment
Architectural Change
```

Substantial architectural changes should not silently redefine Ψ-Core v33.

See `CONTRIBUTING.md`.

---

## Research Integrity

GNOSIS development follows basic principles of scientific integrity.

Contributors and researchers should:

* distinguish hypotheses from validated results;
* report methods accurately;
* preserve relevant negative results;
* avoid fabricated results;
* avoid manipulated benchmarks;
* identify material limitations;
* preserve provenance;
* provide reproducibility information where practical;
* give appropriate attribution.

---

## Security and Safety

GNOSIS is research software.

Independent validation is required before deployment in high-consequence environments.

Particular caution is required for applications involving:

* medical systems;
* critical infrastructure;
* industrial control;
* transportation;
* financial systems;
* autonomous physical systems;
* safety-critical machinery;
* high-consequence decision making.

The project does not provide automatic certification or regulatory approval for such applications.

---

## No Warranty

GNOSIS and UROBOROS are research technologies.

Except where expressly provided by a separate written agreement, the project is provided on an:

**"AS IS"**

basis.

No guarantee is made regarding:

* correctness;
* reliability;
* scientific validity;
* performance;
* security;
* commercial value;
* fitness for a particular purpose;
* regulatory compliance.

Users are responsible for independently evaluating the system for their intended use.

---

## Provenance

The public project record identifies:

```text
Project:
GNOSIS

Core:
UROBOROS

Reference Architecture:
Ψ-Core v33

Author:
Mikhail Kucheriavyi

Public Research Release:
3 September 2026
```

Repository commits, release tags and archived versions should be used when establishing the technical state of a particular release.

The public repository history is a provenance record. It is not represented as a substitute for formal patent filing, trademark registration, copyright registration, notarization or another legally recognized priority mechanism.

---

## Research-to-Commercial Transition

A project may progress through:

```text
Research
   ↓
Experiment
   ↓
Validation
   ↓
Prototype
   ↓
Pilot
   ↓
Commercial Deployment
```

The transition to commercial use is governed by the applicable commercial licensing requirements.

An independently developed discovery does not automatically eliminate licensing requirements applicable to GNOSIS technology incorporated into a commercial system.

See `COMMERCIAL-LICENSE.md`.

---

## Project Documents

The repository maintains the following principal project documents:

| File                    | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `README.md`             | Project overview and orientation             |
| `LICENSE-RESEARCH.md`   | Research-use permissions                     |
| `COMMERCIAL-LICENSE.md` | Commercial licensing framework               |
| `COPYRIGHT.md`          | Copyright and provenance                     |
| `TRADEMARKS.md`         | Project naming and trademark policy          |
| `DISCOVERY-POLICY.md`   | Discovery, attribution and commercialization |
| `CONTRIBUTING.md`       | Contribution and development rules           |

These documents should be interpreted together with the applicable license terms.

---

## Core Philosophy

GNOSIS follows a simple development principle:

```text
Minimum Necessary Complexity
+
Maximum Reproducibility
+
Maximum Testability
```

The objective is not maximum code volume.

The objective is maximum scientific and computational usefulness per unit of complexity.

When two implementations provide equivalent intended behavior, the simpler implementation is generally preferred when it improves inspection, testing and reproducibility.

---

## Vision

GNOSIS aims to provide a computational foundation for investigating:

* intelligence;
* autopoiesis;
* recursive systems;
* scientific discovery;
* autonomous computation;
* complex systems;
* modeling;
* reasoning;
* evolution;
* simulation.

The long-term research direction can be summarized as:

```text
Represent
    ↓
Reason
    ↓
Explore
    ↓
Generate
    ↓
Test
    ↓
Select
    ↓
Evolve
    ↓
Discover
```

**GNOSIS** — the platform.

**UROBOROS** — the recursive core.

**Ψ-Core v33** — the public reference architecture.

**Research** — the purpose.

**Evidence** — the criterion.

**Reproducibility** — the method.

---

## Final Principle

GNOSIS is intended to remain open to scientific investigation while preserving clear provenance and separating research access from commercial authorization.

The project welcomes researchers who seek to:

**prove it right, prove it wrong, improve it, replace it, reproduce it, or develop competing approaches.**

Scientific usefulness is more important than preserving assumptions.
