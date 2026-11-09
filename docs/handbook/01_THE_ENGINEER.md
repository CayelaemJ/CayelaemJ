# Chapter 01 | The engineer behind the systems

[Table of contents](../OMNIMASTER_HANDBOOK.md) · [Next: The career →](02_THE_CAREER.md)

## The short version

I'm **Cayelaem Jantjies**, a Johannesburg-based data engineer, analytics engineer and full-stack software developer. My formal foundation is a **BCom in Statistics and Data Science from the University of Pretoria (2023)**. I have over three years of hands-on professional engineering and analytics experience spanning financial services, manufacturing, FMCG, broadcasting, agriculture and social-impact projects.

What differentiates my work is range with continuity. I can follow a problem from an operational source system, through SQL and transformations, into a semantic model, an API, a user interface and the controls required to run it safely.

My role is not simply to report on technology. I build the technology that makes the reporting, workflow or decision possible.

## The version that matters in a project

I often find that the initial request is narrower than the real problem.

> “The report is slow.”

The underlying issue might be an expensive query, ambiguous relationships in the semantic model, repeated API calls or a missing pre-aggregation. Fixing only the loading animation would leave the bottleneck intact.

> “We need real-time dashboards.”

The source may offer only a nullable timestamp with one-second precision. Polling it every minute is not automatically CDC, and a deleted record may never trigger a change. First define the freshness contract, then choose an ingestion design.

> “Can AI mark this answer?”

That question also implies source grounding, rubric consistency, partial credit, appeals, data privacy, educator review, latency and cost. A model call is one component of the workflow.

This is how I think: **follow the failure across boundaries instead of treating every symptom as an isolated ticket**.

## The work I bring to a team

| Practice | What I can contribute | Example evidence |
|---|---|---|
| **Data engineering** | SQL modelling, staging, quality checks, source integrations, historical semantics, pipeline debugging | Manufacturing and enterprise BI engagements; [CDC lab](../../projects/cdc-replay-lab/) |
| **Analytics engineering** | Power BI, DAX, Power Query, dimensional modelling, access-aware measures, dashboard performance | Banking, research, agriculture and FMCG; [SQL-plan lab](../../projects/sql-query-plans/) |
| **Full-stack delivery** | React, TypeScript, Node.js, API contracts, PostgreSQL/MySQL integration, testing and release processes | [The Fixer](https://github.com/CayelaemJ/NewChanges), [CABO Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) |
| **Applied AI** | Structured outputs, evidence-aware evaluations, provider fallback and human-in-the-loop product flows | Learning assessment experiments; [offline evaluation lab](../../projects/ai-output-evaluation/) |
| **Security and operations** | Identity, authorisation, MFA workstreams, synthetic integration testing, CI, migrations and rollback | Public security and infrastructure PRs, with release gates still visible |

Not all of these disciplines have the same depth of experience. I distinguish production delivery, hands-on experiments and developing skills instead of assigning myself every fashionable job title on the internet.

## What I believe good engineering looks like

**Correctness before presentation.** The number is only useful when we can explain what was counted, at which grain, with which exclusions and at what time.

**A working system before an impressive diagram.** Architecture earns its value when deployment, failure recovery, access and maintenance are possible.

**Security as a property of workflow.** A beautiful admin screen cannot compensate for weak server-side authorisation or an unsafe database role.

**Care for the user.** The correct solution is one someone can use, understand and trust; unnecessary complexity is a cost to the person on the other side of the application.

**A measurable definition of done.** I look for executable tests, traceable outcomes and clear limitations, not declarations that everything is “production ready.”

## What you will find in this handbook

You will find career history and practical technical explanations together. The former explains where my instincts came from. The latter shows the choices I make when building. Some projects are proprietary, some are public, and some are intentionally small synthetic labs. Each kind of evidence has a different meaning.

**My long-term direction:** evolve from hands-on cross-stack ownership toward solution architecture and technology leadership without losing the technical depth to question a system's assumptions.

### Review the primary record

[Professional client case studies](../CLIENT_CASE_STUDIES.md) · [Skills and evidence](../TECHNICAL_SKILLS.md) · [Public repository catalogue](../PROJECT_PORTFOLIO.md)

[← Table of contents](../OMNIMASTER_HANDBOOK.md) · [Next: From statistics to full-stack ownership →](02_THE_CAREER.md)
