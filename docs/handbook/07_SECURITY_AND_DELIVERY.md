# Chapter 07 | Security, testing and the path to release

[← Previous](06_PRODUCTS_AND_AI.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](08_REPRODUCE_THE_WORK.md)

My engineering work has increasingly involved release ownership, where the difficult question is not “does it work once?” but **“what happens when it fails, when someone misuses it, or when the environment changes?”**

## Security is a collection of trust boundaries

~~~mermaid
flowchart LR
    U["User / device"] --> S["Session and MFA"]
    S --> A["Authorisation policy"]
    A --> API["API and domain rules"]
    API --> DB["Least-privilege data access"]
    API --> OUT["Approved external services"]
    DB --> AUDIT["Audit and restore controls"]
    OUT --> AUDIT
~~~

The diagram is a review checklist, not a certification of a particular deployment.

## My practical review lenses

| Boundary | Example failure | Evidence I want |
|---|---|---|
| **Authentication** | Password-only account reaches privileged routes | Real HTTP negative tests, session expiry and re-authentication |
| **MFA / recovery** | TOTP replay succeeds or recovery bypasses policy | Replay, lockout, key handling, passkey and recovery tests |
| **Authorisation** | User swaps an ID and reads another tenant | Cross-tenant negative tests and least-privileged DB role |
| **Source ingestion** | URL validation passes, second DNS lookup connects elsewhere | Pinned transport or enforceable egress controls, SSRF tests |
| **Database operations** | Partial transaction commits | Atomicity, retry, rollback and concurrent-update tests |
| **Output safety** | CSV cell becomes spreadsheet formula | Export encoding tests and safe quoting |
| **Delivery** | A staging “green” is treated as a production sign-off | Exact-commit CI, migration and recovery evidence |
| **Secrets** | Keys leak to logs or frontend | Secret scanning, least privilege and rotation procedures |

## The Fixer security work as a real-world example

The Fixer has active work around mandatory administrator TOTP and WebAuthn, enrolment, session revocation, auditability, source URL safety and security scanning.

The public [MFA draft PR](https://github.com/CayelaemJ/NewChanges/pull/219) and [security remediation PR](https://github.com/CayelaemJ/NewChanges/pull/233) demonstrate a difference I care about: code can be implemented and reviewed without the feature being cleared for release. These changes have required Docker integration checks, browser tests, real roles, deployment-safe keys and migration validation. **An unmerged draft is not a shipped production control.**

One security audit used a local AI scanner. Thousands of generated observations were not thousands of demonstrated vulnerabilities. Model suggestions need source-level evidence, an exploit mechanism, deterministic tests and a disposition. The corresponding [audit triage issue](https://github.com/CayelaemJ/NewChanges/issues/232) remains an engineering task, not a green security badge.

## How I want tests organised

1. **Static and unit checks:** formatting, types, pure functions, boundary cases.
2. **Database tests:** disposable DB, real transactions, constraints, isolation and rollback.
3. **API tests:** authenticated HTTP requests with both happy-path and denial-path checks.
4. **Browser/mobile tests:** genuine user workflows, narrow screens and accessible states.
5. **Security checks:** known risky inputs, secret/dependency/SAST checks and authorisation abuse cases.
6. **Release rehearsal:** migration, backup restore, rollback and exact environment configuration.

A passing unit suite is valuable. It does not establish that a database migration will succeed, a credential will be configured, or a browser flow will remain usable.

## CI is evidence, not decoration

In my GitHub profile, the [Engineering Labs workflow](../../.github/workflows/engineering-labs-ci.yml) runs standard-library tests for four synthetic projects when relevant files change. That verifies local educational examples. It does **not** substitute for the self-hosted Docker and external-service tests required by the larger platforms.

For product releases, I favour:

- Pinning tests to an exact commit.
- Running disposable databases and explicit negative cases.
- Blocking merges on required gates when possible.
- Keeping production secrets out of test artifacts.
- Separating “not run”, “failed”, “passed”, and “not applicable”.
- Treating cost and service availability as operational constraints.
- Never switching live data stores without final sync, writer fencing, rollback and approval.

## Where the learning came from

I have debugged source failures, failed CI, incompatible database assumptions, auth and MFA design questions, cloud migration trade-offs and dependency upgrade risks. The recurring lesson is that the cheapest time to uncover a failure is **before someone relies on the release**.

I want to be the engineer who can explain why a deployment is ready, and also explain why it is not.

[Security field notes](../ENGINEERING_FIELD_NOTES.md) · [The Fixer repository](https://github.com/CayelaemJ/NewChanges)

[← Chapter 06](06_PRODUCTS_AND_AI.md) · [Next: Reproduce the work →](08_REPRODUCE_THE_WORK.md)
