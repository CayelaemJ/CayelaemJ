# Chapter 02 | From statistics to full-stack ownership

[← Previous](01_THE_ENGINEER.md) · [Table of contents](../OMNIMASTER_HANDBOOK.md) · [Next →](03_SYSTEMS_IN_THE_WILD.md)

## My technical origin

I studied **Statistics and Data Science** at the University of Pretoria, graduating with a BCom in 2023. That education still shapes how I approach software engineering. I start by asking whether the data supports the statement somebody wants to make. A model can be mathematically correct while the source events, sample, joins or time window are wrong.

My professional path moved outward from analytical questions.

## Timeline of practice

| Period | Environment | What I learned |
|---|---|---|
| **2023** | University projects and early analytics exposure | Statistics, predictive reasoning, reproducibility and the importance of data definition |
| **2023–2024** | Broadcasting and enterprise reporting | Operational SQL, media/service KPIs, automation, reporting under deadlines |
| **2024–2025** | Consulting across banking, capital markets, FMCG and media | Power BI, DAX, stakeholder definitions, security-aware analytics across organisations and markets |
| **2025–early 2026** | Agriculture, social impact and independent experimentation | ERP/NAV mappings, data capture workflows, business adoption, cross-system reasoning |
| **January–August 2026** | Remote Australian manufacturing delivery | SQL Server, Fabric, Power Automate, logistics and workforce models, production/scheduling reporting |
| **August 2026 onward** | Data/BI and full-stack platform responsibility | TypeScript backends, APIs, PostgreSQL, tenant access, admin workflows, security, cloud and testing |

Dates are broad career context, not an assertion that every engagement was continuous or full-time. The [case-study record](../CLIENT_CASE_STUDIES.md) provides engagement-level descriptions.

## Three turning points

### 1. The grain of the data mattered more than the chart

In industrial and commercial reporting, there are many plausible tables to join. A schedule row, a dispatch, a production batch and an invoice are not necessarily the same business event. A naive join can multiply facts. I learned to define the grain, choose stable keys, check cardinality and reconcile back to the source before trusting a DAX measure.

**What changed:** I stopped thinking of Power BI as the place where incorrect upstream semantics should be patched.

### 2. Automation changed the value of the work

Producing the same manual report every week teaches an obvious lesson: the repeatable task should be engineered. Automated SQL extracts, dataflows, scheduled reports and controlled transformations reduced human hand-offs and made failures easier to investigate.

My historical CV reports reductions of **up to 70% in manual reporting effort** in some engagements. That is a reported historical result, not a public benchmark reproduced by this repository.

**What changed:** I began measuring usefulness in work removed from the process, not only charts added to a page.

### 3. The data product became a software product

Platform work taught me that a metric may need an API, a permissions model, a transaction, a workflow, an audit log and deployment gates. The user's experience and the correctness of the database are not separate disciplines.

**What changed:** I took a stronger interest in TypeScript, React, PostgreSQL, authentication, background jobs, cloud infrastructure and release engineering.

## Cross-industry pattern recognition

The industries may look unrelated, but I keep finding the same failure modes:

- **Financial services:** date-aware measures, restricted information and auditability.
- **Manufacturing:** grain, operational latency, workforce/scheduler alignment and source-system drift.
- **FMCG and research:** large data volumes, survey joins, data-quality assumptions and commercial interpretation.
- **Media:** linking sentiment, contact, service-level and customer experience signals.
- **Agriculture:** bridging ERP/NAV semantics and decision-ready reporting.
- **Education and social impact:** privacy, consent, human interpretation and long-lived records.

The tools vary; the underlying engineering questions persist.

## How I now explain my career

I have been an analyst, BI developer, data engineer, application builder and the person debugging the pipeline when everyone is waiting for the dashboard. That range is not proof that I have expert-level experience in every technology. It means I have learned to take responsibility for **the whole path from problem to useful outcome**.

For the detailed engagement record, see [Client case studies](../CLIENT_CASE_STUDIES.md). For what I am building independently, continue to the next chapter.

[← Chapter 01](01_THE_ENGINEER.md) · [Next: Systems in the wild →](03_SYSTEMS_IN_THE_WILD.md)
