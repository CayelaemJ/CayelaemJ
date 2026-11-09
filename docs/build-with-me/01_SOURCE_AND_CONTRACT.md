# Build With Me 01 | Define the source before building a pipeline

[← Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Next: Ingestion →](02_INGESTION_AND_TRANSACTIONS.md)

## The first question I ask

**What happened in the real world, and what does one record mean?**

In enterprise BI and manufacturing, I learned that a source system often stores what was convenient for its users, not what an analytics engineer expects. A delivery, invoice, account update, school progression decision and audit event have different identities and timing semantics.

This chapter uses **fictional account updates** only. It is not a bank ledger.

## Step 1. Read the event contract

Open [engine.py](../../projects/data-to-decision-platform/engine.py) and find the `Event` dataclass. It contains:

| Field | Why it exists | What the demo assumes |
|---|---|---|
| `event_id` | Identifies one submitted source change | Unique and stable across retry |
| `position` | Identifies where a change sits in a fictional source stream | One unique positive integer per event |
| `tenant` and `account` | Identify the business entity | One current state per tenant/account |
| `version` | Distinguishes newer from older account states | Strict integer that increases per account |
| `operation` | Distinguishes UPSERT from DELETE | Only those two operations exist |
| `amount_cents` | Keeps the fictional balance exact | Nonnegative integer; DELETE is zero |
| `occurred_at` | Records time with explicit timezone | Aware ISO-8601 text |

The **source position** is a teaching stand-in. Real MySQL binlog offsets, Kafka offsets or application sequences have much more complex transaction semantics.

## Step 2. Make invalid input fail visibly

The validator rejects negative balances, Boolean money values, malformed IDs, an invalid source version, a DELETE with a nonzero balance and timestamps lacking a timezone.

Run:

~~~bash
cd projects/data-to-decision-platform
python -m unittest discover -v
~~~

A validation check is valuable because its consequences are explicit. Avoid adding rules merely because a form looks impressive; every rejection should protect a known invariant.

## Step 3. Write the business question

We want the **number of active fictional accounts and total active balances for one tenant**. That means:

- Grain: one latest account state per tenant/account.
- Deleted accounts do not contribute to the total.
- Each account contributes exactly once.
- The caller's identity and permitted tenant scope are **out of scope in this standalone demo**, and must be enforced by a real application.
- Integer cents avoid unnecessary binary floating-point rounding.

## Your exercise

Create two additional fictional updates. One should be a correction to an existing account with a higher version; the other should be a deliberately invalid negative value.

Before running the pipeline, predict which batch should commit, which should roll back and what the aggregate will become. Record your predictions. Then run the test.

## What I would ask in a code review

1. Does source position uniquely identify a logical change?
2. Who generates account versions?
3. Could two writers issue conflicting versions?
4. Does the source guarantee global ordering, per-account ordering or neither?
5. Which timestamps are business time versus ingestion time?
6. What is the rule for correcting an error in already-published data?

### Completion test

You can explain every `Event` field, identify a malformed input and state the current-account grain without reading the query.

[Next: Ingestion and transactions →](02_INGESTION_AND_TRANSACTIONS.md)
