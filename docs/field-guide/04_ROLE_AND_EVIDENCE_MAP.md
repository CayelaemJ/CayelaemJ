# Field Guide 04 | Role and evidence map

[← Engineering workbook](03_ENGINEERING_WORKBOOK.md) · [Volume II](../OMNIMASTER_FIELD_GUIDE.md) · [Next: Decision journal →](05_DECISION_JOURNAL.md)

This page is the most efficient way to assess my fit for an engineering role. It translates my cross-industry experience into actual technical responsibilities, linked examples and open development areas.

**Who I am:** Cayelaem Jantjies, a Johannesburg-based data engineer, analytics engineer and full-stack developer with a BCom in Statistics and Data Science from the University of Pretoria (2023) and over three years of professional experience.

**My specialisation is connected delivery:** tracing a business problem through source data, transformations, semantic models, APIs, applications, access control, testing and operations.

## A 60-second career map

| Evidence | What it demonstrates | Where to inspect |
|---|---|---|
| Banking dashboards spanning **four African markets** | Multi-market analytics, security-aware measures, commercial reporting | [Professional banking case](../CLIENT_CASE_STUDIES.md) |
| Commercial research involving **270M+ survey records** | Large reporting scope, model grain, data preparation and performance focus | [FMCG research case](../CLIENT_CASE_STUDIES.md) |
| Remote Australian manufacturing work | Cross-border delivery, SQL Server, logistics, production and scheduler analytics | [Manufacturing case](../CLIENT_CASE_STUDIES.md) |
| PostgreSQL + TypeScript application ownership | Data and software engineering beyond BI reports | [The Fixer source](https://github.com/CayelaemJ/NewChanges) |
| Learning and assessment product development | Education workflows, permissions, applied AI, source evidence | [Learning Hub source](https://github.com/CayelaemJ/Training-and-Development-Hub) |
| Independent HR and finance platforms | Domain modelling, privacy considerations, atomic financial operations | [HR](https://github.com/CayelaemJ/HR-Software) · [Financial Intelligence](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software) |
| Four reproducible engineering labs | Ability to explain and test data and AI patterns using source code | [Runnable project index](../../projects/README.md) |

**Metrics such as 270M+ records and reported performance improvements come from professional/CV evidence**, not public benchmarking. Private client code is not represented as open source. The independent products vary in maturity and should not be interpreted as uniformly deployed.

## Find the relevant engineering perspective

### If you are hiring a Data Engineer or Data Platform Engineer

**My relevant work:** SQL Server/T-SQL, SQL staging, ELT/ETL design, dataflow failures, Microsoft Fabric exposure, operational source integration, PostgreSQL/MySQL modelling and source freshness investigations.

**Examples to review:** [Australian manufacturing](../handbook/03_SYSTEMS_IN_THE_WILD.md) · [Data engineering chapter](../handbook/04_DATA_ENGINEERING.md) · [CDC lab](../../projects/cdc-replay-lab/) · [CDC issue #241](https://github.com/CayelaemJ/NewChanges/issues/241).

**What I would discuss:** late-arriving facts, restart-safe ingestion, watermark collisions, model grain, index selection, data contracts, recovery and measurable freshness.

**Growth edge:** deeper real-time/distributed stream operations and platform-scale orchestration; I do not equate a synthetic lab with a production Kafka/Flink deployment.

### If you are hiring an Analytics Engineer or BI Engineer

**My relevant work:** Power BI, DAX, Power Query M, SQL, dimensional modelling, multi-market security/reporting, manufacturing/financial metrics and optimisation.

**Examples to review:** [Case studies](../CLIENT_CASE_STUDIES.md) · [BI chapter](../handbook/05_ANALYTICS_ENGINEERING.md) · [SQL query-plan lab](../../projects/sql-query-plans/).

**What I would discuss:** semantic ownership, star schemas, RLS, time intelligence, repeatable KPIs, the effect of query shape and business interpretation.

**Growth edge:** scaling governance and observability across larger enterprise semantic-model estates and new Fabric workloads.

### If you are hiring a Full-Stack or Backend Engineer

**My relevant work:** React, TypeScript, Fastify/Node.js, PostgreSQL/Prisma, APIs, integrations, admin workflows, validation, testing and cloud delivery considerations.

**Examples to review:** [The Fixer](https://github.com/CayelaemJ/NewChanges) · [End-to-end system atlas](01_ARCHITECTURE_ATLAS.md) · [Release and security chapter](../handbook/07_SECURITY_AND_DELIVERY.md).

**What I would discuss:** service boundaries, role and tenant security, schema changes, retries, idempotency, API negative cases, testing and deployment rollback.

**Growth edge:** bigger multi-team service ownership, incident response at scale and longer-running operational reliability programs.

### If you are hiring for Applied AI / AI Product Engineering

**My relevant work:** integrating task-based AI capabilities into learning/product workflows, evidence-aware outputs, provider-routing experiments, fallback behaviour and human approval boundaries.

**Examples to review:** [Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) · [AI product chapter](../handbook/06_PRODUCTS_AND_AI.md) · [Offline AI evaluation lab](../../projects/ai-output-evaluation/).

**What I would discuss:** output contracts, evaluation sets, source provenance, PII constraints, provider errors, latency/cost and how to keep consequential decisions reviewable.

**Growth edge:** production-grade benchmark design, monitoring/calibration and cross-provider security operations. Model integration is not a claim of training or running proprietary foundation models.

### If you are assessing a Solution Architect / Technical Leadership pathway

**My relevant work:** bridging commercial/operational requirements with SQL, application design, access rules, integration/testing and release risk. Independent product development has expanded my understanding of trade-offs across functions.

**Examples to review:** [Leadership chapter](../handbook/09_LEADERSHIP_AND_NEXT.md) · [Architecture atlas](01_ARCHITECTURE_ATLAS.md) · [Decision journal](05_DECISION_JOURNAL.md).

**What I would discuss:** business outcomes, scope boundaries, compliance, budget, architecture fitness, staged release gates and technical documentation.

**Growth edge:** formal technical leadership and larger-team architectural accountability. **This is a career direction, not a claim that I currently hold a CTO title.**

## What I have actually used

| Domain | Tools or approaches present in my work | Evidence caveat |
|---|---|---|
| **Data / BI** | SQL Server, Power BI, DAX, Power Query, Fabric, ETL/ELT, dimensional modelling | Depth varies by engagement and tool |
| **Backend** | TypeScript, Node.js/Fastify, REST APIs, PostgreSQL, MySQL/SQL Server integrations | Product work includes active/staging PRs |
| **Frontend** | React, TypeScript, web UX, dashboard/chart interfaces | Not all independent frontends have full feature parity |
| **Mobile** | Android Kotlin and iOS workstreams | Native parity and real-device QA still in progress |
| **AI** | Groq/Hugging Face routing experiments, evidence/evaluation, human review design | Live provider availability varies; no unverified ML production claim |
| **Security/quality** | Docker testing, Vitest/Playwright, source/security checks, MFA designs, CI | An audit or passing test does not certify all releases |
| **Cloud** | Render, Cloudflare, AWS RDS experiments, Aiven/Neon migration preparation | Cutover candidates have independent gating and cost constraints |

The [complete skills matrix](../TECHNICAL_SKILLS.md) provides more specific caveats.

## What I'd like a reviewer to challenge me on

- Where would I store a source event so recovery stays possible?
- How do I distinguish a correct-looking dashboard from a correct metric?
- When would I place transformation in the database instead of the application?
- How would I design administrative MFA recovery without introducing a bypass?
- What evidence would persuade me *not* to release?
- How does applied AI create real product value while respecting people and their data?

These are useful conversations because the answers require concrete engineering judgment.

## The rest of the book

[Volume I: 10-chapter career and engineering handbook](../OMNIMASTER_HANDBOOK.md) · [Volume II index](../OMNIMASTER_FIELD_GUIDE.md) · [Project archive](../PROJECT_PORTFOLIO.md)

**Contact:** [LinkedIn](https://www.linkedin.com/in/cayelaem-jantjies-000b45144/) · [Interactive portfolio](https://omnimaster-portfolio.onrender.com) · [Email](mailto:cay.jantjies1703@gmail.com)

[← Workbook](03_ENGINEERING_WORKBOOK.md) · [Next: Architecture decisions →](05_DECISION_JOURNAL.md)


### If you are evaluating my UI/UX development experience

My experience combines building data-rich interfaces, responsive React applications, operational workflows, dashboard design and mobile/dark-mode testing with growing attention to usability, accessibility, user feedback and design systems. See [Volume VI: The Human Interface](../OMNIMASTER_HUMAN_INTERFACE.md) for the full reasoning and public cases. This is integrated cross-stack UI/UX work, not a claim of formal design certification or independently measured user-research outcomes.
