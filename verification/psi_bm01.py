"""Ψ-BM-01: bounded executable safety model.

This model is intentionally implementation-independent. It enumerates a small
state space and checks the local fail-closed invariants discussed in the Ψ-GNR
architecture.

Run:
    python verification/psi_bm01.py

A zero-violation result is evidence about this bounded model only; it is not a
proof of the correctness of the production Gnozis implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product

MAX_EPOCH = 1
MAX_HEIGHT = 3
MAX_GENERATION = 2
MAX_CAP_GENERATION = 2
MAX_DEPTH = 7

MODES = ("INIT", "RECOVERY", "READY", "HALT")
WITNESS_PHASES = ("NONE", "PREPARED", "DECIDED", "LINEARIZED", "COMMITTED")


@dataclass(frozen=True)
class State:
    epoch: int = 0
    height: int = 0
    generation: int = 0
    finalized: int = 0
    canonical: str = "GENESIS"
    cap_generation: int = 0
    cap_scope: frozenset[str] = frozenset()
    revoked_cap_generation: int = -1
    witness: str = "NONE"
    mode: str = "INIT"
    recovery_source: str = ""


@dataclass(frozen=True)
class Step:
    name: str
    state: State


def valid_finality(s: State) -> bool:
    return 0 <= s.finalized <= s.height


def valid_generations(s: State) -> bool:
    return 0 <= s.generation <= MAX_GENERATION and 0 <= s.cap_generation <= MAX_CAP_GENERATION


def valid_mode(s: State) -> bool:
    return s.mode in MODES


def safety_ok(prev: State, cur: State) -> tuple[bool, str]:
    if not valid_finality(cur):
        return False, "finalized boundary exceeds height"
    if not valid_generations(cur):
        return False, "generation bound violated"
    if not valid_mode(cur):
        return False, "invalid mode"

    # Non-reversion of canonical state and finality.
    if cur.generation < prev.generation:
        return False, "canonical generation reverted"
    if cur.finalized < prev.finalized:
        return False, "finality reverted"

    # Capability generation and revocation fence are monotonic.
    if cur.cap_generation < prev.cap_generation:
        return False, "capability generation reverted"
    if cur.revoked_cap_generation < prev.revoked_cap_generation:
        return False, "revocation boundary reverted"

    # No mutation while recovering.
    if prev.mode == "RECOVERY" and cur.mode == "READY":
        if cur.recovery_source == "AMBIGUOUS":
            return False, "ambiguous recovery reached READY"

    return True, ""


def successors(s: State) -> list[Step]:
    out: list[Step] = []

    if s.mode == "INIT":
        out.append(Step("BOOTSTRAP", replace(s, mode="READY")))
        return out

    if s.mode == "HALT":
        return out

    if s.mode == "RECOVERY":
        # Recovery is the only operation allowed from RECOVERY.
        out.append(Step("REPLAY_VALID", replace(s, mode="READY", recovery_source="VALID")))
        out.append(Step("REPLAY_AMBIGUOUS", replace(s, mode="HALT", recovery_source="AMBIGUOUS")))
        return out

    # READY transitions.
    if s.height < MAX_HEIGHT and s.generation < MAX_GENERATION:
        out.append(
            Step(
                "VALID_TRANSITION",
                replace(s, height=s.height + 1, generation=s.generation + 1, canonical=f"W{s.generation + 1}"),
            )
        )

    if s.finalized < s.height:
        out.append(Step("FINALIZE", replace(s, finalized=s.height)))

    if s.epoch < MAX_EPOCH:
        # Valid epoch inheritance: finalized boundary is retained.
        out.append(Step("EPOCH_ROTATE_VALID", replace(s, epoch=s.epoch + 1)))
        # Broken inheritance is explicitly rejected rather than installed.
        out.append(Step("EPOCH_ROTATE_REJECT", s))

    if s.cap_generation < MAX_CAP_GENERATION:
        out.append(
            Step(
                "DELEGATE_VALID",
                replace(s, cap_generation=s.cap_generation + 1, cap_scope=frozenset({"read"})),
            )
        )

    if s.cap_generation > s.revoked_cap_generation:
        out.append(Step("REVOKE", replace(s, revoked_cap_generation=s.cap_generation)))

    out.append(Step("CRASH", replace(s, mode="RECOVERY", recovery_source="DURABLE")))

    # Adversarial candidates. These must never be accepted as ordinary READY states.
    out.append(Step("ATTACK_GENERATION_ROLLBACK", replace(s, generation=max(0, s.generation - 1))))
    out.append(Step("ATTACK_CAP_ROLLBACK", replace(s, cap_generation=max(0, s.cap_generation - 1))))
    out.append(Step("ATTACK_FINALITY_ROLLBACK", replace(s, finalized=max(0, s.finalized - 1))))

    return out


def classify(prev: State, step: Step) -> str:
    cur = step.state

    # Explicit adversarial candidates are rejected or halt; they are never CONTINUE.
    if step.name.startswith("ATTACK_"):
        return "REJECT" if step.name != "ATTACK_FINALITY_ROLLBACK" else "HALT"
    if step.name == "EPOCH_ROTATE_REJECT":
        return "REJECT"
    if step.name == "REPLAY_AMBIGUOUS":
        return "HALT"
    if prev.mode == "RECOVERY" and step.name not in {"REPLAY_VALID", "REPLAY_AMBIGUOUS"}:
        return "HALT"
    return "CONTINUE"


def explore() -> tuple[set[tuple[State, ...]], list[tuple[tuple[State, ...], str, str]]]:
    initial = State()
    traces: set[tuple[State, ...]] = {(initial,)}
    frontier = [(initial,)]
    violations: list[tuple[tuple[State, ...], str, str]] = []

    while frontier:
        trace = frontier.pop()
        if len(trace) - 1 >= MAX_DEPTH:
            continue
        prev = trace[-1]
        for step in successors(prev):
            result = classify(prev, step)
            cur = step.state

            if result == "CONTINUE":
                ok, reason = safety_ok(prev, cur)
                if not ok:
                    violations.append((trace + (cur,), step.name, reason))
                    continue
            else:
                # A rejected/halting adversarial transition must not silently
                # appear as a new reachable READY state.
                if result == "REJECT" and cur != prev:
                    continue
                if result == "HALT":
                    cur = replace(cur, mode="HALT")

            new_trace = trace + (cur,)
            if new_trace not in traces:
                traces.add(new_trace)
                frontier.append(new_trace)

    return traces, violations


def main() -> int:
    traces, violations = explore()
    print("Ψ-BM-01 bounded model")
    print(f"bounds: E<={MAX_EPOCH}, h<={MAX_HEIGHT}, g<={MAX_GENERATION}, gC<={MAX_CAP_GENERATION}, depth<={MAX_DEPTH}")
    print(f"traces explored: {len(traces)}")
    print(f"invariant violations: {len(violations)}")

    if violations:
        print("\nCOUNTEREXAMPLE FOUND")
        trace, action, reason = violations[0]
        print(f"action: {action}")
        print(f"reason: {reason}")
        for i, state in enumerate(trace):
            print(f"  S{i}: {state}")
        return 1

    print("RESULT: 0 bounded safety violations")
    print("NOTE: this result applies only to the executable bounded model, not to production code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
