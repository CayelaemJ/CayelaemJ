"""OmniMaster Reliability Lab: deterministic SQLite retry and recovery simulation.

All state and effects are local and disposable. No requests, notifications,
secrets, production queues or external side effects are performed.
"""
from __future__ import annotations

import json
import re
import sqlite3
from typing import Mapping


ID = re.compile(r"^[a-z][a-z0-9_-]{1,55}$")
MAX_ATTEMPTS = 3
BASE_DELAY = 2
MAX_DELAY = 8


def identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase safe identifier")
    return value


def clock(value: int) -> int:
    if type(value) is not int or value < 0:
        raise ValueError("time must be a nonnegative integer simulated tick")
    return value


def backoff(attempt: int) -> int:
    if type(attempt) is not int or attempt < 1:
        raise ValueError("attempt must be a positive integer")
    return min(MAX_DELAY, BASE_DELAY * 2 ** min(attempt - 1, 4))


class ReliabilityLab:
    """A single-process teaching lab. SQLite guarantees do not cross services."""

    def __init__(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE jobs (
                job_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                effect_key TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('PENDING','RETRY','DONE','DEAD')),
                attempts INTEGER NOT NULL DEFAULT 0,
                next_due INTEGER NOT NULL DEFAULT 0,
                last_error TEXT
            );
            CREATE TABLE effects (
                effect_key TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                producer_job TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE audit (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                tenant TEXT NOT NULL,
                action TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                at_tick INTEGER NOT NULL,
                detail TEXT NOT NULL
            );
            CREATE INDEX idx_jobs_due ON jobs(status, next_due, job_id);
        """)
        self.db.commit()

    def __enter__(self) -> "ReliabilityLab":
        return self

    def __exit__(self, *_: object) -> None:
        self.db.close()

    def _audit(self, job_id: str, tenant: str, action: str,
               attempt: int, at_tick: int, detail: str) -> None:
        self.db.execute(
            "INSERT INTO audit(job_id,tenant,action,attempt,at_tick,detail) "
            "VALUES (?,?,?,?,?,?)",
            (job_id, tenant, action, attempt, at_tick, detail),
        )

    def submit(self, job_id: str, tenant: str, effect_key: str,
               payload: Mapping[str, str], now: int = 0) -> bool:
        """Return False on identical replay; reject same job ID, different input."""
        identifier(job_id, "job ID")
        identifier(tenant, "tenant")
        identifier(effect_key, "effect key")
        clock(now)
        if not isinstance(payload, dict) or set(payload) != {"message"} or \
                not isinstance(payload["message"], str) or not payload["message"].strip() \
                or len(payload["message"]) > 160:
            raise ValueError("payload must contain one short, non-empty message")
        data = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        with self.db:
            existing = self.db.execute(
                "SELECT tenant,effect_key,payload FROM jobs WHERE job_id=?",
                (job_id,),
            ).fetchone()
            if existing:
                if existing != (tenant, effect_key, data):
                    raise ValueError("job ID reused with different input")
                return False
            self.db.execute(
                "INSERT INTO jobs (job_id,tenant,effect_key,payload,status,attempts,next_due)"
                " VALUES (?,?,?,?,?,?,?)",
                (job_id, tenant, effect_key, data, "PENDING", 0, now),
            )
            self._audit(job_id, tenant, "SUBMITTED", 0, now, "queued")
        return True

    def run_due(self, now: int, faults: Mapping[tuple[str, int], str] | None = None,
                limit: int = 100) -> list[dict[str, object]]:
        """Process only due jobs; faults map (job_id, attempt) to safe error code."""
        clock(now)
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("limit must be an integer from 1 to 1000")
        faults = {} if faults is None else faults
        if not isinstance(faults, Mapping):
            raise ValueError("fault script must be a mapping")
        for key, error in faults.items():
            if not isinstance(key, tuple) or len(key) != 2:
                raise ValueError("fault key must be (job_id, attempt)")
            identifier(key[0], "fault job ID")
            if type(key[1]) is not int or key[1] < 1:
                raise ValueError("fault attempt must be positive")
            identifier(error, "fault code")

        due = self.db.execute(
            "SELECT job_id,tenant,effect_key,payload,attempts "
            "FROM jobs WHERE status IN ('PENDING','RETRY') AND next_due <= ? "
            "ORDER BY next_due,job_id LIMIT ?",
            (now, limit),
        ).fetchall()
        results = []
        for job_id, tenant, effect_key, payload, previous in due:
            attempt = previous + 1
            error = faults.get((job_id, attempt))
            with self.db:
                if error:
                    state = "DEAD" if attempt >= MAX_ATTEMPTS else "RETRY"
                    next_due = now if state == "DEAD" else now + backoff(attempt)
                    self.db.execute(
                        "UPDATE jobs SET status=?,attempts=?,next_due=?,last_error=? "
                        "WHERE job_id=?",
                        (state, attempt, next_due, error, job_id),
                    )
                    self._audit(job_id, tenant, state, attempt, now, error)
                    results.append({"job": job_id, "state": state, "attempt": attempt,
                                    "next_due": None if state == "DEAD" else next_due})
                    continue

                already = self.db.execute(
                    "SELECT tenant,producer_job,payload FROM effects WHERE effect_key=?",
                    (effect_key,),
                ).fetchone()
                if already and (already[0] != tenant or already[2] != payload):
                    # Reusing an effect key for different data or another tenant is unsafe.
                    raise ValueError("effect key collision across distinct outputs")
                if already is None:
                    self.db.execute(
                        "INSERT INTO effects VALUES (?,?,?,?)",
                        (effect_key, tenant, job_id, payload),
                    )
                action = "DONE_DUPLICATE_SUPPRESSED" if already else "DONE"
                self.db.execute(
                    "UPDATE jobs SET status='DONE',attempts=?,next_due=?,last_error=NULL "
                    "WHERE job_id=?",
                    (attempt, now, job_id),
                )
                self._audit(job_id, tenant, action, attempt, now,
                            "local effect was present" if already else "local effect committed")
                results.append({"job": job_id, "state": "DONE", "attempt": attempt,
                                "deduplicated_effect": bool(already)})
        return results

    def requeue_dead(self, job_id: str, tenant: str, now: int) -> None:
        identifier(job_id, "job ID")
        identifier(tenant, "tenant")
        clock(now)
        with self.db:
            row = self.db.execute(
                "SELECT status FROM jobs WHERE job_id=? AND tenant=?",
                (job_id, tenant),
            ).fetchone()
            if row is None or row[0] != "DEAD":
                raise ValueError("only a dead job in the requested tenant can be requeued")
            self.db.execute(
                "UPDATE jobs SET status='RETRY',attempts=0,next_due=?,last_error=NULL "
                "WHERE job_id=? AND tenant=?",
                (now, job_id, tenant),
            )
            self._audit(job_id, tenant, "MANUAL_REQUEUE", 0, now, "operator recovery simulation")

    def jobs_for(self, tenant: str) -> list[dict[str, object]]:
        identifier(tenant, "tenant")
        rows = self.db.execute(
            "SELECT job_id,status,attempts,next_due,last_error "
            "FROM jobs WHERE tenant=? ORDER BY job_id", (tenant,),
        )
        return [
            {"job": j, "status": s, "attempts": a, "next_due": d, "last_error": e}
            for j, s, a, d, e in rows
        ]

    def effects_for(self, tenant: str) -> list[str]:
        identifier(tenant, "tenant")
        return [row[0] for row in self.db.execute(
            "SELECT effect_key FROM effects WHERE tenant=? ORDER BY effect_key", (tenant,),
        )]

    def history_for(self, job_id: str, tenant: str) -> list[tuple[str, int, int]]:
        identifier(job_id, "job ID")
        identifier(tenant, "tenant")
        return list(self.db.execute(
            "SELECT action,attempt,at_tick FROM audit "
            "WHERE job_id=? AND tenant=? ORDER BY seq", (job_id, tenant),
        ))


def demonstration() -> dict[str, object]:
    with ReliabilityLab() as lab:
        lab.submit("job-alpha", "tenant-alpha", "effect-alpha", {"message": "fictional report"}, 0)
        lab.submit("job-beta", "tenant-beta", "effect-beta", {"message": "fictional notice"}, 0)
        faults = {
            ("job-alpha", 1): "source_unavailable",
            ("job-alpha", 2): "source_unavailable",
        }
        timeline = [
            {"at": tick, "outcomes": lab.run_due(tick, faults)}
            for tick in (0, 1, 2, 5, 6)
        ]
        return {
            "synthetic_only": True,
            "timeline": timeline,
            "alpha": lab.jobs_for("tenant-alpha"),
            "beta": lab.jobs_for("tenant-beta"),
            "alpha_effects": lab.effects_for("tenant-alpha"),
            "beta_effects": lab.effects_for("tenant-beta"),
            "alpha_audit": lab.history_for("job-alpha", "tenant-alpha"),
        }
