# Reliability Chapter 01 | A job is a contract

[← Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Next: Retry safely →](02_RETRIES_AND_IDEMPOTENCY.md)

## The distinction that saves support tickets

When a person starts an operation, **receiving a request is not the same as finishing the work**. The backend may validate and enqueue the task while an independent worker does the actual processing later.

For a frontend, this distinction changes every status label and every promise made to a user.

## Draw the state machine first

| State | What it means in the teaching lab | What the interface may truthfully say |
|---|---|---|
| `PENDING` | Accepted, waiting for its first due attempt | "Queued for processing" |
| `RETRY` | Previous attempt failed; new attempt scheduled | "We're retrying. No success confirmed yet." |
| `DONE` | Local simulated effect, job update and audit committed | "Finished in the teaching simulator" |
| `DEAD` | Automatic attempt limit reached | "We couldn't complete the task. Review is needed." |

Real systems may need more states: `RUNNING`, `CANCELLED`, `PARTIAL`, `UNKNOWN`, `WAITING_FOR_APPROVAL`. A state machine should model the actual business guarantees rather than copy a fashionable queue vocabulary.

## See it in code

Open [reliability.py](../../projects/reliability-recovery-lab/reliability.py) and inspect the `jobs` table. The columns `status`, `attempts`, `next_due` and `last_error` make the decision to retry or stop observable.

~~~bash
cd projects/reliability-recovery-lab
python cli.py
~~~

The demonstration has two fictional tenants. Beta succeeds immediately. Alpha fails twice before succeeding. The events are deterministic and make no network requests.

## A common frontend mistake

The API returns `202 Accepted`. A UI immediately displays a permanent green **Completed** badge.

That is a usability defect and a correctness defect: the backend only accepted work; completion remains unknown.

The safer flow is:

~~~text
Submit task
  -> 202 Accepted, operation ID
  -> Show "Queued"
  -> Poll/subscribe to an authorised status endpoint
  -> Show "Processing", "Retrying", "Needs review" or "Done"
  -> Provide an appropriate next action
~~~

The teaching lab does not implement HTTP. You would need a verified session, tenant-derived scope, and a status endpoint before exposing these records.

## Practical task

Write down the exact allowed transitions: PENDING → RETRY, RETRY → DONE, RETRY → DEAD, DEAD → manually requeued. Then identify which transitions must be forbidden, such as marking a dead job as done without a new attempt.

## Review checklist

- Is every status name linked to an actual backend condition?
- Can the frontend display uncertainty rather than invent completion?
- Is a user's tenant derived from authenticated identity, not a query parameter?
- Can operations staff distinguish a permanent failure from a temporary delay?
- Does a retry change the status and preserve the previous error?

**Pass criterion:** a non-technical person can correctly interpret every displayed state and know when to retry, wait or seek help.

[Next: Retry safely →](02_RETRIES_AND_IDEMPOTENCY.md)
