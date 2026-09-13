from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping


Invariant = Callable[[Any], bool]


@dataclass(frozen=True)
class ProofObligation:
    """Minimal, explicit proof result for a proposed state transition.

    The proof layer does not generate candidates and does not select one.
    Callers provide the already-generated candidate pool and an invariant.
    """

    passed: bool
    invariant: bool
    viable: bool
    evidence: Mapping[str, Any]


def _strict_bool(value: object, *, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must return bool exactly.")
    return value


def _invariant(invariant: Invariant, candidate: Any) -> bool:
    return _strict_bool(invariant(candidate), name="Invariant")


def _viable(candidate: Any, candidates: Iterable[Any], invariant: Invariant) -> bool:
    """Depth-1 viability: a distinct invariant-valid continuation exists."""
    for continuation in candidates:
        if continuation == candidate:
            continue
        if _invariant(invariant, continuation):
            return True
    return False


def prove_transition(
    current: Any,
    candidate: Any,
    candidates: Iterable[Any],
    invariant: Invariant,
) -> ProofObligation:
    """Return a reproducible depth-1 proof for a proposed transition.

    `current` is included in the evidence so the proof describes the actual
    transition boundary, but viability is evaluated from the supplied pool.
    No generation, selection, or hidden state occurs here.
    """
    pool = tuple(candidates)
    invariant_ok = _invariant(invariant, candidate)
    viable_ok = invariant_ok and _viable(candidate, pool, invariant)
    evidence = {
        "candidate_count": len(pool),
        "has_distinct_continuation": viable_ok,
        "depth": 1,
    }
    return ProofObligation(
        passed=invariant_ok and viable_ok,
        invariant=invariant_ok,
        viable=viable_ok,
        evidence=evidence,
    )
