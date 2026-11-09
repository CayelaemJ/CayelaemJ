# CDC Replay Lab

A small, executable **Python + SQLite** portfolio project that demonstrates event replay, idempotency, source ordering, physical-delete tombstones and incremental analytical projection. Everything runs locally with synthetic account balances and the Python standard library.

## Try it

```bash
cd projects/cdc-replay-lab
python replay.py
python -m unittest discover -v
```

## Architecture

`Change` source event → `bronze_events` immutable event-id log → `silver_accounts` latest ordered state → `gold()` active-count and total snapshot.

- Identical event IDs can be replayed without duplicate effects.
- Reusing an event ID for different contents fails closed.
- An older source sequence is recorded in Bronze but cannot overwrite newer Silver state.
- DELETEs leave a tombstone, not a disappearing event history.
- A batch fails atomically on bad events.

## Boundaries

This is an educational **single-process demonstrator**, not a binlog reader, production CDC tool or source-to-dashboard SLA. It assumes a monotonically increasing sequence **per entity**, complete UPSERT images and one SQLite writer. A production implementation still needs source transaction ordering, checkpoint consistency, transport retries, access control, encryption, backfill, lag monitoring and operating procedures. No personal or production data is included.
