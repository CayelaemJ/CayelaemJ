
# Engineering field notes
*7 November 2026 · Cayelaem Jantjies*

> This is a public engineering summary, not a release certification. A branch, a passed test or a staging deployment does not by itself prove production readiness.

[← GitHub profile](../README.md) · [Complete project atlas](PROJECT_PORTFOLIO.md) · [Professional case studies](CLIENT_CASE_STUDIES.md)

## My engineering principles

I prefer systems that are **correct, useful, secure and operable**. That means being able to trace a dashboard number to a source, reproduce a data-quality defect, challenge a risky deployment and explain the resulting trade-offs to people who are not engineers.

## Current workstreams

### The Fixer: data movement and governed reporting

**Challenge.** Repeated conversions, inconsistent validation and unclear change semantics can introduce delay and misleading output. Admin security and migrations must not be considered complete just because the UI loads.

**Approach in progress:**
- Work with stable SQL/API source contracts, reporting views and database-centred transformations when appropriate.
- Simulate CDC-style source changes with synthetic data, looking closely at watermark semantics, update-time precision, nullable values, deletes, replay and idempotency.
- Investigate MySQL reporting and PostgreSQL application integration without assuming a single database is right for every workload.
- Keep local Docker CI isolated from production services and test data.
- Validate sensitive-route step-up authentication, TOTP/WebAuthn flows and administrative audit behaviour.

**Verification still needed:** end-to-end change propagation, full authentication wiring, deployment parity, migration cutover approval, recoverability and rollback.

**Evidence:** [NewChanges repository](https://github.com/CayelaemJ/NewChanges)

### CABO Learning Hub: education intelligence

**Challenge.** Student learning is bigger than a list of courses and marks. Schools and families need continuity, context, interventions and appropriate safeguards around children.

**Engineering direction:** Longitudinal learner history, assessments, educator decision support, parent/institution workflows, school onboarding and system migration, age-appropriate UX, and carefully scoped AI-generated assistance.

**AI reliability:** source grounding, evaluator review, provider fallback, cost/latency boundaries and privacy controls. Sensitive outcomes should not depend on an unchecked model answer.

**Verification still needed:** nationwide rollout suitability, Botswana and South African school integration agreements, full privacy and security review, data migration approvals, and genuine native Android/iOS parity.

**Evidence:** [Training and Development Hub](https://github.com/CayelaemJ/Training-and-Development-Hub)

### Platform engineering and security

| Dimension | Engineering question | Evidence to seek |
| :-- | :-- | :-- |
| Identity | Can every protected action prove the correct user and recent authentication? | TOTP/WebAuthn and live route tests |
| Authorisation | Can a user escape tenant or role boundaries? | Negative tests, RLS and IDOR checks |
| Data quality | Do sources, keys, types, timestamps and units behave as expected? | Contract checks and reproducible fixtures |
| CI/CD | Can tests run without paid services, secrets or production effects? | Docker runs and recorded test results |
| Releases | Can the new version be observed, rolled back and recovered? | Staging checks, runbooks and restore rehearsals |

Tools such as Docker, Playwright, Vitest, Semgrep, Trivy and local AI-assisted scanning can support this work. They do not replace independent review, threat modelling or production evidence.

## Professional analytics patterns

In enterprise reporting, data semantics often matter more than chart formatting. Examples from previous engagements include:

- Resolving duplicate joins and mismatched dimensional grain across logistics and manufacturing datasets.
- Investigating database deadlocks, dynamic-pivot drift and source-data failures before altering Power BI reports.
- Building market-aware analytics with row-level access and filter-aware business measures.
- Improving model performance and automating repetitive operational reports.

Reported historical results include **270M+ survey records**, **40% quicker dashboards** and **up to 70% less manual reporting effort** in selected assignments. These are career outcome claims, not live counters.

## Design decisions I prefer

**Validate at meaningful boundaries.** Excessive duplicated validation can be expensive and contradictory; insufficient validation corrupts downstream decisions. I aim for source contracts, schema integrity and validation placed where it adds clear protection.

**Choose the right compute layer.** Some transformations belong in database views or materialised outputs, others in ELT pipelines or services. It depends on consistency, isolation, query load, ownership and deployment complexity.

**Separate verified delivery from roadmap.** Pilot features, experimental AI, unmerged branches and native parity plans should be labelled. This avoids claiming a production product where one is not yet available.

**Treat security and AI safety as requirements.** Authorisation, model evaluation, human review, privacy protections, backups, monitoring and incident response belong to architecture, not marketing copy.

## Detailed links

- [Complete project and portfolio atlas](PROJECT_PORTFOLIO.md)
- [Professional engagement case studies](CLIENT_CASE_STUDIES.md)
- [Technical skills and evidence matrix](TECHNICAL_SKILLS.md)
- [Back to the profile](../README.md)

*No client datasets, credentials, privileged staging URLs or private source files are reproduced in this document.*
