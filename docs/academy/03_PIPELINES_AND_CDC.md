# Lesson 03 | Pipelines, data quality and CDC

[← Lesson 02](02_SQL_AND_MODELLING.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Next →](04_BUILD_APPLICATIONS.md)

## The pipeline is a promise to the consumer

Data engineering is more than moving data from A to B. It means preserving the meaning and recoverability of changes while meeting a useful freshness target.

A dashboard that refreshes every minute is not “real time” if the underlying extraction skips events.

## Four terms to learn

**Snapshot:** the source state at a point in time. Useful for rebuilding or comparing, but may not explain intermediate changes.

**Watermark:** a position or timestamp used to resume extraction. Its precision and consistency matter.

**CDC:** a mechanism that captures changed rows or events, including cases such as deletions and repeated updates that snapshots may hide.

**Idempotency:** processing the same source event twice should not introduce an unintended duplicate effect.

## Study the event path

~~~mermaid
flowchart LR
    SRC["Source event"] --> READ["Read with stable position"]
    READ --> LOG["Persist event ID and payload"]
    LOG --> APPLY["Apply valid current state"]
    APPLY --> AGG["Publish consumer aggregate"]
    APPLY --> CHECK["Record durable checkpoint"]
    CHECK --> READ
~~~

The diagram is an educational pattern. A production implementation must also handle transaction boundaries, source retention, invalid records, backfills, access and crash recovery.

## Three essential exercises

**Exercise A: duplicates.** Take the [CDC Replay Lab](../../projects/cdc-replay-lab/) and apply the same event ID twice. Check whether the current projection and aggregates remain stable.

**Exercise B: delete.** Apply a deletion. Can the reader distinguish a deleted account from an account that simply did not appear in today's snapshot?

**Exercise C: restart.** Simulate a failure between reading and committing a source position. Write down how the sink and checkpoint should be coordinated. A system should either replay safely or prove the transaction was committed before advancing.

Run the example:

~~~bash
cd projects/cdc-replay-lab
python -m unittest discover -v
~~~

## Build a small source contract

Define a fictional record:

~~~json
{
  "source": "fictional-orders",
  "event_id": "evt-0001",
  "entity_id": "order-17",
  "operation": "UPSERT",
  "sequence": 42,
  "amount_cents": 12999
}
~~~

Document whether the event sequence is monotonically ordered per entity or globally, how a DELETE is represented, and how malformed amounts are handled.

Then use the [Data Quality Contracts Lab](../../projects/data-quality-contracts/) to practise rejecting duplicates, invalid decimals and freshness violations.

## Common ways pipelines lie accidentally

| Symptom | Possible cause | How to test |
|---|---|---|
| Green job, stale dashboard | Batch made no progress but marked success | Inspect checkpoint before/after oversized source event |
| Rows suddenly doubled | Replays or join grain mismatch | Replay same IDs and reconcile sums |
| Delete never appears | Watermark on current table has no deletion signal | Delete record and watch extraction |
| Backfill changes history | Event time and modification time confused | Correct a prior-period record |
| One bad row blocks whole job | No quarantine or defined error policy | Inject synthetic malformed input |

The synthetic [Fixer CDC work](https://github.com/CayelaemJ/NewChanges/pull/237) and [open adapter issue](https://github.com/CayelaemJ/NewChanges/issues/241) illustrate how the question becomes harder in real systems.

## Checkpoint

**Pass when:** you can demonstrate create, update, duplicate, delete and retry behaviour using fictional data, and explain what additional evidence production CDC would require.

**Your engineering journal entry:** Which failure did you intentionally create? What did you expect? What happened? What change would make the system easier to debug?

[← Lesson 02](02_SQL_AND_MODELLING.md) · [Next: Full-stack workflows →](04_BUILD_APPLICATIONS.md)
