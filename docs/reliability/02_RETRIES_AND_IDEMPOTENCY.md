# Reliability Chapter 02 | Retry without causing the problem twice

[← Job contracts](01_JOBS_AND_STATE.md) · [Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Next: Dead letters →](03_DEAD_LETTERS_AND_RECONCILIATION.md)

## The uncomfortable truth about retries

A network timeout might mean an action did not happen, **or** that the action happened and its response was lost. Retrying blindly can duplicate work, notifications, imports or payments.

This matters in the full-stack workflow because the browser only sees the outcome it received, not necessarily the server's actual state.

## Why idempotency is useful

**Idempotency** means repeating the same logical operation doesn't create additional unintended effects. In the teaching lab, the job has a stable `job_id` and an `effect_key`.

- Re-submitting the same job ID with identical data is a harmless replay.
- Reusing the same job ID with different data fails closed.
- Multiple jobs using the same effect key and **same** tenant/payload produce a single local effect.
- Reusing an effect key with different payload or across tenants is rejected.

The code demonstrates these guarantees in **one local SQLite database**. It does not provide exactly-once delivery to an email, payment gateway or remote data warehouse.

## Bounded backoff

Run the example:

~~~bash
cd projects/reliability-recovery-lab
python cli.py
~~~

The simulated retry schedule uses `min(8, 2 × 2^(attempt−1))` ticks. The first failure waits two ticks; the second waits four; the cap is eight. Automatic processing stops after three failures.

| Attempt | At simulated tick | Outcome | Next action |
|---:|---:|---|---|
| 1 | 0 | Source unavailable | Retry at tick 2 |
| 2 | 2 | Source unavailable | Retry at tick 6 |
| 3 | 6 | Successful local effect | Commit DONE and audit |

This is **deterministic** educational backoff without jitter. Real systems should evaluate jitter, rate limits, source retry-after instructions, bounded queue pressure and whether an error is transient at all.

## Why the database transaction matters

In `run_due()`, the local effect row, job state and audit entry are changed together inside one SQLite transaction. If those local writes fail, the database can roll them back.

But imagine a real external service accepted a request before SQLite saved the result. The external effect **cannot be undone** by a local database rollback. You need a delivery contract that accounts for this, often involving an outbox/inbox, external idempotency key and reconciliation.

## Exercise: duplicate work

1. Create two fictional jobs with the same effect key, tenant and payload.
2. Run due work. Confirm only one local effect row exists.
3. Change one payload but reuse the key. Confirm the simulator rejects it.
4. Write a three-sentence explanation of what would be different if the effect were a real email or payment.

## Test the negative path

Read [test_reliability.py](../../projects/reliability-recovery-lab/test_reliability.py). The suite checks duplicate suppression, conflicting key reuse, retry timing and absence of unintended local effects.

**Pass criterion:** you can explain the distinction between **at-least-once delivery**, **idempotent processing** and a true external exactly-once guarantee without treating them as synonyms.

[Next: Dead letters and recovery →](03_DEAD_LETTERS_AND_RECONCILIATION.md)
