"""Reproducible entry point for the first SPT benchmark run."""
from __future__ import annotations

import json
from pathlib import Path

from research.spt_acceptance import evaluate_spt


def main() -> int:
    """Run the acceptance layer on recorded benchmark series.

    The benchmark runner remains responsible for generating the three series.
    This entry point intentionally keeps the experiment deterministic and does
    not alter core state or tune the acceptance criterion.
    """
    # Placeholder until the benchmark runner exposes a persisted run artifact.
    # Refuse to manufacture scientific data.
    artifact = Path("research/artifacts/spt_benchmark.json")
    if not artifact.exists():
        raise SystemExit(
            "No benchmark artifact found; run the benchmark first. "
            "Scientific SPT results must never be fabricated."
        )

    data = json.loads(artifact.read_text(encoding="utf-8"))
    result = evaluate_spt(
        data["baseline"],
        data["random_matched"],
        data["plastic"],
        random_budget=int(data["random_budget"]),
        initial_budget=int(data["initial_budget"]),
    )
    print(json.dumps(result.__dict__, indent=2, sort_keys=True))
    print(json.dumps({"plastic_over_random": result.plastic_over_random, "accepted": result.accepted}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
