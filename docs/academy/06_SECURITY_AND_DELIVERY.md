# Lesson 06 | Security and release engineering

[← Lesson 05](05_APPLIED_AI.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Next →](07_CAPSTONES.md)

## An app is not ready just because it loads

I've spent significant time working with security findings, CI, MFA, database migrations and deployment constraints. The hardest engineering sentence is often **“this release is not verified yet.”**

## Model the trust boundary

For your fictional delivery application, ask who controls each input:

- The browser can send any route and identifier, even when buttons are hidden.
- A user might submit another tenant's record ID.
- Uploaded files and URLs are untrusted.
- A job can retry or run twice.
- A database role might have privileges far beyond its task.
- An AI answer may contain unsafe instructions or sensitive text.

Put the enforcement where the boundary actually exists: authentication and authorisation on the server, least privilege in the database, bounded outbound access, and contextual checks when rendering output.

## The test ladder

| Test layer | Example | What it does not prove |
|---|---|---|
| Pure/unit | Reject invalid state transition | Real DB transaction correctness |
| DB integration | Roll back a partially failing write | Network identity or UI correctness |
| HTTP API | Wrong tenant ID gets denied | All routes are covered automatically |
| Browser | Accessible submit and confirmation flow | Underlying security of every backend |
| Security negative | Replay MFA step-up or malformed file | General penetration-test certification |
| Release rehearsal | Backup, migration, restore and rollback | Future incidents will never occur |

## Build a local gate

Your minimum local pipeline should:

1. Install from a reproducible lockfile.
2. Run code format/lint, typecheck where applicable, unit tests and build.
3. Launch a disposable database and exercise a real API path.
4. Run at least one denied request and one crash/retry scenario.
5. Confirm the test environment has no live credentials.
6. Report the **exact commit SHA** that was tested.

The profile's [GitHub Actions workflow](../../.github/workflows/engineering-labs-ci.yml) covers its own small Python labs and documentation navigation. It is not the release gate for The Fixer, CABO or a production finance system.

## An MFA case you should understand

A privileged user signs in with a password. If the session is not freshly verified, the administrative mutation should fail, even if the user calls the endpoint directly. Factor enrolment and recovery must not bypass the same policy.

Design tests for expired sessions, repeated TOTP, wrong authenticator, changed passkey, revoked sessions, emergency recovery and normal-user access.

The [Fixer MFA PR](https://github.com/CayelaemJ/NewChanges/pull/219) illustrates real implementation work with outstanding release gates. Don't translate “there is a PR” into “it's secured in production.”

## A database cutover exercise

You have a PostgreSQL snapshot that restores successfully. The old database still receives writes. Your staging API starts.

**Question:** should you switch live traffic?

**My answer:** no, not until you have a verified final sync, one authorised writer, data parity, restricted credentials, auth tests, recovery plan and deployment approval. A snapshot restore is one test, not the whole migration.

See [Decision journal](../field-guide/05_DECISION_JOURNAL.md) and [Debugging casebook](../field-guide/02_DEBUGGING_CASEBOOK.md).

## Learning checkpoint

**Pass when:** you can demonstrate a denied user request, a testable rollback, a CI failure, and a written list of unverified assumptions that would block a real release.

**Take-home exercise:** add a file named RELEASE_GATES.md to your capstone. For every gate record: owner, test command, environment, evidence, state and rollback procedure.

[← Lesson 05](05_APPLIED_AI.md) · [Next: Capstones →](07_CAPSTONES.md)
