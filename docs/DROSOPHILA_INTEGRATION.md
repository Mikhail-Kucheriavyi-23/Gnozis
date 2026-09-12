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

No Drosophila connectome dataset, Brian2 model, or original source implementation is placed in the GNOSIS core.

## Why this boundary exists

GNOSIS defines the canonical object as Ψ=(X,R). The Drosophila project is therefore treated as a source of experimentally useful biological principles, not as a replacement architecture. Keeping the adapter outside `core/` prevents the biological simulator from becoming an implicit second state model or an external selector.

## First hypothesis

The useful transfer is not “simulate a fly”. It is:

`local recurrent dynamics + structural plasticity -> candidate endogenous reorganization of R`

The current adapter is deliberately small and dependency-free. It is a research instrument, not evidence that autopoiesis or intelligence has been achieved.

## Required next experiments

- damage one relation and test whether a viable recurrent organization can be regenerated;
- repeat the damage and compare the response with the first trial;
- test whether previous structural changes alter future adaptation;
- test whether novel viable relation structures can arise without an external selector;
- only after positive evidence consider any change to canonical `core/`.

## Attribution

The reviewed source is `philshiu/Drosophila_brain_model`, copyright Philip Shiu and Nico Spiller, licensed under the MIT License. The GNOSIS research adapter is an independent reimplementation of high-level mechanisms and does not copy the source code or datasets.
