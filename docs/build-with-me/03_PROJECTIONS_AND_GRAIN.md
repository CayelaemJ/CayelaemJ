# Build With Me 03 | Model history, current state and business metrics

[← Ingestion](02_INGESTION_AND_TRANSACTIONS.md) · [Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Next: Users and metrics →](04_FROM_METRICS_TO_USERS.md)

## History is not current state

An event log answers **what happened**, and a projection answers **what is true according to the model now**. They are related, but they cannot be treated as interchangeable.

Our simulation uses a deliberately small Bronze/Silver/Gold idea:

- **Bronze:** `bronze_events`, one row per distinct source change.
- **Silver:** `silver_accounts`, one latest logical version per tenant/account. Deletion is represented by a tombstone.
- **Gold:** a query counting active accounts and summing their integer-cent balances by tenant.

These are roles of data, not proof that this is Microsoft Fabric, a Databricks Delta Lake or a managed streaming platform.

## Follow one fictional account

| Event | Business entity | Version | Operation | Silver result |
|---|---|---:|---|---|
| evt-01 | alpha/acct-a | 1 | UPSERT 12,000 cents | Active, 12,000 |
| evt-04 | alpha/acct-a | 2 | UPSERT 14,000 cents | Active, 14,000 |
| hypothetical evt-09 | alpha/acct-a | 1 | UPSERT 12,000 cents | Still active, 14,000; historical arrival retained |

When an event arrives out of order, we do not overwrite the more recent state with an older account version.

**Important caveat:** in real source systems, versions may not be strictly monotonic or globally comparable. This educational contract assumes they are.

## Why DELETE becomes a tombstone

An account's disappearance from a snapshot may mean deletion, missing extraction, lost permission or a filter change. The simulation represents DELETE explicitly, preserving evidence in Bronze and marking Silver as deleted.

The Gold query excludes tombstones. It does not claim that a deleted account has been legally erased from all storage. Actual retention and privacy policies would need separate design.

## The grain of the metric

Our business measure is:

~~~sql
SELECT COUNT(*) AS active_accounts,
       COALESCE(SUM(amount_cents), 0) AS balance_cents
FROM silver_accounts
WHERE tenant = ?
  AND is_deleted = 0;
~~~

Because Silver enforces a primary key on `(tenant, account)`, one account contributes once to the sum. This is not a financial ledger: balances are teaching values without double-entry controls.

## Run and reconcile

~~~bash
python cli.py demo
~~~

The expected synthetic results are 23,000 cents for fictional-alpha and 37,000 cents for fictional-beta, both with two active accounts.

The independent `reconciles()` method creates a separate in-memory database, replays Bronze and compares reconstructed Silver state with the original. If somebody silently corrupts a projection, the comparison should fail.

**Limitation:** replay is only as correct as the event history and model rules. If Bronze itself is incomplete, replaying it perfectly may still reproduce the wrong reality.

## Your exercise

Add a third fictional tenant and two accounts. Verify that the existing tenants' totals remain unchanged. Then corrupt one Silver amount on purpose and prove reconciliation reports false.

### Completion test

You can explain what each layer means, why source identity and business grain are different, and why correct-looking Gold totals are not sufficient without reconciliation to source.

[← Chapter 02](02_INGESTION_AND_TRANSACTIONS.md) · [Next: Users and metrics →](04_FROM_METRICS_TO_USERS.md)
