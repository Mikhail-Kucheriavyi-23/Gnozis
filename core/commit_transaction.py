"""Crash-boundary state machine for the in-memory canonical commit contract."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .commit_contract import CommitResult, commit_once
from .history import AppendOnlyHistory, TransitionRecord


class CommitPhase(str, Enum):
    PREPARE = "prepare"
    APPEND = "append"
    PUBLISH = "publish"


@dataclass(frozen=True)
class CommitTransaction:
    history: AppendOnlyHistory
    record: TransitionRecord
    current: object
    next_value: object

    def prepare(self) -> "CommitTransaction":
        if self.record.sequence != (self.history.head.sequence + 1 if self.history.head else 0):
            raise ValueError("commit transaction sequence is not next.")
        if self.history.head is not None and self.record.previous_hash != self.history.head.state_hash:
            raise ValueError("commit transaction predecessor is not current head.")
        return self

    def append(self) -> AppendOnlyHistory:
        return self.history.append(self.record)

    def publish(self, appended: AppendOnlyHistory) -> CommitResult[object]:
        if appended.head != self.record:
            raise ValueError("published history does not contain prepared record.")
        return CommitResult(self.next_value, appended, True)


def commit_transaction(
    history: AppendOnlyHistory,
    record: TransitionRecord,
    current: object,
    next_value: object,
) -> CommitTransaction:
    tx = CommitTransaction(history, record, current, next_value)
    return tx.prepare()
