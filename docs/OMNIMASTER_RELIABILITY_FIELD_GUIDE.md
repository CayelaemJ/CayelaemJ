# THE OMNIMASTER RELIABILITY FIELD GUIDE
### Volume VII | What happens after everything goes wrong?

**Cayelaem Jantjies · Reliability engineering, truthful UX, retries and recovery**

[The public Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/) · [My technical handbook](OMNIMASTER_HANDBOOK.md) · [Build the reliability lab](../projects/reliability-recovery-lab/)

---

> Reliable engineering isn't only making the happy path fast. It's explaining exactly what happened when the happy path didn't happen.

I came into technology through statistics, data, reporting and the challenge of making operational decisions trustworthy. As I moved deeper into APIs, databases, automations, cloud delivery and UI/UX development, I learned that the critical question is often **"What if the action only partly succeeded?"**

A failed job, lost response, repeated payment request, slow CDC source or inconsistent status message can make an otherwise elegant product misleading. This volume teaches how to reason about those boundaries.

## Read the five chapters

| Chapter | What you will understand | Hands-on exercise |
|---|---|---|
| [01 · A job is a contract](reliability/01_JOBS_AND_STATE.md) | The difference between received, queued, running, retried, done and dead | Define a finite state machine |
| [02 · Retries without chaos](reliability/02_RETRIES_AND_IDEMPOTENCY.md) | At-least-once delivery, backoff, duplicate effects and idempotency keys | Replay a synthetic job |
| [03 · Dead letters and recovery](reliability/03_DEAD_LETTERS_AND_RECONCILIATION.md) | Why failed items need ownership and safe recovery | Force three failures, then requeue |
| [04 · Make failure understandable](reliability/04_STATUS_UX_AND_OPERATIONS.md) | Frontend status, user trust, operational observability and accessible feedback | Design a truthful job timeline |
| [05 · Beyond a local simulation](reliability/05_PRODUCTION_BOUNDARIES.md) | Transactions, distributed failure, outbox/inbox, source positions and release gates | Write a production upgrade proposal |

## The executable lab

**[Open the OmniMaster Reliability & Recovery Lab](../projects/reliability-recovery-lab/)**.

~~~bash
cd projects/reliability-recovery-lab
python cli.py
python -m unittest discover -v
~~~

The code runs in-memory SQLite with no network, cloud services, accounts, keys or real customer data. It uses synthetic tenants and a simulated integer clock.

~~~mermaid
flowchart LR
    UI["Person requests action"] --> API["Backend accepts job"]
    API --> PEND["PENDING"]
    PEND --> RUN{"Attempt succeeds?"}
    RUN -->|"No, more attempts"| RETRY["RETRY with backoff"]
    RETRY --> RUN
    RUN -->|"No, limit reached"| DEAD["DEAD: operator decision"]
    RUN -->|"Yes"| DONE["DONE with local audit"]
    DEAD --> RECOVER["Manual requeue or safe resolution"]
    RECOVER --> RUN
    PEND -.-> STATUS["Frontend: Queued, not Completed"]
    RETRY -.-> STATUS
    DEAD -.-> STATUS
    DONE -.-> STATUS
~~~

## The example outcome

Two wholly fictional jobs are submitted.

- `tenant-beta` completes at tick 0.
- `tenant-alpha` encounters `source_unavailable` twice, at ticks 0 and 2.
- At tick 6, alpha completes. The local event log records each transition.
- If alpha had failed again, it would enter `DEAD`, where a person must decide whether to requeue it.

**"Effect committed" in this project means an inserted row in one local SQLite database.** It is not a bank payment, a sent email or a successful external service call.

## Why this matters to the person using the software

Consider a page showing **"Upload completed"** when the backend has merely accepted a task. If the source later fails, that message was wrong. The backend's job state and the frontend's language must agree.

The question is not just whether there is a spinner. It is whether someone knows if a task was performed, may still finish, failed safely, needs attention or may already have caused an external effect.

That is the connection between **backend engineering and human-centred UX** I want people to learn.

## The lessons from my own engineering practice

Data pipelines taught me to ask whether records actually reached their destination. Full-stack product work taught me to ask which action was authorised, committed and auditable. Security reviews taught me that a passing test only proves what that test observed. UI development taught me to care about how the result is explained to the person waiting for it.

My professional and independent projects include reporting, integration and security workstreams, but this teaching lab is deliberately fictional. It does not reproduce proprietary operational processes or establish the production maturity of The Fixer or any other live system.

## Where this fits in the library

[Volume III · The Academy](OMNIMASTER_ACADEMY.md) teaches core methods. [Volume V · Build With Me](OMNIMASTER_BUILD_WITH_ME.md) builds a synthetic event-to-metric pipeline. [Volume VI · The Human Interface](OMNIMASTER_HUMAN_INTERFACE.md) studies usability and accessible design. [The Frontend / Backend Playbook](OMNIMASTER_FULLSTACK_PLAYBOOK.md) explains ownership across application layers.

**Volume VII connects all four through failure and recovery.**

[Begin with the job state machine →](reliability/01_JOBS_AND_STATE.md)
