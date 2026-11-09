# Build With Me 06 | What it would take to become a real platform

[← Failure lab](05_FAILURE_LAB.md) · [Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [30-Day Expedition](../THIRTY_DAY_ENGINEERING_EXPEDITION.md)

The most useful part of a toy project might be the honesty about what it **cannot** do. A script can prove a local invariant and still be inappropriate for real users.

## The gap from demonstration to operations

| Dimension | In this lab | Production questions |
|---|---|---|
| **Source capture** | In-code fictional events | Which source emits changed rows, offsets, deletes and transactions? |
| **Storage** | SQLite in-memory | Durable backup, retention, migrations, HA and restricted credentials? |
| **Identity** | None | Who authenticated the caller, and who granted the tenant scope? |
| **Checkpoints** | Event position stored in Bronze | How is source acknowledgement atomic with destination commit? |
| **Concurrency** | One process | Multiple readers, concurrent writers, ordering, deadlocks and retries? |
| **Schema evolution** | One fixed dataclass | Versioned source contracts and backwards-compatible migrations? |
| **Quality** | Focused input checks | Completeness, reconciliation, late events, observability and alerts? |
| **Reporting** | One aggregate per tenant | Documented KPIs, as-of semantics, SLO, privacy-safe exports? |
| **Security** | Input validation and parameterised SQL | Auth, authorisation, egress, secrets, RLS, key rotation and negative testing? |
| **Release** | Disposable local test | Staging, load testing, restore, rollback, approval and on-call plan? |

## A staged upgrade plan

### Stage 1. Make the dataset and contracts explicit

Persist synthetic input fixtures in versioned files, add schema documentation and verify that every dataset can be regenerated. Document which identifiers are global versus per account.

### Stage 2. Add durable storage and recovery

Use a disposable local database file or container. Simulate a process restart, database lock and damaged projection. Check whether the event log can rebuild state and whether a restore produces the same answer.

### Stage 3. Connect a real **synthetic** source

Choose a local test MySQL/PostgreSQL service or event queue. Define how to read changes and retain source positions; never connect the learning project to an employer's production database.

### Stage 4. Add real application security

Introduce a trusted identity boundary, tenant memberships, role-specific access and deny-by-default API handlers. Validate cross-tenant denial over real HTTP requests, including ID tampering.

### Stage 5. Serve a consumer

Build one accessible dashboard or reporting API with a visible source-as-of status, structured errors and audit metadata. Do not call it real time until end-to-end freshness is measured.

### Stage 6. Operate and explain

Automate exact-commit tests and build, restore rehearsal, dependency review, logs, metrics, incident playbooks and a rollback procedure. Have another engineer attempt the steps without your machine.

## The true comparison with my professional experience

I have worked on enterprises where source data, access control, reporting metrics, deployment cost and user-facing workflows collide. The public reference projects and independent builds are larger, less tidy and often still being improved.

This synthetic lab is designed to **transfer the habits** without exposing those private operational details. It does not establish that The Fixer or CABO is production-ready.

## What I would look for in a junior engineer's project

I would not demand a complex microservice ecosystem. I would ask:

- Can you explain the authoritative business event?
- Are the keys, joins and time semantics correct?
- Can your code be run from clean setup instructions?
- Have you tested a failed input and an unauthorised action?
- Can you distinguish a tutorial test from a release gate?
- Which decisions would you reconsider at larger scale?

Answer those clearly, and you have something more compelling than a stack-name collection.

## Final assignment

Write a two-page architecture decision record that proposes one safe next step for the project. Include the actual risk, the alternatives, a small disposable experiment, the acceptance tests, the rollback path and a candid limitation.

**My closing principle:** broad engineering ability isn't about writing every component yourself. It's knowing which boundaries need to exist, how to validate them, and when to bring in specialists.

[← Chapter 05](05_FAILURE_LAB.md) · [Return to Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Take the 30-Day Expedition →](../THIRTY_DAY_ENGINEERING_EXPEDITION.md)
