# Chapter 05 | BI, semantic models and decision systems

[← Previous](04_DATA_ENGINEERING.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](06_PRODUCTS_AND_AI.md)

BI is often treated as a presentation layer. My experience suggests it is closer to **a governed interpretation layer** between operational activity and decisions.

## The anatomy of a trustworthy metric

Consider “active customer rate.” A meaningful implementation must specify:

- **Population:** which users are included?
- **Observation window:** today, rolling 30 days, a financial month or programme-to-date?
- **Activity definition:** logins, transactions, settled balances or something else?
- **Grain:** person, account, transaction or organisation?
- **Access boundary:** which employers, markets or teams may see the result?
- **History:** how do corrections, deleted records or changing memberships affect earlier periods?

Without these definitions, two teams can both report a plausible percentage and both be wrong for the decision at hand.

## Where I developed this discipline

Banking reporting across four African markets, 270M+ survey records in a commercial research engagement, Australian production and scheduling reporting, and ERP/NAV-derived agricultural analytics exposed me to different kinds of measure ambiguity.

In each case, correctness required conversations with business owners **and** careful source analysis. I have written DAX, Power Query transformations and SQL, but the most valuable step is often getting agreement on what a metric *means*.

## My semantic-model review checklist

| Layer | What I inspect | Typical symptom |
|---|---|---|
| **Source** | Stable keys, nulls, event date, reconciliation totals | Data differs from operational system |
| **Relationships** | Star-schema grain, direction, ambiguous paths, many-to-many joins | Totals change when unrelated filters are applied |
| **Measures** | Filter context, denominators, time intelligence, blank handling | Percentage exceeds expected range or historical figures drift |
| **Security** | Row-level access, market/employer separation, export paths | A user can inspect another organisation's measure |
| **Performance** | Query plans, cardinality, repeated transformations, visuals | Slow page loads and excessive model scans |
| **Delivery** | Refresh status, source latency, missing periods, fallbacks | “Live” dashboard shows stale data |

## Practical performance reasoning

A slow dashboard invites many unhelpful fixes: adding more compute, reducing visuals arbitrarily or caching incorrect results. I start by isolating where time is spent.

1. Profile source query and row counts.
2. Check filter predicates, indexes and aggregation grain.
3. Review model relationships and DAX query patterns.
4. Determine whether work should happen once in SQL/ELT rather than repeatedly per visual.
5. Re-measure with comparable filters and data.
6. Verify the resulting business numbers did not change.

My previous CV reports a **40% dashboard-load improvement** in an optimisation engagement and reductions in manual report work of up to **70%** in some workflows. Those numbers describe professional experience; this repository does not include client performance logs.

A small related exercise: [SQL Query Plans Lab](../../projects/sql-query-plans/). It compares a full scan against a composite-index range search on fictional data. SQLite is a teaching tool here, not a benchmark for Power BI, Fabric or SQL Server.

## Modern data platforms without cargo-cult architecture

I have worked with SQL Server, Power BI and Microsoft Fabric-related analytics, and developed skills in PySpark/Databricks patterns. My evaluation of any new stack asks: Do we need distributed processing? Who owns the transformation? What is the cost of moving the data? Is there a stable semantic layer? What happens during source correction?

A sophisticated lakehouse architecture is useful when its scale, history, governance or interoperability justify it. It is not automatically superior to a clear and well-indexed SQL query.

## How I explain technical decisions to business users

I translate “the join changes row multiplicity” into “the same delivery has been counted more than once.” I translate “watermark collision” into “two legitimate updates may arrive with the same timestamp, so the report could miss one.” I translate “role-based access” into “an employer must only see people and metrics they are allowed to see.”

**A good analytic product gives decision-makers confidence about its assumptions, not merely colourful certainty.**

[Professional experience](../CLIENT_CASE_STUDIES.md) · [Technical skills](../TECHNICAL_SKILLS.md) · [SQL runnable demo](../../projects/sql-query-plans/)

[← Chapter 04](04_DATA_ENGINEERING.md) · [Next: Software and AI →](06_PRODUCTS_AND_AI.md)
