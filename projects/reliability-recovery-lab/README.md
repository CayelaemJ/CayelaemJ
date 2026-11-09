# OmniMaster Reliability & Recovery Lab
### A source-free teaching system for retries, background jobs and truthful status

This is the runnable companion to **Volume VII: Reliability Engineering and the Human Experience**.

[Read Volume VII](../../docs/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [All projects](../README.md) · [Public Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)

## Run

Python **3.12+** and the standard library only. No package install, network requests, API keys, financial records, accounts or persistent filesystem writes.

~~~bash
cd projects/reliability-recovery-lab
python cli.py
python -m unittest discover -v
~~~

The CLI produces JSON for two fictional tenants and a simulated clock:

- `tenant-beta`'s fictional job finishes on tick **0**.
- `tenant-alpha`'s job fails at ticks **0** and **2** with `source_unavailable`, then succeeds at tick **6**.
- The alpha retry delay is 2 ticks, then 4 ticks. Each successful effect is inserted **once**.
- The audit records each state transition. The final status is `DONE` for both synthetic jobs.

## Data flow

~~~mermaid
flowchart LR
    Q["Fictional submit"] --> VALID["Validate IDs and payload"]
    VALID --> DB["SQLite job row"]
    DB --> DUE{"Due now?"}
    DUE -->|"No"| WAIT["Wait on simulated clock"]
    DUE -->|"Yes"| EXEC{"Injected failure?"}
    EXEC -->|"Yes, attempts remain"| RETRY["Retry with bounded backoff"]
    EXEC -->|"Yes, limit reached"| DEAD["DEAD, operator decision"]
    EXEC -->|"No"| EFFECT["Local simulated effect, unique key"]
    EFFECT --> AUDIT["Atomic DONE and audit record"]
    RETRY --> DUE
~~~

## What each table teaches

| Table | Job | Invariant |
|---|---|---|
| `jobs` | Tracks requested tasks and attempts | One row per unique `job_id` |
| `effects` | Represents a **fictional local side effect** | One row per `effect_key`; conflicting reuse rejected |
| `audit` | Records state transitions and retry history | Errors, attempt numbers and simulated ticks available for review |

The `run_due()` method processes due jobs in one Python process. It uses a SQLite transaction for each job's state changes, effect and audit entry.

## Try breaking it

1. Submit the exact same job again. It should return `False` and not duplicate the row.
2. Reuse the job ID with changed payload. It should raise a conflict.
3. Set fault scripts for attempts 1, 2 and 3. The job should finish in `DEAD`, without an effect.
4. Requeue the dead job manually at a later simulated tick. It should execute from attempt 1 again and record `MANUAL_REQUEUE`.
5. Submit two jobs with the same effect key and identical data. Only one local effect is inserted.
6. Try the same effect key across tenants or with different payloads. The simulator rejects that collision.
7. Explain why a frontend should show **Queued** after a 202 acceptance rather than **Completed**.

## A crucial security distinction

The `jobs_for(tenant)`, `effects_for(tenant)` and `history_for(job_id,tenant)` methods take a tenant identifier. They illustrate **tenant filtering**, not authentication or authorisation. An untrusted caller must **never** choose arbitrary tenant IDs in a real API. A real backend derives allowed scope from verified identity and enforces permissions.

## What this proves, and what it does not

**Demonstrates:** deterministic local retries, bounded delays, dead-letter state, collision checks, atomic SQLite effect/state/audit writes, manual requeue, synthetic tenant-filtered queries and clear test outcomes.

**Does not prove:** distributed exactly-once delivery, concurrency safety, a real queue or CDC connector, authentication, durable process recovery, external email/payment idempotency, retry-after semantics, production observability, or business correctness for real datasets.

An external API call cannot be made atomic with your SQLite transaction simply by wrapping the local database writes. Real consumers require a designed outbox/inbox or source/sink checkpoint strategy, idempotency at the external target, failure injection across process boundaries, and tested recovery.

**Your exercise:** Write a one-page production upgrade plan with the missing guarantees and tests. If you cannot describe what happens when the worker crashes after performing the effect but before saving the result, you have not yet specified an end-to-end delivery guarantee.

[Start the Reliability textbook](../../docs/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md)
