"""Deterministic, read-only analytics queries on a disposable SQLite database."""
from __future__ import annotations

import sqlite3
from datetime import date, timedelta


AGGREGATE_SQL = """SELECT COUNT(*), COALESCE(SUM(amount_cents), 0)
FROM orders
WHERE tenant_id = ? AND status = ? AND created_on >= ? AND created_on < ?"""


NON_SARGABLE_SQL = """SELECT COUNT(*), COALESCE(SUM(amount_cents), 0)
FROM orders
WHERE tenant_id = ? AND status = ? AND substr(created_on, 1, 7) = ?"""


def build_synthetic_store(rows: int = 2400) -> sqlite3.Connection:
    """Return an isolated in-memory store containing *fictional* transactions."""
    if not isinstance(rows, int) or isinstance(rows, bool) or rows < 1:
        raise ValueError("rows must be a positive integer")
    db = sqlite3.connect(":memory:")
    db.execute("""CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        status TEXT NOT NULL,
        created_on TEXT NOT NULL,
        amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0)
    )""")
    start = date(2026, 1, 1)
    db.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
        ((
            index,
            f"tenant-{(index % 6) + 1:02d}",
            "POSTED" if index % 5 else "DRAFT",
            (start + timedelta(days=(index * 7) % 100)).isoformat(),
            1000 + (index * 41) % 90000,
        )
        for index in range(1, rows + 1))
    )
    db.commit()
    return db


def plan(db: sqlite3.Connection, sql: str, params: tuple) -> list[str]:
    """Extract the query planner details without executing a write statement."""
    if not sql.lstrip().upper().startswith("SELECT "):
        raise ValueError("Only SELECT statements can be explained")
    return [row[3] for row in db.execute("EXPLAIN QUERY PLAN " + sql, params)]


def result(db: sqlite3.Connection, sql: str, params: tuple) -> tuple[int, int]:
    return db.execute(sql, params).fetchone()


def create_composite_index(db: sqlite3.Connection) -> None:
    db.execute("CREATE INDEX idx_orders_tenant_status_date ON orders(tenant_id, status, created_on)")


def demonstrate() -> dict:
    db = build_synthetic_store()
    try:
        params = ("tenant-02", "POSTED", "2026-02-01", "2026-03-01")
        before_result = result(db, AGGREGATE_SQL, params)
        before_plan = plan(db, AGGREGATE_SQL, params)
        create_composite_index(db)
        after_result = result(db, AGGREGATE_SQL, params)
        after_plan = plan(db, AGGREGATE_SQL, params)
        non_sargable_plan = plan(db, NON_SARGABLE_SQL, params[:2] + ("2026-02",))
        assert before_result == after_result
        return {
            "row_count": 2400,
            "result": {"orders": after_result[0], "sum_cents": after_result[1]},
            "without_index": before_plan,
            "with_index": after_plan,
            "function_on_date_column": non_sargable_plan,
        }
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(demonstrate(), indent=2))
