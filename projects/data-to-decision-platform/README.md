# Data-to-Decision Platform | A full-stack *thinking* lab
### Volume V's runnable capstone: source events → trusted state → business metrics

**This is the smallest complete teaching example of how I reason across data engineering, database design, analytics, testing and application boundaries.**

[Volume V textbook](../../docs/OMNIMASTER_BUILD_WITH_ME.md) · [Project index](../README.md) · [GitHub profile](../../README.md)

## Run locally

You only need Python **3.12+** and its standard library. No accounts, pip packages, cloud services, keys, network connections or actual business data.

~~~bash
cd projects/data-to-decision-platform
python cli.py demo
python cli.py failure
python -m unittest discover -v
~~~

### What happens

1. Eight **fictional** account events from two synthetic tenants enter an in-memory SQLite Bronze log.
2. Each event has a stable ID, unique source position, tenant, account and integer cents value.
3. A Silver projection keeps the latest logical version per tenant/account, including a DELETE tombstone.
4. A Gold query returns authorised-scope **illustrative** aggregates when passed a tenant identifier.
5. Reapplying the same exact events makes no changes. Conflicting event IDs or account versions fail closed.
6. Every batch runs in a database transaction; if a later event is invalid, the earlier writes in that batch roll back.
7. Independent replay from the Bronze log can detect a corrupted current-state projection.

**Expected synthetic totals:** `fictional-alpha` has 2 active accounts and 23,000 cents, `fictional-beta` has 2 active accounts and 37,000 cents.

The CLI `failure` demonstration attempts a valid event followed by an invalid negative amount. Both must roll back.

## Read the implementation

| File | Role |
|---|---|
| [engine.py](engine.py) | Event contract, validation, transactional ingestion, projection, Gold aggregate and independent replay |
| [cli.py](cli.py) | Run the fictional scenario and deliberate rollback example |
| [test_engine.py](test_engine.py) | Regression cases for event identity, replay, versioning, deletes, tenant data separation, corruption and transaction atomicity |

## Diagram

~~~mermaid
flowchart LR
    SRC["Eight synthetic events"] --> V["Schema and business validation"]
    V --> LOG["SQLite Bronze event log"]
    LOG --> PROJ["Silver account state"]
    PROJ --> GOLD["Gold tenant metrics"]
    LOG --> REPLAY["Independent replay & reconciliation"]
    REPLAY --> PROJ
~~~

## What this does **not** prove

- **Not real CDC:** there is no MySQL binlog, Kafka or production source connector; `position` and versions are fictional.
- **Not authenticated multitenancy:** `metrics_for(tenant)` is a parameterised SQL teaching method, **not an HTTP endpoint or server authorisation layer**. A real app must derive tenant scope from a verified identity. It would be unsafe to expose this method directly to untrusted callers.
- **Not durable state:** SQLite is `:memory:`; closing the process discards everything. Real consumers need backup, process recovery, source checkpoints and concurrency decisions.
- **Not arbitrary financial accounting:** cents are integer to avoid float rounding, but the projection is not a ledger, regulated accounting engine or banking platform.
- **Not distributed delivery guarantees:** exactly-once semantics, multiple consumers, late-event business resolution and source transaction atomicity need dedicated design.
- **No real data:** all identifiers and dates are fake; the code doesn't access external services or user files.

The constraints are part of the lesson, not fine print. A code sample should teach what it cannot do as clearly as what it does.

## Study extensions

- Change one event's version and explain why the batch should be rejected.
- Add a source correction for an old business date and keep distinct occurred/processed times.
- Introduce a source checkpoint and deliberately crash before commit.
- Add a **separate authenticated application boundary** before exposing any tenant metrics over HTTP.
- Move from in-memory to a disposable file-based DB, then write restore and schema migration tests.
- Write a performance experiment over 100,000 fictional records and inspect the query plan.

[Continue the worked lessons](../../docs/build-with-me/01_SOURCE_AND_CONTRACT.md) · [30-day expedition](../../docs/THIRTY_DAY_ENGINEERING_EXPEDITION.md)
