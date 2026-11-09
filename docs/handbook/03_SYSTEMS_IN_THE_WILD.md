# Chapter 03 | Systems in the wild

[← Previous](02_THE_CAREER.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](04_DATA_ENGINEERING.md)

A career is easier to understand through the systems and constraints behind it than through a list of logos. This chapter is a guided tour of what I have worked on, why it was difficult and what kind of evidence a reviewer can inspect.

## 01. Enterprise banking analytics across four markets

**Status:** Historical professional delivery. **Practice:** Power BI, DAX, Power Query, access-aware reporting.

I worked on commercial and retail reporting spanning **South Africa, Namibia, Botswana and Zambia**, with a documented portfolio of **18 banking dashboards**. Regional reporting changes the problem: access controls, product definitions, local market contexts and time comparisons have to remain intelligible as the audience expands.

**Engineering focus:** improve model relationships, simplify expensive measure logic, challenge over-broad access and remove repeated manual transformations. My CV reports a **40% improvement in dashboard load time** on relevant optimisation work.

**What I learned:** a fast report showing inconsistent numbers is not a successful optimisation. Establish the semantic contract, then measure performance.

**Evidence:** [Professional case-study record](../CLIENT_CASE_STUDIES.md#3-fnb--iqbusiness-consulting-commercialretail-analytics). Client code and data remain proprietary.

## 02. Commercial research at survey scale

**Status:** Historical professional delivery. **Practice:** large survey datasets, Power Query, DAX, marketing analytics.

A documented FMCG engagement involved cleaning, modelling and visualising **more than 270 million survey records** for commercial insights. Large volumes turn small modelling mistakes into expensive mistakes, especially when joining outlets, campaigns, brands and survey responses at mismatched grains.

**Engineering focus:** careful transformations, model efficiency, metric definitions and meaningful breakdowns for business owners.

**What I learned:** scale alone is not the achievement. The real product is a trusted commercial measure that users can explain.

**Evidence:** [Research and FMCG case studies](../CLIENT_CASE_STUDIES.md#5-diageo-africa--iqbusiness-large-scale-brand-analytics). The record is historical; these are not public raw datasets.

## 03. Manufacturing and logistics in Australia

**Status:** Historical delivery. **Practice:** SQL Server/T-SQL, Power BI, DAX, Power Automate, Fabric workflows.

I supported remote Australian manufacturing operations, where reports linked production, dispatch, stock, employee scheduling and operational timing. A scheduler model documented in my CV included **15 temporary SQL tables, 35 DAX measures, 11 relationships and reporting across eight states**.

**Engineering focus:** reason about event grain, repair dataflow failures, support accurate production-versus-hours reporting, and automate recurring delivery. Complex SQL became useful only after the business event and join path were defined.

**What I learned:** the database schema and the real world are different representations. Delivery engineers must understand both.

**Evidence:** [Manufacturing case study](../CLIENT_CASE_STUDIES.md#1-bitberry--bestbar--australia-data-platform-manufacturing-and-delivery-analytics). Industrial source systems are not reproduced in this public profile.

## 04. The Fixer: from reporting to governed applications

**Status:** Public implementation with active security, CDC and cloud work; **not** an approved all-features production cutover.  
**Repository:** [NewChanges](https://github.com/CayelaemJ/NewChanges).

The Fixer explores governed imports and synchronisation from SQL views, APIs and files into employer, partner and administrative reporting. It crosses product boundaries: **TypeScript/Fastify APIs, PostgreSQL/Prisma, a React modernisation track, reporting, authentication and operational controls**.

A current design question is how to connect source updates with dashboard freshness. The simulation work includes a MySQL row-binlog experiment, but the existing ten-feed reporting source still requires an ingestion-specific CDC adapter and dedicated validation. Polling a nullable timestamp is not the same as capturing every change.

**What I learned:** reporting freshness is a contract between source, transformation and consumer, not a UI refresh button.

**Evidence:** [Repository](https://github.com/CayelaemJ/NewChanges) · [Active CDC integration issue](https://github.com/CayelaemJ/NewChanges/issues/241) · [Security audit issue](https://github.com/CayelaemJ/NewChanges/issues/232).

## 05. CABO Learning Hub: education as a long-lived system

**Status:** Public product under development, with pilot and proposed integrations; **not** a government deployment.  
**Repository:** [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub).

The product goal is bigger than course delivery: connect learning materials, assessments, teachers, guardians, institutional roles, historical progress and future interventions. I have explored source-grounded written exams and AI-assisted partial-credit marking, with teacher oversight needed for consequential decisions.

Longitudinal educational records create engineering difficulties that ordinary demo apps avoid: learner transfers, role changes, guardian consent, assessment provenance, country jurisdiction and controlled retention.

**What I learned:** a learner is not a row that belongs forever to one school. Data governance must travel with the person and the purpose.

**Evidence:** [Repo status and documented limits](https://github.com/CayelaemJ/Training-and-Development-Hub) · [Admissions and transfer epic](https://github.com/CayelaemJ/Training-and-Development-Hub/issues/97) · [Year-end progression review issue](https://github.com/CayelaemJ/Training-and-Development-Hub/issues/163).

## 06. CABO Financial Intelligence: the transaction is the truth

**Status:** Staging/prototype, not statutory accounting or auditing certification.  
**Repository:** [Accounting, Audit and Analytics Software](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software).

This independent product explores a **double-entry ledger, exact-decimal values, immutable journals, atomic invoice settlements, bank CSV reconciliation, period locking and audit review**. Reporting consumes the controlled transactional state rather than altering it.

A vital separation: generated financial explanations may help a reader understand a report, but they must not silently create, amend or approve journal entries.

**What I learned:** in financial workflows, an atomic transaction and a documented reversal matter more than a dashboard animation.

**Evidence:** [Repository and capability matrix](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software) · [Mission dossier](../OMNIMASTER_MISSION_DOSSIERS.md#mission-06--cabo-financial-intelligence).

## 07. CABO Human Capital: decisions need accountable humans

**Status:** Public prototype and synthetic development.  
**Repository:** [HR-Software](https://github.com/CayelaemJ/HR-Software).

Recruitment and workforce software deals with incomplete evidence, privacy, fairness and people whose opportunities may depend on the output. I have explored role-scoped candidate workflows, review history, evidence provenance and AI-assisted recommendations.

**What I learned:** a score without an explanation is not better decision-making. Humans need to remain accountable for meaningful hiring and development decisions.

**Evidence:** [HR software repository](https://github.com/CayelaemJ/HR-Software) · [Mission dossier](../OMNIMASTER_MISSION_DOSSIERS.md#mission-05--cabo-human-capital).

## 08. Social impact and smaller operational products

**Status:** Historical volunteer work plus public prototypes.

In social-impact reporting I worked with capture processes and dashboards for service outcomes. Independent work in artist management, commerce and bookings has explored how enquiries, identities, transactions and notifications form usable business workflows.

**What I learned:** even a small application needs an identifiable business event, an authoritative state change and an accessible path for the user.

**Evidence:** [Volunteer case study](../CLIENT_CASE_STUDIES.md#9-jozi-my-jozi--social-impact-analysis) · [Artist Management Hub](https://github.com/CayelaemJ/Artist-Management-Hub) · [CABO Solutions website](https://github.com/CayelaemJ/CABOSOLUTIONS).

## Reading the range correctly

These examples are not eight claims of production certification. Some are historical professional delivery, some are inspectable public implementations, and others are unfinished product experiments. What connects them is the engineering approach: **start with the real operational problem, make definitions explicit, enforce correct transitions, and prove the system's behavior**.

[Complete project inventory](../PROJECT_PORTFOLIO.md) · [Detailed mission dossiers](../OMNIMASTER_MISSION_DOSSIERS.md)

[← Chapter 02](02_THE_CAREER.md) · [Next: Data engineering →](04_DATA_ENGINEERING.md)
