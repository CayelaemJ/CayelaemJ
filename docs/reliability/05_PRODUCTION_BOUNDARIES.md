# Reliability Chapter 05 | From a local retry toy to real operations

[← Status UX](04_STATUS_UX_AND_OPERATIONS.md) · [Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Back to the Academy](../OMNIMASTER_ACADEMY.md)

## Don't confuse deterministic tests with distributed guarantees

The runnable lab is valuable because you can inspect every decision and reproduce every failure. That is not the same as proving a production system will recover from worker crashes, network partitions, source replays or downstream outages.

Here is the gap a responsible engineer should make explicit.

| Dimension | Local teaching lab | Production design requirement |
|---|---|---|
| Storage | In-memory SQLite | Durable storage, backups, HA and restore rehearsal |
| Work scheduling | Simulated integer clock | Real-time scheduling, visibility timeout and clock skew |
| Worker concurrency | One process | Multiple workers, claim/lease semantics and bounded parallelism |
| Delivery semantics | Deterministic local effect | Real source acknowledgements and idempotent external effects |
| Identity | Tenant parameter only | Authenticated actor, operation permission and server-derived tenant |
| Observability | Local audit table | Structured logs, metrics, alerts, tracing, retention and owner |
| Requeue | Direct method call | Operator authentication, approval, audit and duplicate-effect reconciliation |
| Traffic | A handful of fictional jobs | Load and saturation testing, capacity budgets and backpressure |
| Failure recovery | Scripted temporary failures | Process crash, timeout, partial write, external outage and rollback |
| Release | Local tests | Staging, CI, canary/gradual rollout and rollback plan |

## The failure window that matters most

Imagine an API call to send a message succeeds. The worker crashes before its local database records that outcome.

On restart, the job is still pending. A blind retry might send the message twice. **Local SQL transactions cannot roll back an already-committed external HTTP side effect.**

Possible controls include stable external idempotency keys, durable outbox/inbox records, reconciliation from provider receipts and state machines that preserve unknown outcomes. None is a universal magic fix; they must fit the target service's semantics.

## A safe engineering progression

**Stage 1. Correct local state:** source contracts, idempotency tests, bounded retries and visible failures.

**Stage 2. Durable persistence:** use a disposable database file or container, test restart, restore, schema migration and corruption detection.

**Stage 3. Real worker coordination:** introduce claims/leases and concurrent consumers in a local test environment. Test a worker that loses its lease midway through work.

**Stage 4. External synthetic integration:** use a mock or disposable downstream service. Inject timeouts both before and after the service commits.

**Stage 5. Security and tenant isolation:** enforce verified identity at HTTP boundaries, roles, tenant membership, least privilege and audit trails; test tampered identifiers.

**Stage 6. Operational proof:** implement dashboards, error budgets, alerts, a dead-letter response playbook, release gates and rollback.

## Release review questions

- Did the destination effect actually happen, or only local state update?
- What evidence survives a crash between the two operations?
- Can a duplicate source event produce a second real-world effect?
- Can workers concurrently claim the same job?
- Can a caller inspect or requeue another tenant's job?
- What happens during an hour-long downstream outage?
- Which states can be safely retried and which need human approval?
- Can a deploy be reverted without losing acknowledged jobs?
- Does the UI distinguish accepted, processing, confirmed and unknown?

## Your capstone assignment

Design a **fictional scheduled reporting system**. It processes a CSV of synthetic metrics and posts a mock notification. Specify the queue, job ID, idempotency key, maximum attempts, retry rules, manual review policy, status API, test matrix, source-of-truth and operations checklist.

Then implement only the smallest version that proves one risk. Your documentation should say precisely what it cannot yet guarantee.

I care about reliability because it connects all the layers I enjoy: SQL and source truth, backend business rules, DevSecOps, full-stack user experiences and the responsibility to explain a system honestly.

**The goal is not to avoid every failure. The goal is to make failure bounded, observable, recoverable and understandable.**

[Back to Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Visit the Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)
