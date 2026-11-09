# Chapter 04 | Data engineering as a discipline

[← Previous](03_SYSTEMS_IN_THE_WILD.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](05_ANALYTICS_ENGINEERING.md)

My starting principle is simple: **data cannot become reliable by changing its colour in a dashboard**. Reliability begins with source events and continues through extraction, transformation, storage, serving and recovery.

## A pipeline is a sequence of contracts

~~~mermaid
flowchart LR
    A["Operational SQL / APIs / files"] --> B["Source identity, grain and access"]
    B --> C["Ingestion & checkpoint"]
    C --> D["Quality, lineage & modelling"]
    D --> E["Curated data / semantic model"]
    E --> F["APIs, BI, operational decisions"]
    F --> G["Reconciliation, monitoring, rollback"]
~~~

Every arrow is a place data can be lost, duplicated, misclassified or delayed.

## 1. Define the grain before writing the join

Imagine an operational system with one order, three deliveries and five quality observations. Joining all three at the raw record level can multiply the order amount fifteen times. That is not a DAX error; it is a relational grain mismatch.

**My review sequence:**

1. State each table's business event and unique key.
2. Identify one-to-many relationships and expected cardinality.
3. Reconcile counts and amounts before and after joins.
4. Determine whether to aggregate early, create bridge tables or model separate facts.
5. Add tests for unexpected duplicate keys and late-arriving events.

This is the same thinking I have used in manufacturing, banking and research analytics.

## 2. Separate business time from modification time

A payment may have occurred in June, been corrected in July and been ingested in August. These are different facts: **event time**, **source modification time** and **pipeline processing time**. Historical reports may need any of the three.

An updated timestamp that is nullable, rounded to one second or never advanced by manual updates cannot by itself guarantee lossless incremental loads.

**Design questions:** Can multiple updates share a watermark? Can a record be deleted physically? What happens to a correction for a closed period? Is the source query repeatable? Can the pipeline resume after a partial write?

## 3. Choose polling, CDC or batch on purpose

| Strategy | Useful when | Failure to anticipate |
|---|---|---|
| **Scheduled batch** | Daily reports and stable extraction windows | Missed windows, late files and inconsistent snapshots |
| **Watermark polling** | Source exposes reliable version/update keys | Same-timestamp writes, nullable values and invisible deletes |
| **Row-binlog CDC** | Changes must be captured continuously or near-continuously | Binlog retention, transaction ordering, checkpoints and read privileges |
| **Event publishing** | The source application can emit durable domain events | Producer/consumer contracts, duplicates, retries, poison messages |

The Fixer's MySQL source work has been exploring these boundaries. Its existing reporting views and synthetic binlog laboratory are **not yet the same production pipeline**. See [CDC integration work](https://github.com/CayelaemJ/NewChanges/issues/241).

## 4. Bronze, Silver, Gold is a contract, not a naming scheme

- **Bronze:** preserve source identity, payload, ingestion metadata and replay evidence.
- **Silver:** produce validated, typed, deduplicated and business-consistent records.
- **Gold:** curate consumer-level measures and aggregates at a documented grain.

In Microsoft Fabric or Databricks these layers can be implemented using lakehouse and Delta-style patterns where appropriate. In my public [CDC Replay Lab](../../projects/cdc-replay-lab/), a small SQLite program illustrates the semantics without pretending to be a managed distributed lakehouse.

## 5. Let each validation own a real risk

I do not want every component to reimplement a slightly different definition of an email address, effective date or identifier. Validation should be deliberate:

- **At the source boundary:** check structure, required keys, contract type and authorisation.
- **In the database:** enforce relationships, uniqueness and transactional consistency.
- **At the business layer:** apply domain policy with explicit error handling and audit.
- **At the consumer:** explain freshness, completeness and interpretation.

The [Data Quality Contracts Lab](../../projects/data-quality-contracts/) shows a deliberately small contract with readable failures instead of silent repairs.

## 6. Design the failure path before release

I expect a pipeline to encounter duplicate input, a malformed record, transient network errors, unavailable secrets, unexpected schema changes and backfills. My preferred evidence includes:

| Failure | Recovery property |
|---|---|
| Same event delivered twice | Idempotent handling or detected duplicate |
| Worker restarts mid-batch | Transactional checkpoint with no lost committed work |
| Source timestamp is ambiguous | Explicit warning or alternate change mechanism |
| Destination write partially fails | Rollback, retry and clear dead-letter handling |
| A user loses access | Server-side scope enforcement and revocation tests |
| Historic source records change | Recompute impacted aggregates rather than full arbitrary rewrite |

## A reproducible design exercise

Open [CDC Replay Lab](../../projects/cdc-replay-lab/) and trace one account through create, update and delete operations. Repeat the events. Check that the current projection stays correct and the event log retains the deletion. Then inspect what the toy example lacks: source transaction capture, a durable source checkpoint, cross-entity ordering and multi-writer consistency.

**The distinction between a demonstration and a production pipeline is part of the lesson.**

Further reading: [System design playbook](../OMNIMASTER_SYSTEM_DESIGN.md) · [Source contract and mission history](../OMNIMASTER_MISSION_DOSSIERS.md)

[← Chapter 03](03_SYSTEMS_IN_THE_WILD.md) · [Next: Analytics engineering →](05_ANALYTICS_ENGINEERING.md)
