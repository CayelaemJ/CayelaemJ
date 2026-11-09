# Build With Me 05 | Break it on purpose and prove the boundaries

[← Metrics to users](04_FROM_METRICS_TO_USERS.md) · [Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Next: Beyond the demo →](06_BEYOND_THE_DEMO.md)

A system that works on the happy path can still be unusable in practice. My method is to **find the failure that changes the user's outcome** and design an experiment that reproduces it.

The [test suite](../../projects/data-to-decision-platform/test_engine.py) contains twenty explicit regression cases. They demonstrate expected behaviour of this fictional Python project, not production security or distributed recovery.

## Failure matrix

| Failure | What might go wrong | What to observe |
|---|---|---|
| Event delivered twice | Duplicate current state or inflated totals | State and Gold totals unchanged |
| Event ID reused with different payload | Silent corruption | Rejection and unchanged committed state |
| Same source position assigned twice | Stream identity ambiguity | Database rejects the collision |
| Same version assigned to conflicting events | Non-deterministic latest state | Fail closed; do not guess the winner |
| Old version arrives late | Historical update overwrites current truth | Store event but preserve later projection |
| Delete arrives | Ghost account remains in aggregate | Tombstone retained, aggregate excludes it |
| Later row is invalid | Earlier row commits from a failed declared batch | Entire batch rolls back |
| Projection manually corrupted | Green process with incorrect state | Independent replay detects mismatch |
| Caller supplies malicious-looking tenant string | Unsafe query interpolation | Input validation and parameterisation |
| Timestamp lacks timezone | Business order becomes ambiguous | Reject at contract boundary |

## How to run the tests

~~~bash
cd projects/data-to-decision-platform
python -m unittest discover -v
python cli.py failure
~~~

The CLI produces `all_or_nothing`, `event_log_unchanged` and `reconciled` flags. Inspect the source rather than trusting flags without understanding how they are computed.

## The test that proves transactions

A good batch includes **a valid update followed by a deliberately invalid update**. If the implementation processes and commits rows one by one, it could leave half the batch accepted.

The demonstration encloses all writes inside one SQLite transaction. A later exception rolls back the earlier uncommitted writes.

**A real distributed source-to-sink system needs more:** the source checkpoint must not advance if the destination commit fails. That boundary doesn't exist in this toy example.

## The test that proves the event identity contract

Replay a previously accepted event ID with the **same payload**: it should do nothing.

Replay the same ID with a **different amount**: it should fail.

If you don't make that distinction, deduplication can silently hide corruption.

## The test that proves business version precedence

Apply account version 2, then a valid but late arrival of version 1 using a new event ID and source position.

The late event should appear in Bronze history but should not replace the newer Silver state. Now try two different events both claiming version 2. The code should reject the conflict rather than picking an arbitrary winner.

## Your deliberate failure exercise

1. Run the complete test suite.
2. Temporarily remove the code path that recognises duplicate event IDs.
3. Run the duplicate test again and observe a failure.
4. Restore the code.
5. Change the Gold filter to include tombstones.
6. Run the aggregate test, observe failure, then restore.
7. Write a journal entry: what invariant did each defect violate?

**Never commit the intentionally broken version as a claimed working solution.**

## A better explanation than “all tests green”

A strong statement is: “At this commit, the synthetic suite verified unique event IDs, replay, conflict rejection, rollback, tombstones, tenant-separated state and projection reconstruction against its own in-memory event history. It did not test external CDC, authentication, durable recovery, distributed consumers or live deployment.”

That is the level of precision I aim for in real engineering releases.

[← Chapter 04](04_FROM_METRICS_TO_USERS.md) · [Next: Beyond the demo →](06_BEYOND_THE_DEMO.md)
