# Reliability Chapter 03 | Dead letters, evidence and recovery

[← Safe retries](02_RETRIES_AND_IDEMPOTENCY.md) · [Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Next: Reliable UX →](04_STATUS_UX_AND_OPERATIONS.md)

## When automatic retries must stop

A system that retries forever can turn one bad event into an operational incident. It consumes resources, floods logs, pressures the dependency and leaves users waiting for something that will never happen.

The **dead-letter state** separates automatic processing from deliberate human review.

In this synthetic lab, `MAX_ATTEMPTS = 3`. A third failed attempt sets the status to `DEAD`, records `last_error` and an audit transition, and does not insert any local effect.

## A responsible recovery workflow

~~~mermaid
flowchart TD
    FAIL["Attempt fails"] --> N{"Attempt limit reached?"}
    N -->|"No"| RETRY["Schedule safe retry"]
    N -->|"Yes"| DEAD["DEAD: needs operator review"]
    DEAD --> CHECK["Inspect cause and external effects"]
    CHECK --> DECIDE{"Safe to replay?"}
    DECIDE -->|"Yes"| RECOVER["Requeue with audit record"]
    DECIDE -->|"No"| RESOLVE["Resolve by documented alternative"]
    RECOVER --> TEST["Verify outcome and reconcile"]
~~~

The lab's `requeue_dead(job_id,tenant,now)` method allows a dead fictional job to be requeued, resetting the attempt count and adding a `MANUAL_REQUEUE` entry.

It rejects attempts to requeue a job in the wrong tenant, one that is pending or one already completed.

## Where the user interface matters

An operator needs more than a generic `Failed` label. Show the safe error category, last attempt, how many attempts ran, whether any effect might already have occurred, whether another attempt is automatic, and the appropriate next action.

A real product may need an incident ID, business impact, escalation level, permission-based requeue and a peer approval for consequential actions.

## Practice

Using a disposable Python session:

~~~python
from reliability import ReliabilityLab

with ReliabilityLab() as lab:
    lab.submit("job-demo", "tenant-demo", "effect-demo", {"message": "fictional only"})
    faults = {("job-demo", n): "source_unavailable" for n in (1, 2, 3)}
    for tick in (0, 2, 6):
        lab.run_due(tick, faults)

    assert lab.jobs_for("tenant-demo")[0]["status"] == "DEAD"
    assert lab.effects_for("tenant-demo") == []
    lab.requeue_dead("job-demo", "tenant-demo", 20)
    lab.run_due(20)
    assert lab.jobs_for("tenant-demo")[0]["status"] == "DONE"
~~~

## A cautious technical note

The SQLite database here is **in-memory and disposable**. Its history is an audit *demonstration*, not a durable production audit trail. It does not implement real operational approvals, external effect reconciliation or incident recovery.

For real systems, document retention, immutable history requirements, notification/alert routing and the conditions under which an item is safe to requeue.

## Review questions

1. What should a system do with a permanently malformed record?
2. How do you distinguish a temporary dependency failure from a business-rule violation?
3. What evidence do you require before a human presses Requeue?
4. How can you tell whether an external effect occurred before a crash?
5. When should an item be marked Resolved rather than attempted again?

**Pass criterion:** you can write a safe operator playbook with a reason for every manual action.

[Next: Make failures understandable →](04_STATUS_UX_AND_OPERATIONS.md)
