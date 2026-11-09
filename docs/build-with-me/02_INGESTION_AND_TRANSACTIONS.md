# Build With Me 02 | Ingest, replay, and fail atomically

[← Source contract](01_SOURCE_AND_CONTRACT.md) · [Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Next: State projection →](03_PROJECTIONS_AND_GRAIN.md)

## A successful batch needs a definition

A common data engineering failure is treating “the process finished” as evidence that every change reached the destination. I look for **durable progress, no unintended duplication, and a recoverable failure state**.

The [Pipeline.apply_batch()](../../projects/data-to-decision-platform/engine.py) example uses SQLite transactions and two tables: a source-event history and the latest-account projection.

## What happens to one event

~~~mermaid
flowchart TD
    E["Input event"] --> V{"Contract valid?"}
    V -->|"No"| RB["Raise error and roll back batch"]
    V -->|"Yes"| ID{"Event ID already seen?"}
    ID -->|"Identical"| DUP["Count duplicate; no state change"]
    ID -->|"Conflicting"| RB
    ID -->|"New"| BR["Insert Bronze event"]
    BR --> VER{"Account version"}
    VER -->|"Older"| ST["Record late event, keep newer projection"]
    VER -->|"Equal conflicting"| RB
    VER -->|"Newer"| UP["Upsert Silver state or tombstone"]
    ST --> COM["Commit entire valid batch"]
    UP --> COM
    DUP --> COM
~~~

The transaction is a toy demonstration using one in-memory SQLite connection. It is **not an end-to-end exactly-once guarantee for an external source**.

## Test 1. Idempotent replay

~~~bash
python cli.py demo
~~~

The CLI inserts eight events, then replays them. On replay, all eight should be recognised as exact duplicates, and the active-account totals should remain unchanged.

**Why this matters:** a consumer restart often causes at-least-once delivery. Correct applications must either tolerate safe replay or explicitly detect duplicates.

## Test 2. Conflicting identity

Change the amount of a previously processed event but keep its `event_id`. The engine should reject it, rather than silently treating it as the old event.

**Why:** if an identifier is reused for a different payload, deduplication has become data corruption.

## Test 3. All-or-nothing batch failure

~~~bash
python cli.py failure
~~~

The CLI deliberately sends a valid update followed by an invalid negative balance. The transaction rolls back the valid update too. The demonstration reports whether the source-event log and state remained unchanged.

**Why:** partial acceptance inside one declared atomic batch is hard to reason about unless explicitly designed.

## Test 4. Source positions

Two different event IDs with the same source position are rejected by a uniqueness constraint. This example assumes unique positions; a real source may identify events using a composite transaction ID, row index and offset.

## What this does not solve

Real capture/processing systems must coordinate reading from a remote source, destination commit and checkpoint acknowledgement. They need crash testing, source retention awareness, backpressure, bounded batches, concurrency rules and operations monitoring.

The [Fixer synthetic CDC review](https://github.com/CayelaemJ/NewChanges/issues/241) illustrates why a successful local replay experiment does not replace a real source-adapter test.

## Your exercise

Create an event with a fresh ID but the **same account version** as an existing event. It should fail closed. Then create an older version with a new source position: it should be recorded as historical arrival without overwriting the newer current state.

### Completion test

You can describe the difference between *duplicate event ID*, *same-version conflict*, *stale business update* and *source-position collision*, and demonstrate the expected transaction behaviour.

[← Chapter 01](01_SOURCE_AND_CONTRACT.md) · [Next: State projection →](03_PROJECTIONS_AND_GRAIN.md)
