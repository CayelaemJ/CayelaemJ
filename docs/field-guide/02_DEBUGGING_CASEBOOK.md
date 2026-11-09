# Field Guide 02 | The debugging casebook

[← Architecture atlas](01_ARCHITECTURE_ATLAS.md) · [Volume II](../OMNIMASTER_FIELD_GUIDE.md) · [Next: Engineering workbook →](03_ENGINEERING_WORKBOOK.md)

A debugger's first obligation is to separate **what was observed** from **what might have caused it**. I want these cases to show my reasoning habits, not pretend that every diagnostic thought was a resolved production incident.

The cases below are derived from public PR reviews, engineering experiments and professional practice. The Fixer/CABO code-review cases identify actual open work; the manufacturing/analytics cases are **representative examples informed by past work**, not disclosures of protected client incidents.

## Case 01. A CDC loop can report success while making no progress

**Source:** [The Fixer PR #237](https://github.com/CayelaemJ/NewChanges/pull/237) and [CDC adapter issue #241](https://github.com/CayelaemJ/NewChanges/issues/241).  
**Evidence class:** Public code-review finding and an unresolved engineering task, not a completed production correction.

### Symptom

In the synthetic CDC runner, a batch limit is applied while accumulating row events. If a single row event exceeds the configured limit, the loop can stop rather than process the event. The run may still be recorded as a successful batch.

### Why I care

This is a subtle kind of failure: monitoring sees green, but the source checkpoint and destination state may stop progressing. A refreshed dashboard can look “live” while the underlying data remains stale.

### How I would diagnose it

1. Record the exact source event position and configured batch maximum.
2. Create a synthetic transaction whose row count is larger than that maximum.
3. Run the reader twice and compare checkpoint, processed-row count and job outcome.
4. Confirm whether the engine reports a retryable blocked state, progresses safely or silently repeats the same stalled position.
5. Check how checkpoint commit interacts with destination commit.

### Design alternatives

| Option | Benefit | Cost or risk |
|---|---|---|
| Fail closed on oversized event | Impossible to claim success while stalled | Requires operator response or controlled retry |
| Process oversized atomic event with explicit exception | Can preserve progress | Must respect transaction/memory limits |
| Split event carefully | Controls memory | Must preserve source transaction atomicity and ordering |

**My preferred invariant:** no successful CDC run without either real progress or an explicitly valid empty-source condition. The exact implementation needs transaction semantics reviewed in the target adapter.

**Proof needed before closure:** oversized-event regression, repeat polling, error status, retry and checkpoint consistency.

---

## Case 02. A year-end progression decision can target the wrong academic year

**Source:** [Learning Hub PR #160](https://github.com/CayelaemJ/Training-and-Development-Hub/pull/160) and [tracking issue #163](https://github.com/CayelaemJ/Training-and-Development-Hub/issues/163).  
**Evidence class:** Public cross-platform code-review finding. Still open until fixed and regression-tested.

### Symptom

An administrator loads learner progression candidates for academic year A, then changes the editable year control to B without forcing the candidates to refresh. A submission can use B to calculate the target year while still operating on candidate data that was reviewed for A.

### Why this matters

A UI state mismatch becomes a **data-integrity error** when submitted identifiers and derived fields have different temporal meaning.

### Investigation

- Trace where the year value lives in Android and iOS state.
- Trace the request parameter used to fetch candidates.
- Trace the value used for target-year derivation on submit.
- Change the year *after* a successful fetch and before confirmation.
- Verify whether the UI invalidates its selection or clearly binds it to the reviewed year.

### A stronger design

Treat each candidate set as a versioned decision context: **reviewed year + source request + selected records**. If the user changes the year, invalidate candidate state and require a refetch. On submit, bind the request to the reviewed context, and reject stale decisions server-side.

**Regression matrix:** Android, iOS, empty selection, year change, loading state, response ordering and server-side stale-context rejection.

---

## Case 03. The database snapshot is valid, but not a safe cutover

**Source:** [The Fixer guarded migration PR #225](https://github.com/CayelaemJ/NewChanges/pull/225) and the project's documented Aiven/Neon migration work.  
**Evidence class:** Historical test and migration-preparation record, not evidence of a completed live cutover.

### Symptom

A snapshot can have all expected tables and most correct row counts, while differences remain in an actively written audit table or in extension metadata. A schema restore passing does not mean the target is current enough for real traffic.

### Different questions that are often confused

**Schema parity:** Do tables, keys, functions, extensions, grants and migrations match?

**Data parity:** Is the target a consistent point-in-time representation of required source state?

**Security parity:** Can the application connect using restricted roles? Are there unintended privileges?

**Operational cutover readiness:** Can the old writer be fenced, final changes reconciled, and requests safely switched or rolled back?

### Investigation sequence

1. Capture a consistent source point and document any concurrent writes.
2. Compare schema, constraints, required functions and effective permissions.
3. Compare counts *and* checksums/key sets for required tables.
4. Investigate drift by table, especially append-only audit data.
5. Validate auth, MFA, tenant isolation and write functionality against a restricted target role.
6. Rehearse rollback and check which side is the sole authorised writer.

**My rule:** a successful restore proves the backup can be restored to some state. It does not prove zero data loss, current state, least privilege or a safe production switch.

---

## Case 04. “Email failed” can mean two different things

**Source:** [The Fixer security PR #233](https://github.com/CayelaemJ/NewChanges/pull/233).  
**Evidence class:** Source-remediation workstream and documented regression intent.

### Symptom

An outbound email is accepted by the transport, but persisting its audit record fails. Reporting the *whole operation* as a send failure can cause an operator to resend, producing an accidental duplicate.

### Hidden assumption

A single status field is being asked to represent two separate outcomes:

1. **Delivery request outcome:** what did the SMTP transport accept or reject?
2. **Audit persistence outcome:** did the platform save the record describing that action?

### Safer model

Represent outcomes independently, with a durable retry strategy for recording status rather than falsely telling the user the send did not happen. Where possible use idempotency keys and a transactional outbox to avoid dual-write inconsistencies.

### Tests I expect

- Transport accepts, audit succeeds.
- Transport rejects, audit attempts record the failure.
- Transport accepts, audit fails: UI does not falsely prompt resend.
- Retries do not duplicate a logically identical notification.
- Malformed addresses or header injections are denied before transport.

**Lesson:** when a workflow spans two independent systems, a single “success/fail” flag often hides the very distinction needed for safe recovery.

---

## Case 05. An apparently correct KPI can double-count industrial events

**Source context:** [Australian manufacturing and enterprise reporting case studies](../CLIENT_CASE_STUDIES.md).  
**Evidence class:** Illustrative teaching example based on the type of grain and join problems encountered in professional analytics. The fictional numbers below are not client records.

### Fictional sample

An order for **R1,000** has two dispatch rows and three quality-check rows. Joining order, dispatch and quality checks directly gives **six result rows**. Summing the order amount over those rows incorrectly yields **R6,000**.

### How I would isolate the problem

1. Establish the order table's primary grain as one row per order.
2. Check dispatch and inspection cardinalities independently.
3. Compare row counts before and after each join.
4. Choose whether to pre-aggregate child facts, model relationships or use separate fact tables.
5. Reconcile the expected R1,000 back to the source, both globally and under representative filters.
6. Measure performance **after** correctness is restored.

### Design decision

The fix is not an arbitrary DISTINCT or a visual-level filter that hides the problem. The model must reflect the business event being measured.

The accompanying [SQL Query Plans Lab](../../projects/sql-query-plans/) teaches index and predicate behaviour; it does not reproduce this specific grain example or any manufacturing data.

---

## Case 06. The best dashboard fix may be a database or API fix

**Source context:** [Engineering field notes](../ENGINEERING_FIELD_NOTES.md) and [professional client studies](../CLIENT_CASE_STUDIES.md).  
**Evidence class:** Representative diagnostic workflow.

If a page is slow, I divide the elapsed time into **source query, transformation, backend/API, browser/network and semantic calculation**. Each can fail independently.

| What I observe | Hypothesis | How I test |
|---|---|---|
| Raw query is slow | Scan, bad selectivity, missing index or costly joins | Query plan and comparable-row timing |
| Source SQL is fast but BI is slow | Model context, measure complexity or repeated transformations | Performance analyzer and controlled DAX/query comparisons |
| API slow under load | N+1 queries, missing indexes, connection pool pressure | Traces, query count, concurrency test |
| UI slow with fast API | Excess rendering, chart size, client-side transformations | Browser profiling and narrow-device tests |
| Results differ after optimisation | Semantic regression, duplicated joins or filter changes | Source reconciliation tests and snapshot comparison |

**Lesson:** instrument before redesigning. If a solution is faster but silently changes the intended figure, it failed the real test.

---

## The investigation template I use

~~~text
PROBLEM
User-visible impact:
Observed behaviour (with timestamp and environment):
What changed:
Expected invariant:

EVIDENCE
Reproducible steps:
Code/SQL/query plan:
Log/trace/test:
What is NOT known yet:

HYPOTHESES
1. ...
2. ...
3. ...

SAFE EXPERIMENTS
Disposable inputs:
Negative path:
Regression boundary:

DECISION
Smallest safe change:
Tests required:
Rollback strategy:
Residual risk:
Status: proposed / implemented / tested / deployed
~~~

The best incidents produce better contracts and tests, not just more alerts.

[← Architecture atlas](01_ARCHITECTURE_ATLAS.md) · [Next: Engineering workbook →](03_ENGINEERING_WORKBOOK.md)
