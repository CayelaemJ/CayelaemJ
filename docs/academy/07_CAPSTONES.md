# Lesson 07 | Capstones and proof of work

[← Lesson 06](06_SECURITY_AND_DELIVERY.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Try the arcade →](../OMNIMASTER_ARCADE.md)

You do not need to copy the size of my independent platforms. You need to finish a **small, believable system** and prove its invariants.

## Capstone A. The trustworthy operations dashboard

**Goal:** build a complete synthetic operations pipeline from source events to a governed dashboard or local report.

### Required features

- Fictional source data covering at least two organisations.
- Clear entities, source grain and keys.
- Ingestion/replay logic that handles duplicates, corrections and deletes.
- A curated reporting layer with at least three documented KPIs.
- An authorised API endpoint or equivalent scoped consumer layer.
- Automated tests for data quality, cross-tenant access and business invariants.
- A README explaining freshness, source reconciliation and limitations.

### Architecture sketch

~~~mermaid
flowchart LR
    S["Synthetic events"] --> R["Replay / ingestion"]
    R --> Q["Quality & state projection"]
    Q --> M["Business metrics"]
    M --> A["Scoped API or report"]
    A --> U["Reader / operator"]
~~~

**Use as a starting point:** [CDC Replay Lab](../../projects/cdc-replay-lab/) and [SQL Query Plans Lab](../../projects/sql-query-plans/). Those labs are examples, not drop-in production services.

### Failure demonstration

Deliberately send the same event twice, correct a historic amount and delete an account. Record expected and actual Gold aggregates at each step. Then introduce a filter that would expose another organisation's data and prove the access layer blocks it.

## Capstone B. The responsible learning assistant

**Goal:** build a small fictional learning workflow where a model-assisted output can be inspected and rejected.

### Required features

- Three fictional, approved learning passages.
- Question/answer JSON schema with source evidence.
- Offline evaluation for fabricated source IDs, unsupported claims and invalid fields.
- Deterministic rubric or review control that prevents silent grade writes.
- A fake provider-failure mode and safe fallback/no-answer response.
- A policy document covering consent, privacy, retention and what is *not* proven.

**Use as a starting point:** [Offline AI Output Evaluation Lab](../../projects/ai-output-evaluation/).

**Avoid:** real learners, confidential school records, publicly accessible private prompts, implied grading certification or unreviewed automatic advancement.

## Capstone C. The secure workflow application

**Goal:** make a small tenant-scoped work-order/exception tracker.

### Required features

- Login and server-validated permissions, or an explicitly documented local fake-auth test harness.
- CRUD and state changes with relational constraints.
- Full negative tests for cross-tenant IDs and invalid transitions.
- Observable audit results and safe error messages.
- A disposable database and reproducible build/test script.
- A rollback/recovery document.

**Inspiration:** [The Fixer](https://github.com/CayelaemJ/NewChanges), but do not copy or imply ownership of someone else's private implementation.

## Your public README should answer these questions

1. **Problem:** who needs this and why?
2. **Scope:** what is implemented, not what you want to build next year?
3. **Architecture:** source, application, security and operational boundaries.
4. **Data:** is the sample fictional, public and legitimately used?
5. **Setup:** can a stranger run it using a documented command?
6. **Verification:** what tests passed at what commit?
7. **Security:** what does the system deny and what has not been assessed?
8. **Decisions:** what alternatives did you reject and why?
9. **Limitations:** what would be needed before production?
10. **Learning:** what went wrong and what changed in your thinking?

## A portfolio reviewer rubric

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Source truth | Missing | Named | Validated by tests |
| Data model | Guesswork | Documented | Grain and invariants verified |
| API/workflow | Demo-only | Works | Denial paths and retries tested |
| Quality | No tests | Basic tests | Negative and recovery cases |
| Operations | None | Setup notes | Reproducible CI and rollback |
| Communication | Marketing | Honest README | Evidence, trade-offs and limits |

**10–12 points** is a strong educational project, not a universal production certification. **6–9** shows a useful start. Below that, identify one missing boundary and fix it before adding more features.

## The last exercise: teach somebody else

Have another person explain a failure using only your README and tests. If they cannot, your documentation is incomplete. If they find a wrong assumption, you've gained an engineering review.

Then publish the learning journey as a series of small commits: initial contract, first test, first failure, corrected design, verification. Do not manufacture issue activity. Keep real decisions and revisions visible.

## Where to go from here

Read the [Volume I career story](../OMNIMASTER_HANDBOOK.md) to see why these habits matter to me. Use [Volume II](../OMNIMASTER_FIELD_GUIDE.md) for deeper code-review questions. And when you want a break that still teaches something, play the [Incident Academy](../OMNIMASTER_ARCADE.md).

[← Lesson 06](06_SECURITY_AND_DELIVERY.md) · [Return to Academy](../OMNIMASTER_ACADEMY.md)
