# THE 30-DAY ENGINEERING EXPEDITION
### Thirty practical missions to learn systems thinking, data pipelines, applications, AI and release engineering

**Designed by Cayelaem Jantjies as a self-study path; no qualification, paid account or professional experience is implied.**

[Academy](OMNIMASTER_ACADEMY.md) · [Volume V](OMNIMASTER_BUILD_WITH_ME.md) · [Interactive study room](interactive/index.html) · [The person behind the methods](personal/02_WHY_I_THINK_IN_SYSTEMS.md)

---

## The promise

This is not thirty days of motivational quotes. Each day ends with **one inspectable artifact and one test of understanding**. If the exercise takes longer than a day, take longer. Progress is not a race.

Use Python 3.12+, SQLite, Git and a code editor. Later lessons optionally use React/Node.js and containers, but the core path is locally reproducible and uses fictional data.

### The journal template

~~~text
DAY:
Business question:
What I predicted:
Smallest experiment:
Result and evidence:
What failed:
What changed:
What I still cannot claim:
Commit or artifact link:
~~~

## Week 1 | Understand source truth

| Day | Mission | Deliverable | Pass criterion |
|---:|---|---|---|
| **01** | Explain the customer/business problem before picking a tool | One-page problem and audience statement | Another person can explain the intended outcome |
| **02** | Create fictional organisations, accounts and events | Versioned synthetic dataset | No real data, keys documented |
| **03** | State the grain and unique keys of each entity | Source contract table | Each row has one unambiguous meaning |
| **04** | Write first SQL create/insert/select statements | Runnable schema script | Clean setup reproduces expected rows |
| **05** | Create a one-to-many join that duplicates a financial measure | Failing demonstration and corrected query | Expected totals reconcile after correction |
| **06** | Compare inclusive and exclusive date boundaries | Temporal test table | A boundary record appears in the intended period |
| **07** | Turn the week's errors into a regression suite | At least five tests and journal notes | Tests catch deliberate duplicate/invalid input |

**Checkpoint:** you can defend your schema, business grain and metric definition without leaning on a dashboard visual.

Read: [SQL modelling lesson](academy/02_SQL_AND_MODELLING.md) · [Query-plan lab](../projects/sql-query-plans/).

## Week 2 | Engineer reliable movement

| Day | Mission | Deliverable | Pass criterion |
|---:|---|---|---|
| **08** | Define an event ID, source position and operation | Event contract | Create, update and delete represented |
| **09** | Write source validation | Invalid-input cases | Malformed IDs, amounts and timestamps rejected |
| **10** | Store events separately from current state | Bronze + Silver design | Raw evidence retained and current view correct |
| **11** | Implement idempotent replay | Duplicate event test | Same input twice does not double-count |
| **12** | Introduce same-version conflict and stale arrival | Reconciliation note | Conflicts reject; stale events do not overwrite newer state |
| **13** | Make one batch fail on a later bad record | Rollback test | Earlier writes in that batch are not committed |
| **14** | Rebuild current state from an event log | Deterministic comparison | Corrupted projection is detected |

**Checkpoint:** you can explain why a green batch isn't evidence of correct source-change capture and what a real checkpoint must guarantee.

Run: [Data-to-Decision capstone](../projects/data-to-decision-platform/) · [CDC replay lab](../projects/cdc-replay-lab/).

## Week 3 | Deliver a user-facing system

| Day | Mission | Deliverable | Pass criterion |
|---:|---|---|---|
| **15** | Define one useful business metric | Metric contract | Population, grain, time and exclusions specified |
| **16** | Create a curated query | Gold SQL or Python aggregate | Matches reconciled source state |
| **17** | Define API request/response and errors | OpenAPI-style outline or Markdown contract | Clear success, invalid input and denial behaviour |
| **18** | Sketch the permission boundary | Identity/tenant/role diagram | No claim that client-side button hiding is security |
| **19** | Build one small CLI or browser view | Usable display of fictional results | Correct labels and documented freshness |
| **20** | Add accessibility/error/empty states | UI or documented test case | Keyboard and readable failure paths checked |
| **21** | Conduct a skeptical peer/self-review | Written design critique | At least three risks and specific tests captured |

**Checkpoint:** the person using your output knows what the number means, how fresh it is and what they are authorised to do.

Study: [Full-stack lesson](academy/04_BUILD_APPLICATIONS.md) · [Metrics chapter](build-with-me/04_FROM_METRICS_TO_USERS.md).

## Week 4 | Add intelligence and release discipline

| Day | Mission | Deliverable | Pass criterion |
|---:|---|---|---|
| **22** | Find one task where AI could help, and one where it should not decide | AI use-case note | Deterministic and human decision boundaries explicit |
| **23** | Build an offline structured answer validator | Source-ID and quote tests | Fabricated evidence rejected |
| **24** | Create an eight-case evaluation set | Test matrix with expected outcomes | Wrong answers, unknowns and failure cases included |
| **25** | Simulate AI provider timeout or no-response | Controlled fallback | System makes no unsupported consequential decision |
| **26** | Identify three application abuse paths | Threat model | Cross-tenant, input and privilege cases included |
| **27** | Write automated checks for your project | Test command and CI plan | Clean run fails on a deliberately broken invariant |
| **28** | Rehearse backup or state rebuild and define rollback | Recovery document | Restore path and residual risks visible |

**Checkpoint:** you understand the difference between a useful demonstration and a safely operated service.

Study: [Applied AI lesson](academy/05_APPLIED_AI.md) · [Release lesson](academy/06_SECURITY_AND_DELIVERY.md) · [AI evaluation lab](../projects/ai-output-evaluation/).

## Days 29–30 | Publish your own textbook chapter

| Day | Mission | Deliverable | Pass criterion |
|---:|---|---|---|
| **29** | Write your architecture decision record | Context, options, choice, tests, risks and rollback | A reviewer can challenge it without extra meetings |
| **30** | Publish your synthetic capstone and teach someone its limits | README, setup, tests, screenshots if helpful, failure diary | Another person runs it and can explain an invariant |

**Final outcome:** a clear repository showing what you built, why you built it, how it can fail and what you still need to learn.

## The three skill badges you can actually earn

These are **personal study milestones**, not official GitHub badges or professional certifications.

**Source Detective:** you can explain grain, identity, temporal boundaries and double-counting.

**Systems Builder:** you can demonstrate replay, atomic writes, bounded scope and a useful consumer metric.

**Evidence Guardian:** you can show negative tests, clear AI boundaries, release gaps and a reproducible README.

## When you get stuck

Follow the routine I use:

1. Reduce the problem to the smallest failing input.
2. Write expected versus actual behaviour.
3. Test one hypothesis at a time.
4. Read the actual source error and inspect the data.
5. If you don't know a tool, learn that one concept rather than replacing the whole stack.
6. Ask another engineer to challenge the evidence.
7. Record the failure and the change in thinking.

A finished day is one with **an honest result**, not necessarily a green result.

[Go to Volume V](OMNIMASTER_BUILD_WITH_ME.md) · [Play the offline Incident Academy](../projects/omnimaster-incident-academy/) · [Launch the study room](interactive/index.html)
