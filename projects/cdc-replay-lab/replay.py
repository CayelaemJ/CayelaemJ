"""Small, dependency-free CDC event replay demonstrator (synthetic data only)."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Change:
    event_id: str
    entity_id: str
    sequence: int
    operation: str
    amount: str | None = None


class ReplayStore:
    """Bronze event log and latest-state Silver projection in one transaction."""

    def __init__(self, connection: sqlite3.Connection | None = None):
        self.db = connection or sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS bronze_events (
                event_id TEXT PRIMARY KEY,
                entity_id TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                operation TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS silver_accounts (
                entity_id TEXT PRIMARY KEY,
                sequence INTEGER NOT NULL,
                amount TEXT,
                is_deleted INTEGER NOT NULL CHECK (is_deleted IN (0, 1))
            );
        """)

    @staticmethod
    def _validate(event: Change) -> str | None:
        if not event.event_id.strip() or not event.entity_id.strip():
            raise ValueError("Event and entity IDs are required")
        if type(event.sequence) is not int or event.sequence < 1:
            raise ValueError("Source sequence must be a positive integer")
        if event.operation not in {"UPSERT", "DELETE"}:
            raise ValueError("Unsupported CDC operation")
        if event.operation == "DELETE":
            if event.amount is not None:
                raise ValueError("DELETE must not carry an amount")
            return None
        try:
            value = Decimal(str(event.amount))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("UPSERT needs a decimal amount") from None
        if not value.is_finite() or value < 0:
            raise ValueError("Amount must be finite and non-negative")
        return str(value)

    def apply_batch(self, events: list[Change]) -> dict[str, int]:
        """Apply all or none; duplicate IDs and old source sequences are harmless."""
        outcome = {"applied": 0, "duplicate": 0, "stale": 0}
        with self.db:
            for event in events:
                amount = self._validate(event)
                row = self.db.execute(
                    "SELECT entity_id, sequence, operation, payload FROM bronze_events WHERE event_id=?",
                    (event.event_id,),
                ).fetchone()
                payload = json.dumps({"amount": amount}, sort_keys=True)
                if row is not None:
                    if row != (event.entity_id, event.sequence, event.operation, payload):
                        raise ValueError("Event ID reused with different contents")
                    outcome["duplicate"] += 1
                    continue
                self.db.execute(
                    "INSERT INTO bronze_events VALUES (?, ?, ?, ?, ?)",
                    (event.event_id, event.entity_id, event.sequence, event.operation, payload),
                )
                latest = self.db.execute(
                    "SELECT sequence FROM silver_accounts WHERE entity_id=?", (event.entity_id,)
                ).fetchone()
                if latest is not None and event.sequence <= latest[0]:
                    outcome["stale"] += 1
                    continue
                self.db.execute(
                    """INSERT INTO silver_accounts VALUES (?, ?, ?, ?)
                       ON CONFLICT(entity_id) DO UPDATE SET
                         sequence=excluded.sequence, amount=excluded.amount,
                         is_deleted=excluded.is_deleted""",
                    (event.entity_id, event.sequence, amount, int(event.operation == "DELETE")),
                )
                outcome["applied"] += 1
        return outcome

    def state(self) -> list[dict]:
        rows = self.db.execute(
            "SELECT entity_id, sequence, amount, is_deleted FROM silver_accounts ORDER BY entity_id"
        ).fetchall()
        return [dict(entity_id=r[0], sequence=r[1], amount=r[2], deleted=bool(r[3])) for r in rows]

    def gold(self) -> dict:
        active = [r for r in self.state() if not r["deleted"]]
        return {"active_accounts": len(active),
                "total_amount": str(sum((Decimal(r["amount"]) for r in active), Decimal("0")))}


if __name__ == "__main__":
    demo = ReplayStore()
    demo.apply_batch([
        Change("evt-1", "sample-A", 1, "UPSERT", "120.50"),
        Change("evt-2", "sample-B", 1, "UPSERT", "40.00"),
        Change("evt-3", "sample-A", 2, "UPSERT", "125.25"),
        Change("evt-4", "sample-B", 2, "DELETE"),
    ])
    print(json.dumps({"silver": demo.state(), "gold": demo.gold()}, indent=2))
