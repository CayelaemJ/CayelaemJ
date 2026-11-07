# OMNIMASTER · Engineering mission dossiers
**Cayelaem Jantjies · 7 November 2026**  
**Project architecture, business context, decisions, outcomes and evidence boundaries**

[← Return to the OmniMaster GitHub profile](../README.md) · [System design](OMNIMASTER_SYSTEM_DESIGN.md) · [Client cases](CLIENT_CASE_STUDIES.md) · [Portfolio site](https://omnimaster-portfolio.onrender.com)

> **Reading guide:** A dossier records professional experience, available source evidence, current engineering decisions and known gaps. **Implemented**, **under active development**, **pilot/staging** and **planned** are different states. Neither a repository nor a successful build proves every capability has been launched to production. Client-owned code and datasets are not reproduced.

---

## Mission 01 / The Fixer integration platform

**Public source:** [NewChanges](https://github.com/CayelaemJ/NewChanges)  
**Stack represented:** TypeScript, Fastify, Node.js, PostgreSQL/Prisma, React, Docker, MySQL integration experiments and Render/Cloudflare workstreams  
**Stage:** Existing application with active product modernisation, security hardening and guarded infrastructure migrations

### The underlying business problem

Financial-wellness and employer dashboards draw from operational sources that are often inconsistent and slow to reconcile. Data can arrive from SQL views, APIs and files. Each has its own update semantics. A reporting portal must also serve different employers and channel partners without leaking information across tenants or presenting misleading historic metrics.

### Scope of engineering

**Data contracts and ingestion.** The existing repository documents a ten-dataset source contract, import validation, reporting definitions, governance and tenant-related operations. The contract is important because the same metric may look different when captured as an event, a snapshot or a derived state. Importing records without preserving these semantics produces incorrect results.

**Application and presentation.** The application connects an established reporting dashboard, API routes, administration tools, branding/tenant experiences, reporting automation and a separate React modernisation path. UI parity needs to protect established data behaviour while making the interface easier to navigate and maintain.

**Identity and security.** Current hardening addresses stronger administrator MFA, TOTP/WebAuthn workflows, sensitive-operation step-up, recovery, consistent validation, audit clarity and isolation of synthetic test data. An observed unit test is not proof that all release routes are wired to the policy.

**Operations.** A recurring goal is disposable Docker regression testing using local test databases, self-hosted runners, documented migrations, scanning and cautious cloud cutovers. This keeps tests reproducible without granting local CI access to live data.

### Engineering decisions and trade-offs

| Decision | Why it matters | What remains to prove |
|:--|:--|:--|
| Keep a defined source contract | Data meaning stays traceable across imports, APIs and analytics. | Schema drift, nullability and real source behaviour across updates. |
| Explore database-side transforms and views | Reduces unnecessary application round trips for reporting-heavy workloads. | Query cost, contention, freshness and incremental performance. |
| Simulate CDC instead of assuming polling equals streaming | Updates, deletes, ordering and late events need explicit behaviour. | Idempotency, watermark precision, replay, lag and recovery. |
| Gate high-risk admin actions through stronger authentication | Logging in once should not authorise every sensitive operation forever. | Complete integration tests and verified deployed enforcement. |
| Keep migrations staging-first | Prevents losing data or permissions during a hurried cutover. | Parity, restores, operational monitoring and rollback rehearsal. |

### Specific lessons

1. A dashboard that renders is not necessarily accurate; source semantics and historical filters are part of correctness.
2. “More validation” is not always safer. Checks should be deterministic, consistent and placed at meaningful trust boundaries.
3. Security reports must distinguish a failed audit-write from an actual delivery failure, or administrators may repeat actions unnecessarily.
4. Boolean parsing, email input validation and authorization behaviour should be tested with malicious or malformed inputs, not just happy-path values.
5. CI evidence should explain *what ran*, on *what data* and *against which branch*.

### Evidence boundary

The repository and associated documentation show significant implementation history. Current MFA, CDC, MySQL, database migrations and Cloudflare/Render work may be on separate branches or in isolated environments. **No production cutover or full security acceptance is claimed here.**

**Review:** [Repository README](https://github.com/CayelaemJ/NewChanges) · [Architecture and project atlas](PROJECT_PORTFOLIO.md)

---

## Mission 02 / CABO Learning Hub

**Public source:** [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub)  
**Stack:** React/TypeScript, Node/Express workflows, PostgreSQL/Drizzle, AI provider integrations and mobile-platform workstreams  
**Stage:** Implemented learning/assessment functionality, pilots and ongoing connected-education architecture

### Why I am building it

Learner development is a longitudinal system problem. Marks, assessments, attendance, intervention history, school transfers and extracurricular development are often captured in disconnected systems. A richer education platform should connect meaningful learner history with responsible assistance for educators and parents.

### Documented implemented and developing scope

**Learning and assessment.** The repository describes material upload, multiple-choice practice, document-grounded written examinations, rubric-based marking, free-text assessment and explicit feedback/review markers. The exact implementation stage differs by workflow and branch.

**School and family operations.** Broader product work explores learner and educator role design, academic records, school and university registration, guardian journeys, reporting and continuity during transfers.

**National-system interoperability.** Botswana and South African school-system onboarding and migrations are strategic product directions. A genuine replacement of official mark-capture processes would require agreements, data mapping, retention rules, historical reconciliation, import sign-off and phased adoption. It must not be presented as an existing government integration.

**Multiple devices.** The direction spans responsive web, Android/Kotlin, iOS and Windows. An APK or mobile wrapper is not sufficient proof of equivalent native functionality. Accessibility, offline constraints, device testing and deployment approvals require separate evidence.

### Responsible AI architecture

| Concern | Design intention | Why it matters |
|:--|:--|:--|
| Source grounding | Generate or grade with reference to authorised learning material and rubrics. | Limits unsupported explanations and misleading assessment. |
| Human oversight | Educators review disputed or high-stakes marks. | Model outputs cannot replace accountable educational decisions. |
| Provider strategy | Consider provider selection, Groq/Hugging Face compatibility and safe fallback. | Availability, costs and latency change; interruptions should degrade safely. |
| Child data | Permissions, guardian controls, minimisation, audit trails and suitable retention. | Learning history may be sensitive and long lived. |
| Evaluation | Test answer quality, bias, partial-credit grading and consistency. | A plausible output is not necessarily a fair result. |

### Architectural tension

The platform has to support local everyday school tasks while offering district/national insight. That creates tension between multi-tenancy and administrative aggregation. A learner's personal record should be visible only to authorised parties, whereas anonymised or aggregated cohort trends might be useful for planning. Transfers, child consent, auditability and conflict resolution all require policy-aware design.

### What is not claimed

No claim of official government adoption, nationally verified data migration, completed legal certification, universal native parity or independently validated nationwide AI grading.

**Review:** [Repository](https://github.com/CayelaemJ/Training-and-Development-Hub) and its phase-delivery register.

---

## Mission 03 / Australian manufacturing intelligence

**Engagement:** Bitberry / Bestbar, remote delivery during 2026  
**Stack:** SQL Server/T-SQL, SSIS, SQL Server Agent, Power BI/DAX, Fabric, Power Query and Power Automate  
**Stage:** Historic professional delivery; proprietary source systems

### Business problem

Manufacturing operations need to understand scheduler efficiency, production, scrap, stock, workforce effort and dispatch outcomes. Operational data is rarely built with analytics-friendly grains and consistent keys. One misinterpreted relation can multiply cost and tonnage across a dashboard.

### Work performed

- SQL extraction and modelling across production, logistics, payroll/rostering and ERP sources.
- A scheduler reporting architecture documented as covering eight states, fifteen temporary tables, 35 DAX measures and eleven model relationships.
- Cutting-production and mesh/rebar reporting, scrap calculations, stock movement, forecasts, workforce output, manifest/delivery analysis and automated report distribution.
- Automation for mill-certificate emails and attachments and regular operational exports.
- Investigation of deadlocks, schema and column-name drift, malformed records and cascading refresh failures.

### Why grain mattered

A **schedule** describes a planned activity. A **manifest line** describes a delivery item. A **driver or truck assignment** describes an operational relationship at a point in time. Joining these without testing cardinality can multiply or omit facts.

My preference is to:

1. Write down the business event and the unit being counted.
2. Establish each table's grain and keys.
3. Verify the desired time and state context.
4. Test join cardinality and duplicated totals on representative samples.
5. Build an explicit analytical model and DAX measures.
6. Reconcile totals to operational source examples before publishing the visuals.

### Examples of failure-mode investigation

**SQL deadlocks.** A dataflow failure should be traced through the database workload and dependencies, not masked by repeated refresh attempts.

**Dynamic pivot drift.** Pivot outputs can change columns when an input shape evolves. The contract and downstream model must be designed for that instability.

**Duration semantics.** A numeric field called "hours" may actually contain minutes or an encoded duration. Units must be verified with source examples.

**State/date modelling.** A measure grouped by an operational state is only meaningful if relationships preserve historical attribution rather than using an unrelated current mapping.

### Evidence boundary

The figures and architecture elements above come from earlier CV and engagement documentation. They are not a public client benchmark, and the source code is not published.

**Review:** [Australian manufacturing case study](CLIENT_CASE_STUDIES.md#1-bitberry--bestbar--australia-data-platform-manufacturing-and-delivery-analytics)

---

## Mission 04 / Banking, capital markets, FMCG and media analytics

**Engagement pattern:** IQbusiness client delivery and related BI roles, primarily 2024–2025  
**Stack:** Power BI, DAX, SQL, Power Query, Fabric, Power Automate, SharePoint and related client systems  
**Stage:** Historic professional delivery

### Banking: trust boundaries and regional analytics

Banking analytics requires more than consistent visuals. Market users have different entitlements, products and business semantics. Previous work included a documented 18-dashboard portfolio across South Africa, Namibia, Botswana and Zambia, plus dynamic calculations, row-level security and performance tuning. A reported 40% reduction in load times reflects a specific historical delivery outcome.

**Core design question:** Which users can see which markets and historical periods without creating a new dataset for every team?

### FMCG and brand research: scale and correctness

Brand, distribution, outlet and market performance reporting can involve hundreds of millions of survey records. I worked with a reported 270M+ survey dataset in a Diageo engagement. The challenge was reliable data cleaning, efficient modelling, meaningful segment filters and reporting that stakeholders could understand.

**Core design question:** Are campaign and market comparisons computed from compatible samples and business definitions?

### Capital markets: automate the repetitive layer

At JSE, Jira extraction, service-level dashboards and automated reporting reduced recurring manual preparation in a documented engagement by up to 70%.

**Core design question:** Which recurring transformations can be made repeatable while retaining auditability and exception handling?

### Media and broadcasting: integrate service signals

MultiChoice-related experience included customer experience, NPS, repeat contacts, service processes, sentiment signals and earlier broadcast operations reporting. Different sources can use different keys and response-time definitions, so aggregation must be explicit.

### Core lessons

- A DAX performance improvement is only successful if the measures remain mathematically and semantically correct.
- Row-level security needs role and market tests with representative access expectations.
- Business definitions should be versioned, not hidden inside dozens of hard-to-review report measures.
- A management dashboard must explain its denominator, filtering window, refresh cadence and exclusions.

**Review:** [Professional client case studies](CLIENT_CASE_STUDIES.md)

---

## Mission 05 / CABO Human Capital

**Public source:** [HR-Software](https://github.com/CayelaemJ/HR-Software)  
**Stack:** React, TypeScript, Express, PostgreSQL, audit/event workflows  
**Stage:** Active development and synthetic demonstration; not approved for live personal candidate records

### Problem and design

Recruitment and people operations are full of decisions that need explanation and review. A candidate scoring widget that cannot show its evidence may be worse than a manual process. The product explores recruitment, application stages, employee development and human-governed evaluation.

**Engineering areas:**
- Tenant-aware organisation, recruiter, candidate and employee records.
- Evidence provenance for qualifications, skills, interviews and scorecards.
- Human review, reasons for decisions and audit history.
- Candidate document safeguards, retention and restricted access.
- AI-assisted drafting/analysis with human ownership rather than automatic selection.
- Careful separation of candidate data, synthetic demonstrations and payroll handoff experiments.

### Risk and ethics

Model ranking cannot be assumed fair simply because it produces a score. The design must test disparate outcomes, incomplete evidence, explainability, consent, retention and appeals. Responsible AI also means the system is usable when the model is unavailable.

### Evidence boundary

This is not a live applicant processing approval, employment-law certification or a replacement for regulated payroll systems.

**Review:** [Public repository and its stated limitations](https://github.com/CayelaemJ/HR-Software)

---

## Mission 06 / CABO Financial Intelligence

**Public source:** [Accounting-Audit-And-Analytics-Software](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software)  
**Stack:** Next.js, TypeScript, PostgreSQL, tenant access and staged migrations  
**Stage:** Gated staging, not production-certified accounting/audit software

### The problem

Financial workflows must preserve exact balances, transaction provenance, approval and period rules. A beautiful chart that depends on incorrect posting semantics is not a financial system.

### Engineering choices

- **Double-entry ledger:** exact-decimal amounts, balanced postings and immutable journal designs.
- **Transactional integrity:** a posting must succeed or fail as one operation. It cannot partially debit and quietly omit the credit.
- **Period controls:** closed periods and access rules prevent unauthorised backdating or mutation.
- **Bank reconciliation:** CSV intake and controlled matching, while avoiding unsupported claims about full bank-feed integrations.
- **Audit operations:** workpapers, findings, reviewer approval concepts and deterministic monitoring checks.
- **AI assistance:** explanations are read-only and separated from transactional posting.

### Limitations

Live banking feeds, statutory statements, full tax treatment, year-end close, complex audit evidence storage and regulated sign-off are not all implemented or verified. **No audit opinion or regulatory certification is implied.**

---

## Mission 07 / Social-impact reporting

**Engagement:** Jozi My Jozi, volunteer work during 2025  
**Stack:** Power Apps, SharePoint, Power BI  
**Stage:** Historic volunteer delivery

### Why this mattered

Useful dashboards require reliable first capture. When a nonprofit depends on spreadsheets or fragmented notes, structured intake and consistent definitions can have more value than advanced predictive modelling.

**Work included:** shelter and service data capture, intervention/outcome categories, occupancy and throughput reporting, dashboard design, validation rules and non-technical user support.

**Principle:** never expose beneficiary-level records simply to demonstrate the reporting system. Aggregate, anonymise and obtain the appropriate permission for examples.

**Review:** [Social-impact case study](CLIENT_CASE_STUDIES.md#9-jozi-my-jozi--social-impact-analysis)

---

## Mission 08 / Artist, commerce and independent product systems

**Sources:** [CABO Artist Hub](https://github.com/CayelaemJ/Artist-Management-Hub), [CABO corporate site](https://github.com/CayelaemJ/CABOSOLUTIONS) and other independent projects

These products let me explore how the same engineering principles apply to smaller operational domains.

**Artist operations:** booking enquiries, synthetic social/career-health scores, management dashboards, privacy and role design. The prototype intentionally uses fictional artists and is not proof of live social-media integrations or financial controls.

**Company enquiries:** React/Vite/Three.js frontend, an API and persisted contact records, with validation and private administrative access.

**Commerce and booking:** independent Botswana-oriented experiments with customer journeys, business workflows, order/bookings concepts and system integration. Some source repositories remain private and should not be represented as publicly inspectable.

**The overarching lesson:** operational software needs a clear business event, source of truth, ownership of state transitions, permission model and trustworthy user feedback whether it supports banks, schools or artist bookings.

---

## The current engineering notebook

Recent work in November 2026 spans:

| Theme | Main concern | Stage |
|:--|:--|:--|
| Database change simulation | Capturing updates and mapping freshness into reporting views | Experimentation |
| MySQL and PostgreSQL roles | Clear transformation ownership, tenancy and reporting integration | Validation |
| Admin MFA | Step-up routes, recovery and live integration tests | Active hardening |
| Security scanning | Regression, dependency/secret checks and AI-assisted analysis | Active engineering |
| Docker/local CI | Disposable test systems and self-hosted runners | In operation / ongoing refinements |
| Cloud deployment | Render and Cloudflare staged work, avoiding unverified cutovers | Guarded integration |
| Applied AI | Grounded assessment, provider fallback and human oversight | Product work and evaluation |

**No claim of universal completion is made for these ongoing initiatives.**

[← Back to the profile](../README.md) · [System design and trade-offs](OMNIMASTER_SYSTEM_DESIGN.md) · [Full project atlas](PROJECT_PORTFOLIO.md)
