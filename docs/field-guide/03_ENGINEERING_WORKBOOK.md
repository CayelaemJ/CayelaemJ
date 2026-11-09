# Field Guide 03 | Engineering workbook

[← Debugging casebook](02_DEBUGGING_CASEBOOK.md) · [Volume II](../OMNIMASTER_FIELD_GUIDE.md) · [Next: Role and evidence map →](04_ROLE_AND_EVIDENCE_MAP.md)

This workbook turns the ideas in my profile into concrete problem-solving exercises. They are designed for engineering reviewers, interview panels and curious developers. **Inputs and sample numbers are fictional.** I include my reasoning, not hidden answer keys or claims that these exact questions came from interviews.

## How to use this chapter

Try each exercise before reading the discussion. Write down the business invariant, the failure mode, the smallest safe experiment and the evidence needed to consider the change done.

| Exercise | Skill | Estimated work |
|---|---|---|
| **A. The duplicate ledger amount** | Relational grain and BI semantics | Small SQL or paper exercise |
| **B. The missing CDC update** | Watermarks, ordering and replay | Design + code |
| **C. The unsafe bulk administrator endpoint** | RBAC, MFA and tenant isolation | API threat model |
| **D. The confident-but-unsupported AI answer** | Grounding, evaluation and human review | Python negative test |
| **E. The cutover that passed staging** | Release engineering and migrations | Deployment decision |
| **F. The query that got slower after indexing** | Query plans and selectivity | SQL profiling |
| **G. The incident briefing** | Technical communication | Two short explanations |

---

## Exercise A. The duplicate ledger amount

**Scenario:** An order table contains one invoice for 5,000 units of currency. The dispatch table contains two separate deliveries for that invoice. The QA table contains three inspection records. A report joins all three tables and sums invoice amounts.

**Questions**

1. What aggregate does the naive join produce?
2. Why is applying DISTINCT to the final invoice amount not a general solution?
3. What grain should each fact preserve?
4. How would you protect the fix against a new fourth QA record?

<details>
<summary>My worked reasoning</summary>

A direct two-child one-to-many join can produce 2 × 3 = **6 joined rows**, repeating the 5,000 invoice amount and reporting **30,000**. DISTINCT happens to hide some duplicates but breaks as soon as multiple legitimate invoices share the same value.

I would aggregate invoice value at invoice grain, model dispatch counts at delivery grain and QA counts at inspection grain, then relate them through stable identifiers and explicit dimensions. I would test the global amount, a filtered customer subtotal and a case with an extra QA row. The amount must remain 5,000.

A key requirement is that the invoice grain and its measure are defined **before** any join is optimised.

</details>

**Related history:** [Enterprise and manufacturing analytics](../CLIENT_CASE_STUDIES.md). **Runnable adjacent example:** [SQL query-plan lab](../../projects/sql-query-plans/).

## Exercise B. The missing CDC update

**Scenario:** The source stores an UPDATED_AT timestamp to second precision. Two updates to one account occur within that second. A loader advances its watermark to that timestamp and fetches rows with UPDATED_AT greater than the last value.

**Questions**

1. Which update can disappear from the consumer's history?
2. Will switching to greater-than-or-equal alone guarantee correctness?
3. How should DELETE operations be represented?
4. How do we make the checkpoint and destination transaction agree?

<details>
<summary>My worked reasoning</summary>

A strict greater-than predicate can skip writes sharing the last watermark. Greater-than-or-equal helps avoid missing a row but can replay rows, and it still cannot reconstruct two successive states or physical deletes from a final-state table.

I would first confirm the actual business requirement. For latest-state snapshots, a composite watermark such as timestamp plus stable key may work if the source exposes all needed changes and updates deterministically. For lossless event history and deletes, a genuine change log, transaction/binlog CDC or durable source event publishing is more suitable. I would combine an idempotent sink with a checkpoint that only advances after committed processing.

I would test two changes in one second, restart mid-batch, delete, out-of-order event and replay.

</details>

**Public reference:** [CDC Replay Lab](../../projects/cdc-replay-lab/) · [Fixer source-adapter issue](https://github.com/CayelaemJ/NewChanges/issues/241).

## Exercise C. The unsafe bulk administrator endpoint

**Scenario:** The React UI hides “bulk export” from ordinary employees. An employee discovers the API endpoint directly and submits a tenant ID belonging to another organisation.

**Questions**

1. Which checks must run on the server?
2. Is a logged-in session enough?
3. Where does MFA fit for sensitive actions?
4. How do you test denial without accidentally exposing other tenants' existence?

<details>
<summary>My worked reasoning</summary>

Front-end visibility is not authorisation. The API must authenticate the user, resolve their **authorised tenant scope from the server-side identity**, check operation permission and enforce data access constraints. Sensitive administrative actions may require current step-up proof and an auditable record.

I would test ordinary user requests, missing MFA, wrong role, cross-tenant parameters, revoked sessions, bulk pagination and alternate API paths. Negative responses must not return another tenant's rows, identifiers or counts. A database least-privileged role adds defense in depth; it does not replace a correct service permission model.

I would not call the control production-ready merely because a unit mock passes.

</details>

**Public reference:** [Fixer security workstream](https://github.com/CayelaemJ/NewChanges/pull/219) · [Security handbook](../handbook/07_SECURITY_AND_DELIVERY.md).

## Exercise D. The confident-but-unsupported AI answer

**Scenario:** A model is asked whether a fictional learning resource permits unlimited retakes. The approved document says **two retakes**, but the model answers “unlimited retakes” with a high claimed confidence.

**Questions**

1. Does a confidence score validate truth?
2. What evidence can an output validator compare?
3. Should a generated answer be allowed to update a learner's official grade?
4. What should happen when the provider is unavailable?

<details>
<summary>My worked reasoning</summary>

A high self-reported confidence score is not calibration. I would require an approved source identifier, source-grounded evidence, validated response shape and explicit handling for unknown or contradictory documents. An exact quotation validator can reject fabricated extracts, but does not establish that the source itself is correct or that a paraphrase is semantically faithful.

For grading or progression, I would use a controlled rubric, deterministic score limits, educator review, transparent correction and privacy-aware records. A provider failure should produce a safe fallback or an explicit **no-decision** state, not a fabricated grade.

The runnable demo intentionally restricts answers to extractive text because that is a verifiable toy contract.

</details>

**Run a negative test:** [Offline AI Output Evaluation](../../projects/ai-output-evaluation/). **Related product:** [CABO Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub).

## Exercise E. The cutover that passed staging

**Scenario:** PostgreSQL schema restore and unit tests pass. The target contains a one-day-old snapshot, audit entries differ, and the source is still receiving live writes. The team wants to switch the primary app to the new database tonight.

**Questions**

1. Is a healthy connection a sufficient release gate?
2. What must happen to the old writer?
3. Which validation is missing?
4. What would make a rollback possible?

<details>
<summary>My worked reasoning</summary>

No. A connection proves reachability and perhaps permissions. It cannot prove data completeness, final replication, identity correctness, tenant security or cutover safety.

I would require a documented final-sync method, explicit old-writer fencing, data parity at a stable point, restricted-role privilege checks, application auth/MFA and write-path tests, backup/restore evidence, owner approval and a reversible rollout plan.

If those conditions cannot be met, the release should remain blocked. An attractive staging screenshot is not a substitute.

</details>

**Public reference:** [Guarded migration preparation](https://github.com/CayelaemJ/NewChanges/pull/225) · [Release principles](../handbook/07_SECURITY_AND_DELIVERY.md).

## Exercise F. The query that got slower after indexing

**Scenario:** A table stores tenant, status, date and amount. A developer adds a composite index on (tenant, status, date), but a dashboard query filters by a date-expression function and still performs slowly.

**Questions**

1. Which fields can the index still help?
2. What happens if the filter uses a direct inclusive/exclusive date range?
3. How can the test avoid confusing query correctness with performance?
4. Why might a database still choose a scan?

<details>
<summary>My worked reasoning</summary>

The equality prefix (tenant, status) may remain usable. Applying a function to the date column can prevent efficient use of the date range part. A direct predicate such as **date >= start and date < end** often gives the optimiser a better indexed range.

I would compare EXPLAIN output and verify identical aggregate results. On a real engine, I would also examine distribution, statistics, selectivity, table size, index maintenance and concurrency. The presence of an index does not require the optimiser to use it.

</details>

**Reproduce:** [SQL Query Plans Lab](../../projects/sql-query-plans/).

## Exercise G. Explain one issue twice

**Scenario:** A financial dashboard is missing updates because the underlying source timestamp cannot distinguish rapid consecutive changes.

Write two explanations:

- **For a technical reviewer:** describe timestamp precision, checkpoint/watermark risks, replay/deletion semantics and testing options.
- **For a business owner:** describe which numbers may be stale, how you will identify affected records and why the team should not present the dashboard as real time until checks are complete.

<details>
<summary>How I would communicate it</summary>

**Technical:** “The current incremental reader uses a second-resolution updated timestamp. Multiple events can share the checkpoint value, and a strict greater-than query may miss them. It also does not represent physical deletes. We need a verified source-change mechanism or a bounded reconciliation strategy with duplicate-safe replay. I'll prove this with a synthetic multiple-write test before changing the reporting freshness claim.”

**Business:** “Some changes made close together may not be reflected in the dashboard. We're testing the source and comparing it with the displayed records. Until the gap is fixed and measured, the figures should be treated as periodically updated rather than live.”

</details>

## A reviewer can use this rubric

| Criterion | Weak answer | Strong answer |
|---|---|---|
| **Business understanding** | Lists technologies | Defines the real event, audience and decision |
| **Data correctness** | Assumes joins are safe | States grain, keys and reconciliation invariants |
| **Failure handling** | “Retry until it works” | Covers idempotency, ordering, limits and rollback |
| **Security** | Hides controls in the UI | Enforces role, tenant and purpose server-side |
| **AI quality** | Trusts model confidence | Grounds evidence, validates output, requires human control |
| **Testing** | Reports “tests pass” | Names exact cases, commit, environment and missing proof |
| **Communication** | Hides uncertainty | States what is known, unknown and safe to release |

The aim is not to memorise these answers. It's to make the assumptions visible enough that a colleague can challenge them.

[← Casebook](02_DEBUGGING_CASEBOOK.md) · [Next: Role and evidence map →](04_ROLE_AND_EVIDENCE_MAP.md)
