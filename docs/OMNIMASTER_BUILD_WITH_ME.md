# OMNIMASTER | BUILD A SYSTEM WITH ME
### Volume V · From source events to trustworthy decisions, one verified boundary at a time

**Cayelaem Jantjies | A complete, fictional, runnable engineering walkthrough · November 2026**

[GitHub cover](../README.md) · [Volume I: My engineering history](OMNIMASTER_HANDBOOK.md) · [Volume III: Academy](OMNIMASTER_ACADEMY.md) · [Data-to-Decision code](../projects/data-to-decision-platform/) · [Interactive study room](interactive/index.html)

---

> I don't want someone to leave my GitHub merely thinking I know a lot of tools. I want them to know **how to start with a confusing problem, break it into contracts, build a small system, verify it, find what isn't proven, and explain the decisions to another human**.

This is an applied counterpart to my previous volumes. The code is not a giant platform, but a fully **reproducible synthetic example** spanning data contracts, ingestion, SQLite transactions, current state, metrics and testing. Every chapter explains the choices, alternatives, failure scenarios and limitations.

## Your working project

[**Open the Data-to-Decision Platform source →**](../projects/data-to-decision-platform/)

~~~bash
git clone https://github.com/CayelaemJ/CayelaemJ.git
cd CayelaemJ/projects/data-to-decision-platform
python cli.py demo
python cli.py failure
python -m unittest discover -v
~~~

Only Python 3.12+ is needed. Data is fictional, storage is in-memory, no packages are downloaded and no external service is contacted.

### What you will observe

| Stage | Meaning | Evidence you can inspect |
|---|---|---|
| **Source** | Eight fictional events from two organisations | The `sample_events()` fixture |
| **Boundary** | IDs, source positions, timezone-aware timestamps and nonnegative cents | `validate()` and negative tests |
| **Bronze** | Immutable-style event history with unique identity | `bronze_events` table and replay tests |
| **Silver** | Current version per tenant/account and DELETE tombstones | `silver_accounts` projection |
| **Gold** | Synthetic active-account counts and balances by tenant | Parameterised `metrics_for()` query |
| **Operations** | Atomic failure, duplicate replay and independent reconciliation | `cli.py failure`, `reconciles()` and unit tests |

The sample's expected Gold result is **23,000 cents for fictional-alpha** and **37,000 cents for fictional-beta**. Both groups have two active accounts. The numeric values are *test fixtures*, not real financial data.

~~~mermaid
flowchart LR
    S["Fictional source events"] --> C["Contract validation"]
    C --> B["Bronze event log"]
    B --> P["Silver latest state"]
    P --> G["Gold tenant metrics"]
    B --> R["Independent replay"]
    R --> P
    C -->|"Invalid event"| X["Rollback entire batch"]
~~~

## The six guided chapters

| Chapter | Question | Practical result |
|---|---|---|
| [01 · Define the source](build-with-me/01_SOURCE_AND_CONTRACT.md) | What is an event, and who owns the truth? | Source contract and validation tests |
| [02 · Ingest with guarantees](build-with-me/02_INGESTION_AND_TRANSACTIONS.md) | What must be atomic, unique and replayable? | Transactions, version and duplicate behaviour |
| [03 · Model the current state](build-with-me/03_PROJECTIONS_AND_GRAIN.md) | How do history and latest state differ? | Bronze/Silver/Gold and semantic reconciliation |
| [04 · Deliver the metric](build-with-me/04_FROM_METRICS_TO_USERS.md) | What makes a number useful and appropriately scoped? | Metric contract, privacy boundary and API design exercise |
| [05 · Break and prove the system](build-with-me/05_FAILURE_LAB.md) | What happens when inputs conflict or processing fails? | Failure injection, expected invariants and regression tests |
| [06 · Make the production boundary explicit](build-with-me/06_BEYOND_THE_DEMO.md) | What would be required before real customers used this? | Auth, checkpoints, durable storage, operations and cost roadmap |

## How this project resembles my actual work

It connects habits I developed in enterprise reporting, manufacturing, data platform experiments and full-stack work:

- **BI and manufacturing:** define grain and source truth before computing a measure.
- **Data engineering:** make ingestion, replay, historical changes and error paths explicit.
- **Backend development:** treat database transactions as correctness boundaries.
- **Security-conscious delivery:** distinguish a tenant parameter from actual authorisation.
- **Technical leadership:** write down the rejected alternatives and release evidence.

It does **not** reproduce any employer's code, actual The Fixer architecture or a live CDC service. The point is to teach general reasoning without exposing proprietary systems or overstating a demonstration.

## Two extra routes

**[30-Day Engineering Expedition](THIRTY_DAY_ENGINEERING_EXPEDITION.md)** gives a day-by-day plan to create a real portfolio project, with tangible artifacts rather than an arbitrary course badge.

**[Interactive Study Room](interactive/index.html)** is a small offline HTML/JavaScript interface with scenario questions and optional local progress. Download/clone the repo and open the HTML file in a browser; it is not presented as a hosted GitHub Pages app.

## What you should have when you finish

A clear problem contract, a runnable synthetic dataset, deterministic tests, documented failures, a metric whose grain you can explain, an honest security boundary, a system design decision log, and a list of production capabilities still missing.

**Build small, understand deeply, test the denial path, and learn to say what is *not* verified.**

[Start Chapter 01 →](build-with-me/01_SOURCE_AND_CONTRACT.md)
