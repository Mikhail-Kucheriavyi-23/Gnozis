"""Generate one reproducible benchmark artifact from the controlled protocol.

This is a deterministic fixture for validating the measurement pipeline. The
matched control is explicitly supplied and has the same relation count as the
initial topology; it is not yet a claim of a statistically sampled random
control.
"""
from __future__ import annotations

import json
from pathlib import Path

from research.controlled_benchmark import run_controlled_benchmark
from research.drosophila_principles import LIFState, Synapse

ARTIFACT = Path("research/artifacts/spt_benchmark.json")


def main() -> int:
    states = {"a": LIFState(), "b": LIFState(), "c": LIFState()}
    relations = (Synapse("a", "b", 0.5), Synapse("b", "a", 0.5))
    matched = (Synapse("a", "c", 0.5), Synapse("c", "a", 0.5))
    inputs = tuple({"a": 1.0} for _ in range(4))

    result = run_controlled_benchmark(
        states,
        relations,
        inputs=inputs,
        random_matched_relations=matched,
    )

    payload = {
        "baseline": [float(step.viability) for step in result.baseline],
        "random_matched": [float(step.viability) for step in result.random_matched],
        "plastic": [float(step.viability) for step in result.plastic],
        "initial_budget": len(relations),
        "random_budget": len(matched),
        "seed": 0,
        "control_type": "deterministic_matched_fixture",
        "input_steps": len(inputs),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
