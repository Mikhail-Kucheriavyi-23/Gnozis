"""Produce a reproducible SPT benchmark artifact from benchmark_runner.

No scientific numbers are embedded here. The artifact is generated only by
executing the existing benchmark implementation.
"""
from __future__ import annotations

import json
from pathlib import Path

from research.benchmark_runner import run_benchmark

ARTIFACT = Path("research/artifacts/spt_benchmark.json")


def main() -> int:
    # Keep the experiment configuration explicit and deterministic.
    result = run_benchmark(seed=0)
    payload = {
        "baseline": [float(step.baseline) for step in result],
        "random_matched": [float(step.random_matched) for step in result],
        "plastic": [float(step.plastic) for step in result],
        "random_budget": int(result[0].random_budget),
        "initial_budget": int(result[0].initial_budget),
        "seed": 0,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
