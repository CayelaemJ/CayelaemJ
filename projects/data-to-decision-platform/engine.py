"""A compact fictional source-event -> SQLite state -> tenant metrics pipeline.

Educational only: no networking, external databases, authentication, CDC connector,
or real client data. Every operation runs against a disposable in-memory database.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
import sqlite3
from typing import Iterable


_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,40}$")


@dataclass(frozen=True)
class Event:
    event_id: str
    position: int
    tenant: str
    account: str
    version: int
    operation: str
    amount_cents: int
    occurred_at: str


def validate(event: Event) -> None:
    if not isinstance(event, Event):
        raise ValueError("events must be Event instances")
    for value in (event.event_id, event.tenant, event.account):
        if not isinstance(value, str) or not _ID.fullmatch(value):
            raise ValueError("event, tenant and account IDs must be safe identifiers")
    if type(event.position) is not int or event.position < 1:
        raise ValueError("source position must be a positive integer")
    if type(event.version) is not int or event.version < 1:
        raise ValueError("account version must be a positive integer")
    if event.operation not in ("UPSERT", "DELETE"):
        raise ValueError("operation must be UPSERT or DELETE")
    if type(event.amount_cents) is not int or event.amount_cents < 0:
        raise ValueError("amount must be nonnegative integer cents")
    if event.operation == "DELETE" and event.amount_cents != 0:
        raise ValueError("DELETE must not carry a balance")
    if not isinstance(event.occurred_at, str):
        raise ValueError("event timestamp must be text")
    try:
        timestamp = datetime.fromisoformat(event.occurred_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid event timestamp") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("event timestamp must include a timezone")


class Pipeline:
    """Transactional, replay-safe *simulation* of current-state projections."""

    def __init__(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE bronze_events(
            event_id TEXT PRIMARY KEY,
            source_position INTEGER NOT NULL UNIQUE,
            tenant TEXT NOT NULL,
            account TEXT NOT NULL,
            version INTEGER NOT NULL,
            operation TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            occurred_at TEXT NOT NULL
        );
        CREATE TABLE silver_accounts(
            tenant TEXT NOT NULL,
            account TEXT NOT NULL,
            version INTEGER NOT NULL,
            amount_cents INTEGER NOT NULL,
            is_deleted INTEGER NOT NULL CHECK (is_deleted IN (0,1)),
            source_position INTEGER NOT NULL,
            PRIMARY KEY(tenant, account)
        );
        CREATE INDEX idx_silver_active_tenant
            ON silver_accounts(tenant, is_deleted);
        """)
        self.db.commit()

    def __enter__(self) -> "Pipeline":
        return self

    def __exit__(self, *_: object) -> None:
        self.db.close()

    @staticmethod
    def fields(event: Event) -> tuple:
        return (
            event.event_id, event.position, event.tenant, event.account,
            event.version, event.operation, event.amount_cents, event.occurred_at,
        )

    def apply_batch(self, events: Iterable[Event]) -> dict[str, int]:
        """Atomic batch; duplicates are harmless and conflicting IDs fail closed."""
        stats = {"accepted": 0, "duplicates": 0, "stale": 0, "projected": 0}
        with self.db:
            for event in events:
                validate(event)
                existing = self.db.execute(
                    "SELECT event_id, source_position, tenant, account, version, "
                    "operation, amount_cents, occurred_at "
                    "FROM bronze_events WHERE event_id = ?",
                    (event.event_id,),
                ).fetchone()
                if existing is not None:
                    if existing != self.fields(event):
                        raise ValueError("event ID reused with different content")
                    stats["duplicates"] += 1
                    continue

                current = self.db.execute(
                    "SELECT version FROM silver_accounts WHERE tenant = ? AND account = ?",
                    (event.tenant, event.account),
                ).fetchone()
                if current is not None and current[0] == event.version:
                    raise ValueError("conflicting events share an account version")

                # UNIQUE source_position rejects two different events at one position.
                self.db.execute(
                    "INSERT INTO bronze_events VALUES (?,?,?,?,?,?,?,?)",
                    self.fields(event),
                )
                stats["accepted"] += 1
                if current is not None and current[0] > event.version:
                    stats["stale"] += 1
                    continue
                self.db.execute(
                    "INSERT INTO silver_accounts "
                    "(tenant,account,version,amount_cents,is_deleted,source_position)"
                    " VALUES (?,?,?,?,?,?) ON CONFLICT(tenant,account) DO UPDATE SET "
                    "version=excluded.version, amount_cents=excluded.amount_cents, "
                    "is_deleted=excluded.is_deleted, source_position=excluded.source_position",
                    (
                        event.tenant, event.account, event.version,
                        event.amount_cents, int(event.operation == "DELETE"), event.position,
                    ),
                )
                stats["projected"] += 1
        return stats

    def metrics_for(self, tenant: str) -> dict[str, object]:
        """Trusted-scope *example*. No auth is provided: this is NOT an API."""
        if not isinstance(tenant, str) or not _ID.fullmatch(tenant):
            raise ValueError("invalid tenant")
        count, total = self.db.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount_cents),0) FROM silver_accounts "
            "WHERE tenant = ? AND is_deleted = 0",
            (tenant,),
        ).fetchone()
        return {"tenant": tenant, "active_accounts": count, "balance_cents": total}

    def events(self) -> list[Event]:
        return [
            Event(*row) for row in self.db.execute(
                "SELECT event_id,source_position,tenant,account,version,"
                "operation,amount_cents,occurred_at "
                "FROM bronze_events ORDER BY source_position"
            )
        ]

    def snapshot(self) -> list[tuple]:
        return list(self.db.execute(
            "SELECT tenant,account,version,amount_cents,is_deleted,source_position "
            "FROM silver_accounts ORDER BY tenant,account"
        ))

    def reconciles(self) -> bool:
        """Rebuild from Bronze and compare projection, without changing the original."""
        with Pipeline() as rebuilt:
            rebuilt.apply_batch(self.events())
            return rebuilt.snapshot() == self.snapshot()


def sample_events() -> tuple[Event, ...]:
    moment = "2026-11-09T10:00:00+00:00"
    records = (
        ("evt-01", 1, "fictional-alpha", "acct-a", 1, "UPSERT", 12000),
        ("evt-02", 2, "fictional-alpha", "acct-b", 1, "UPSERT", 8000),
        ("evt-03", 3, "fictional-beta", "acct-a", 1, "UPSERT", 30000),
        ("evt-04", 4, "fictional-alpha", "acct-a", 2, "UPSERT", 14000),
        ("evt-05", 5, "fictional-alpha", "acct-b", 2, "DELETE", 0),
        ("evt-06", 6, "fictional-beta", "acct-c", 1, "UPSERT", 5000),
        ("evt-07", 7, "fictional-alpha", "acct-d", 1, "UPSERT", 9000),
        ("evt-08", 8, "fictional-beta", "acct-a", 2, "UPSERT", 32000),
    )
    return tuple(Event(*row, moment) for row in records)
