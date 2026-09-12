# Drosophila → GNOSIS research integration

## Status

RESEARCH ADAPTER — not part of the canonical Ψ core.

## Source reviewed

`philshiu/Drosophila_brain_model` is a Python/Brian2 computational model of the adult Drosophila brain based on connectome data. Its README describes leaky integrate-and-fire dynamics, synaptic connections, activation and silencing experiments, and parallel trial execution. The source repository is MIT licensed.

## What was transferred

Only mechanism-level ideas were reimplemented independently in `research/drosophila_principles.py`:

1. Local leaky activity with threshold/reset.
2. Recurrent propagation through weighted relations.
3. Local activity-dependent relation strengthening/weakening.
4. Structural decay and explicit relation extinction (`R -> ∅`).
5. A research-only candidate for local relation creation between co-active nodes.

No Drosophila connectome dataset, Brian2 model, or original source implementation is placed in the GNOSIS core.

## Audit finding — 2026-09-12

The adapter is useful as an experimental scaffold, but it does **not yet demonstrate endogenous autopoiesis, structural memory, or intelligence**.

The current topology generator creates a relation only when two nodes are already marked active. Therefore it changes `R`, but it does not yet demonstrate that the system generated a new functional organization from its own evolving state. In particular, the current experiment does not establish viability preservation or recovery after damage.

The repeated-damage harness retains the structural result between trials, but its local activity input is supplied as a fixed mapping. Consequently, it is a valid structural-memory *test harness*, not yet evidence of structural memory.

## Architectural decision

Keep all Drosophila-derived mechanisms outside `core/`. Do not merge them into canonical Ψ until experiments show a property that cannot be explained by a fixed rule or externally supplied state.

## Next required experiment

Build a closed experimental loop in which:

`Ψ=(X,R)` → activity → relation change → next `X,R` → viability test → repeat.

The experiment must measure whether a damaged system can produce a **new viable topology** without being told the target topology. The viability criterion must itself be explicit and auditable, but the repair topology must not be prescribed.

Only after this experiment passes should the mechanism be considered for promotion from `research/` into the canonical architecture.

## Attribution

The reviewed source is `philshiu/Drosophila_brain_model`, copyright Philip Shiu and Nico Spiller, licensed under the MIT License. The GNOSIS research adapter is an independent reimplementation of high-level mechanisms and does not copy the source code or datasets.
