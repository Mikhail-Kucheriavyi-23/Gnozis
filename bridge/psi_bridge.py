"""Minimal fail-closed Ψ terminal bridge.

This module is a contract-level implementation of the Ψ authority boundary.
It deliberately does not implement a consensus algorithm or real cryptographic
signature verification. Those capabilities are injected as verifiers.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import json
from typing import Callable, Iterable, Mapping, Optional


class WitnessStatus(str, Enum):
    PREPARED = "PREPARED"
    DECIDED = "DECIDED"
    LINEARIZED = "LINEARIZED"
    COMMITTED = "COMMITTED"


class PsiHalt(RuntimeError):
    """Raised when durable evidence contains a safety conflict."""


@dataclass(frozen=True)
class CanonicalPointer:
    epoch: int
    generation: int
    height: int
    state_hash: str
    finality_height: int = 0
    finality_hash: str = ""


@dataclass(frozen=True)
class JPsiWitness:
    old: CanonicalPointer
    new: CanonicalPointer
    gamma_finality: str
    omega: str
    token: str
    status: WitnessStatus

    @property
    def old_generation(self) -> int:
        return self.old.generation

    @property
    def new_generation(self) -> int:
        return self.new.generation


def _digest(pointer: CanonicalPointer) -> str:
    body = {
        "epoch": pointer.epoch,
        "generation": pointer.generation,
        "height": pointer.height,
        "state_hash": pointer.state_hash,
        "finality_height": pointer.finality_height,
        "finality_hash": pointer.finality_hash,
    }
    raw = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


class GnosisPsiBridge:
    """Generation-fenced authority projection with deterministic recovery."""

    def __init__(
        self,
        canonical: CanonicalPointer,
        *,
        gamma_verifier: Optional[Callable[[JPsiWitness], bool]] = None,
        omega_verifier: Optional[Callable[[JPsiWitness], bool]] = None,
        finality_verifier: Optional[Callable[[JPsiWitness], bool]] = None,
    ) -> None:
        self.canonical = canonical
        self.recovery_active = False
        self._gamma_verifier = gamma_verifier or (lambda _: True)
        self._omega_verifier = omega_verifier or (lambda _: True)
        self._finality_verifier = finality_verifier or (lambda _: True)

    @staticmethod
    def _finality_compatible(old: CanonicalPointer, new: CanonicalPointer) -> bool:
        if new.finality_height < old.finality_height:
            return False
        if new.finality_height == old.finality_height:
            return new.finality_hash == old.finality_hash
        return True

    def validate_witness(self, witness: JPsiWitness) -> bool:
        old = witness.old
        new = witness.new
        if witness.new_generation != witness.old_generation + 1:
            return False
        if new.epoch < old.epoch:
            return False
        if new.height < old.height:
            return False
        if old.epoch == new.epoch and new.height < old.height:
            return False
        if not self._finality_compatible(old, new):
            return False
        if not self._gamma_verifier(witness):
            return False
        if not self._omega_verifier(witness):
            return False
        if not self._finality_verifier(witness):
            return False
        return True

    def _halt(self, reason: str) -> None:
        raise PsiHalt(reason)

    def install(self, pointer: CanonicalPointer) -> str:
        current = self.canonical
        if pointer.generation < current.generation:
            self._halt("generation rollback")
        if pointer.generation == current.generation:
            if pointer != current:
                self._halt("conflicting authority state")
            return "NOOP"
        if pointer.generation != current.generation + 1:
            self._halt("generation gap")
        self.canonical = pointer
        return "APPLY"

    def replay(self, witnesses: Iterable[JPsiWitness]) -> CanonicalPointer:
        self.recovery_active = True
        try:
            ordered = list(witnesses)
            decisions: dict[int, JPsiWitness] = {}
            for witness in ordered:
                if witness.status == WitnessStatus.PREPARED:
                    continue
                if not self.validate_witness(witness):
                    self._halt("invalid durable witness")
                key = witness.old_generation
                previous = decisions.get(key)
                if previous is not None and previous.new != witness.new:
                    self._halt("conflicting durable witnesses")
                decisions[key] = witness

            progress = True
            while progress:
                progress = False
                candidate = decisions.get(self.canonical.generation)
                if candidate is not None:
                    self.install(candidate.new)
                    progress = True

            return self.canonical
        finally:
            self.recovery_active = False

    def ready_to_transact(self) -> bool:
        return not self.recovery_active

    def transition(self, new: CanonicalPointer, *, gamma_finality: str, omega: str, token: str) -> JPsiWitness:
        if not self.ready_to_transact():
            self._halt("recovery in progress")
        old = self.canonical
        witness = JPsiWitness(
            old=old,
            new=new,
            gamma_finality=gamma_finality,
            omega=omega,
            token=token,
            status=WitnessStatus.PREPARED,
        )
        if not self.validate_witness(replace(witness, status=WitnessStatus.DECIDED)):
            self._halt("transition evidence rejected")
        return replace(witness, status=WitnessStatus.DECIDED)

    @staticmethod
    def authority(pointer: CanonicalPointer, state_hash: str) -> bool:
        return pointer.state_hash == state_hash

    @staticmethod
    def state_digest(pointer: CanonicalPointer) -> str:
        return _digest(pointer)
