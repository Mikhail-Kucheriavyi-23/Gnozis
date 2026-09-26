# Core Contracts

## Purpose

These contracts define the minimum boundary that every higher layer must use when interacting with Gnozis-Core.

## State

A trusted state has an explicit state_id, canonical representation, digest, version and provenance reference.

## Transition

A transition is an explicit candidate operation from one trusted state to another. It carries input identity and evidence. No implicit clock, global selector, hidden model call or external repository is authoritative.

## Context

Context is explicit data: identity reference, project reference, session/task context, selected knowledge/evidence references, permissions, version and provenance. Context can be restored without exposing Core internals.

## Evidence

Evidence records what was observed, tested, verified and committed. Persistence is not itself proof of correctness.

## External update

Core may emit a governed update request for a downstream repository or service. The downstream result is recorded as an external artifact/evidence item; it does not become Core authority automatically.

## Authority

Only the Core verification/commit path can change trusted state.
