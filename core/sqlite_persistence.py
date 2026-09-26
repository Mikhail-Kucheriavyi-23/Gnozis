"""SQLite durable history store with transactional crash-injection boundaries."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Callable

from .commit_contract import CommitResult
from .history import AppendOnlyHistory, TransitionRecord

FailureInjector = Callable[[str], None]


class SQLiteHistoryStore:
    """Persist accepted TransitionRecord values atomically in SQLite."""

    def __init__(self, path: str | Path, *, failure_injector: FailureInjector | None = None):
        self.path = str(path)
        self.failure_injector = failure_injector
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transition_history (
                    sequence INTEGER PRIMARY KEY,
                    previous_hash TEXT NOT NULL,
                    state_hash TEXT NOT NULL,
                    kernel_version TEXT NOT NULL,
                    candidate_hash TEXT NOT NULL,
                    admitted INTEGER NOT NULL CHECK (admitted = 1),
                    evidence_hash TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _fail(self, point: str) -> None:
        if self.failure_injector is not None:
            self.failure_injector(point)

    def load(self) -> AppendOnlyHistory:
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                """
                SELECT sequence, previous_hash, state_hash, kernel_version,
                       candidate_hash, admitted, evidence_hash
                FROM transition_history
                ORDER BY sequence
                """
            ).fetchall()

        history = AppendOnlyHistory()
        for row in rows:
            record = TransitionRecord(
                sequence=row[0],
                previous_hash=row[1],
                state_hash=row[2],
                kernel_version=row[3],
                candidate_hash=row[4],
                admitted=bool(row[5]),
                evidence_hash=row[6],
            )
            history = history.append(record)
        return history

    def commit_once(
        self,
        record: TransitionRecord,
        current,
        next_value,
    ) -> CommitResult:
        """Atomically append one record, preserving idempotence across restart."""
        existing = self.load()
        if existing.records:
            head = existing.head
            if record.sequence < head.sequence:
                raise ValueError("commit sequence is stale")
            if record.sequence == head.sequence:
                if record.state_hash == head.state_hash:
                    return CommitResult(current, existing, False)
                raise ValueError("commit conflicts with existing head")
        elif record.sequence != 0:
            raise ValueError("genesis commit must have sequence zero")

        if existing.head is not None and record.previous_hash != existing.head.state_hash:
            raise ValueError("history chain is broken")

        self._fail("before_transaction")
        with sqlite3.connect(self.path) as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                self._fail("before_insert")
                conn.execute(
                    """
                    INSERT INTO transition_history (
                        sequence, previous_hash, state_hash, kernel_version,
                        candidate_hash, admitted, evidence_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.sequence,
                        record.previous_hash,
                        record.state_hash,
                        record.kernel_version,
                        record.candidate_hash,
                        int(record.admitted),
                        record.evidence_hash,
                    ),
                )
                self._fail("after_insert_before_commit")
                conn.commit()
            except Exception:
                conn.rollback()
                raise

        # This point models a process failure after durable commit but before
        # the caller publishes next_value. Recovery must reload the DB truth.
        self._fail("after_commit")
        durable = self.load()
        return CommitResult(next_value, durable, True)
