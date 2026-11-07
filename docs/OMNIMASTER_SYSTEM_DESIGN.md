# OMNIMASTER · System design and delivery playbook
**Cayelaem Jantjies · November 2026**

[← GitHub profile](../README.md) · [Mission dossiers](OMNIMASTER_MISSION_DOSSIERS.md) · [Engineering field notes](ENGINEERING_FIELD_NOTES.md) · [OmniMaster live experience](https://omnimaster-portfolio.onrender.com)

> These are patterns drawn from my professional and independent engineering work. They are explanatory architecture notes, not a promise that every pattern has been implemented in every repository.

## 1. System thinking: from problem to operational software

I see a data platform and an application as connected parts of one delivery system. Data quality, model semantics, interface design, permissions, observability and rollback are different faces of the same problem: making the result useful, correct, safe and maintainable.

The simplest useful architecture often has four boundaries:

1. **Collect:** identify the real event and contract at the source.
2. **Trust:** transform, model and validate the data in the right compute layer.
3. **Deliver:** expose metrics, workflows or intelligence through well-defined APIs and interfaces.
4. **Operate:** test, observe, secure, recover and maintain the system.

The boundaries matter more than whether the implementation uses a cloud warehouse, SQL server, managed Postgres, a TypeScript service or Power BI. Those choices depend on source behaviour, expected load, team size, cost and risk.

## 2. Decide what the data represents before selecting the pipeline

### Grain and identity

For each dataset, I want to know:

- What single business event or state does one row represent?
- Which fields reliably identify that row?
- Is it mutable, append-only, or a snapshot that can be restated?
- What is the effective date versus the arrival or processing date?
- Which values are measurements, derived metrics, or reference attributes?
- What does a delete mean for downstream history?
- Are joins one-to-one, many-to-one, many-to-many, or time dependent?

**Example from manufacturing:** a delivery manifest line, schedule record and driver assignment should not be joined without testing their effective keys and cardinality. The wrong join can produce convincing but inflated totals.

**Example from banking:** a report segmented by market needs historically correct market membership, a clear data scope and user-level entitlements. A global metric can be fast but wrong for a local user.

### The contract should be explicit

Source contracts ought to describe field definitions, business units, keys, valid nulls, refresh expectations, version changes and failure behaviour. They should be readable by downstream engineers, analysts and the operational team.

I prefer contract tests that catch meaningful shape or semantic changes early, without putting the same contradictory rules into five application services.

## 3. CDC and near-real-time: define the claim before building it

In current experimentation, I am exploring SQL/MySQL source changes and reporting views to simulate production-like CDC behaviour. The key architectural distinction is between:

- A **snapshot refresh**, which periodically recomputes state.
- **Incremental polling**, which reads changes after a tracked point.
- **Change-data capture**, which represents inserts, updates and deletes as a durable change stream or log.
- A **derived reporting projection**, which maintains a useful consumer-facing state from source events or updates.

These patterns have different operational guarantees. An updating dashboard is not proof that the entire pipeline is event-driven.

### Questions I would ask in design review

| Concern | Failure to protect against | Evidence needed |
|:--|:--|:--|
| Timestamp precision | Two writes share a timestamp; one is missed. | Repeated-update and same-timestamp tests |
| Nullable watermarks | Rows with null update times never arrive. | Explicit null handling and baseline snapshot |
| Deletes | Old data remains visible indefinitely. | Tombstone or reconciliation plan |
| Replays | Retried batches duplicate counts or side effects. | Idempotent upsert/event handling |
| Out-of-order events | Stale updates overwrite later truth. | Ordering/version rules |
| Load spikes | Reporting queries affect transactional throughput. | Query plans, indexes and load metrics |
| Schema evolution | Dynamic fields or missing columns silently break consumers. | Contract checks, versioning and migration tests |
| Failure recovery | Consumer cannot resume after outage. | Checkpoint, retry and alert procedures |

### Where should transformation run?

A database view or materialised projection can be elegant when it keeps logic close to the data, but it is not free. I compare database CPU, contention, caching, tenancy, permissions, freshness and deployability with the cost of another service or analytical store.

**Preferred decision logic:** use the simplest layer that meets correctness, isolation, latency and operational requirements. Reject elaborate architecture when a well-modelled read view is enough; reject a cheap shortcut when it cannot preserve update and recovery semantics.

## 4. Microsoft Fabric, SQL and Power BI: the semantic layer is a product

A dashboard is a consumer of a data model. Performance improvements should not silently alter the business definition.

### Typical analytical flow

- Operational source extraction and staging.
- Standardised types, effective dates and meaningful dimensions.
- Fact/dimension modelling at declared grains.
- Semantic definitions: measures, filter behaviour, period logic and user access.
- Reporting, drill-through and distribution.
- Refresh monitoring, reconciliation and change management.

I have delivered work using SQL Server/T-SQL, Microsoft Fabric, Power BI, DAX, Power Query and Power Automate. When using lakehouse patterns, the bronze/silver/gold distinction is useful **only when its contracts and ownership are clear**:

- **Bronze:** source preservation and provenance.
- **Silver:** cleaned, conformed and validated data.
- **Gold:** consumer-ready business models and aggregated views.

This is a conceptual pattern, not a claim that every historical project used an identical named medallion implementation.

### Performance checks

I investigate query plans, model cardinality, relationship direction, unnecessary bi-directional filters, high-cardinality columns, DAX evaluation costs and repeated calculations. I also compare response times **with representative filters and access rules**, because a benchmark on an unrestricted subset can be misleading.

### Historical and role semantics

A row-level security implementation must be exercised with permitted and forbidden market/tenant combinations. Historical comparisons must define which time key is authoritative; month-end and cohort snapshots cannot always be summed as flows.

## 5. Full-stack architecture: the API is not just a thin wire

The value of a product comes from preserving intent across the whole chain:

**User action → validated request → permission check → domain state transition → transaction → response → audit/notification → reporting update.**

In TypeScript/React/Node products, I consider:

- **Authentication:** establish identity, session state and re-verification rules.
- **Authorisation:** verify which role or tenant can operate on a specific record.
- **Validation:** define business constraints centrally and validate at trust boundaries.
- **Transactions:** avoid partial writes that turn a completed screen into inconsistent data.
- **Idempotency:** protect retries, email sends and imports from duplicate side effects.
- **Background work:** use queues/jobs for slow operations, with statuses and retries.
- **Observability:** structured errors, request context, safe metrics and audit events.
- **UI behaviour:** accessible feedback, responsive navigation, correct loading/error states and mobile testing.

### Example: a document-assessment feature

An education product should validate file type and ownership, store content according to privacy rules, process it within limits, generate questions with source references and show review status. The student sees feedback; the educator retains authority over high-stakes decisions.

### Example: a financial journal

A financial system should use exact decimals, balanced debits and credits, database transactions, immutable journal semantics and permissions. AI explanations must not directly mutate the ledger.

## 6. Security: design the denial paths

Security testing is not only proving a happy path. I look for:

| Threat boundary | Useful tests or controls |
|:--|:--|
| Unauthenticated or stale session | Refuse protected actions and expire sensitive sessions correctly. |
| Wrong organisation | Verify that tenant A cannot read or change tenant B's records. |
| Wrong role | Check forbidden administrative and destructive operations. |
| Admin MFA | Challenge step-up and recovery flows, including new and existing accounts. |
| Hostile input | Validate headers, URLs, file uploads, query parameters and output encoding. |
| Secrets | Ensure scans and logs never expose credential material. |
| Third-party integrations | Verify signatures, rate limits, timeouts, backoff and input contracts. |
| Data migration | Compare schema, access policies, protected functions, behaviour and recoverability. |
| AI integration | Limit prompts, isolate data, evaluate outputs and restrict tool actions. |

Relevant engineering work includes TOTP/WebAuthn integration, secure administrative routes, local test isolation, Semgrep/Trivy/Gitleaks usage and controlled review of AI-assisted security analysis. **None of these single measures certifies the full system as secure.**

## 7. Testing and CI: prove what was actually run

My preferred test pyramid is not dogmatic about test counts. It aims for the failure modes that matter:

1. **Static gates:** lint, types, format, dependency and secret checks.
2. **Unit/contract checks:** domain logic, parsing, data validation and predictable outputs.
3. **Integration tests:** a real application route against a disposable test database.
4. **Browser tests:** critical user journeys, responsive layouts and access boundaries.
5. **Migration/recovery drills:** schema changes, backups, rollback, and safe cutover checks.
6. **Production observability:** separate verification of health and release behaviour.

I have been developing Docker-based local test suites with disposable PostgreSQL, synthetic records and a self-hosted runner. This helps avoid unpredictable hosted runner costs and protects production credentials, but a local test result still needs correct branch/version mapping to be useful.

### Why I avoid overstated release status

A staged migration may have schema parity but lack MFA route enforcement on the deployed release branch. A feature may be green in tests but blocked in a production configuration. A deploy can be *live* while an integration is still disabled. I report these as separate facts.

## 8. Applied AI: put the guardrails around the workflow

The interesting question is not “which model?” but “what should the system let a model decide, and how do we know the answer is useful?”

### Product use cases

**Education:** source-grounded revision questions, written assessment support, feedback and learner insights.

**HR:** evidence-linked recommendations, drafting assistance, and interview/assessment summaries subject to human review.

**Finance:** read-only explanation of derived reports; deterministic accounting remains outside model control.

**Operations:** summarisation, troubleshooting assistance and workflow automation with bounded access.

### Evaluation dimensions

- Source grounding and correctness.
- Fairness and human override where decisions affect people.
- Failure and fallback behaviour.
- Prompt and input limits, privacy and retention.
- Cost, latency and provider dependency.
- Security against prompt injection and inappropriate data access.

I explore Groq and Hugging Face integration paths where supported by the relevant repositories; model compatibility and production controls must be tested, not assumed.

## 9. Mobile, desktop and multi-device parity

Native and responsive are not synonyms. A credible cross-platform rollout needs:

- An inventory of user journeys and capabilities that must match.
- Platform-appropriate navigation, offline behaviour and permissions.
- Secure account/session lifecycle per device.
- Accessibility, text scaling and device testing.
- App signing, distribution, upgrades and recovery procedures.
- A known implementation status per feature, not only a design mock-up.

My established delivery is web/full-stack and analytics; Android/Kotlin, iOS and Windows work are active development directions, with feature parity and release readiness still under validation.

## 10. Professional delivery: the business problem stays visible

When presenting a technical solution, I explain:

**Problem:** what was failing or inefficient?  
**Constraints:** scale, privacy, source quality, team, time and cost.  
**Decision:** what did I choose, and what alternatives did I reject?  
**Verification:** how did I test assumptions and implementation?  
**Outcome:** what did users gain, and how is it measured?  
**Residual risk:** what is not yet proven or deployed?

This structure makes documentation more honest and makes projects easier to support after the first release.

### Further reading

- [OmniMaster GitHub overview](../README.md)
- [Engineering mission dossiers](OMNIMASTER_MISSION_DOSSIERS.md)
- [Professional client case studies](CLIENT_CASE_STUDIES.md)
- [Technical capability and evidence matrix](TECHNICAL_SKILLS.md)
- [Engineering field notes](ENGINEERING_FIELD_NOTES.md)
