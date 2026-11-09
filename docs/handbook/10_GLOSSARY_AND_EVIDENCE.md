# Chapter 10 | Glossary, references and claim register

[← Previous](09_LEADERSHIP_AND_NEXT.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Return to cover](../../README.md)

This last chapter is here because technical language should make work understandable, and public evidence should not quietly turn aspiration into achievement.

## A working glossary

| Term | What I mean when I use it |
|---|---|
| **Business grain** | The one real-world event or entity represented by one row of a fact or source table |
| **Data contract** | Explicit source/output schema, keys, semantic meaning, ownership and permitted changes |
| **ETL / ELT** | Extract-transform-load or extract-load-transform; the correct choice depends on where transformations belong |
| **Watermark** | Position or value used to identify new/changed data; its precision and reliability determine what can be missed |
| **CDC** | Change data capture, typically recording actual changes rather than repeatedly rereading a full source |
| **Idempotency** | Repeating the same operation has no unintended additional effect |
| **Tombstone** | Evidence of a deletion maintained for consumers rather than silently removing historical change context |
| **Bronze / Silver / Gold** | Raw or auditable intake, curated validated records, and consumer-ready aggregates or views |
| **Semantic model** | Business-aware analytical relationships, dimensions, measures, security and time interpretation |
| **Star schema** | Facts at a defined grain connected to shared descriptive dimensions |
| **DAX** | Formula language for analytical measures and calculations in Power BI and related Microsoft tools |
| **RLS** | Row-level security, restricting which data a database or semantic-model user can access |
| **RBAC** | Role-based access control; identity alone is not permission |
| **MFA / TOTP / WebAuthn** | Multi-factor authentication, time-based one-time codes, and passkey/security-key standards |
| **SSRF** | Server-side request forgery, including tricks that push a server into connecting to unauthorised endpoints |
| **SAST** | Static application security testing; findings require analysis, not blind acceptance |
| **Sargable query** | A query shaped to let the database efficiently use indexes on searchable predicates |
| **Human-in-the-loop** | A meaningful human control over consequential system or model output, not a decorative checkbox |
| **Exact-commit CI** | Tests and checks tied to the specific source commit being considered for merge or release |
| **Deployment gate** | A requirement that must be satisfied before enabling a candidate in the intended environment |

## Claim register: what you can verify here

| Claim or theme | Nature of evidence | Primary reference |
|---|---|---|
| BCom in Statistics and Data Science (2023) | Education history from CV, not independently validated by GitHub | [Career case studies](../CLIENT_CASE_STUDIES.md), [profile timeline](../../README.md) |
| 3+ years across analytics and engineering | Professional history as documented by CV and engagement summaries | [Career record](../CLIENT_CASE_STUDIES.md) |
| 270M+ survey records | **CV-reported historical scope**, not a public dataset benchmark | [FMCG case study](../CLIENT_CASE_STUDIES.md#5-diageo-africa--iqbusiness-large-scale-brand-analytics) |
| 40% dashboard load-time improvement | **CV-reported historical outcome**, not rerun here | [Banking case study](../CLIENT_CASE_STUDIES.md#3-fnb--iqbusiness-consulting-commercialretail-analytics) |
| Up to 70% manual reporting reduction | **CV-reported historical outcome**, dependent on engagement | [Professional cases](../CLIENT_CASE_STUDIES.md) |
| Banking analytics across four markets | Historical work scope | [Banking case](../CLIENT_CASE_STUDIES.md#3-fnb--iqbusiness-consulting-commercialretail-analytics) |
| The Fixer implementation | Public code with active issues/PRs; no blanket production readiness claim | [NewChanges](https://github.com/CayelaemJ/NewChanges) |
| Learning Hub education/AI implementation | Public code, pilots and planned work clearly distinguished | [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) |
| Financial and HR products | Public prototype/staging work and explicit limits | [Financial Intelligence](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software), [Human Capital](https://github.com/CayelaemJ/HR-Software) |
| Four educational engineering labs | Runnable synthetic source, local tests and GitHub Actions | [Project index](../../projects/README.md), [CI workflow](../../.github/workflows/engineering-labs-ci.yml) |
| CTO or technology leadership | **Future career direction**, not current position | [Chapter 09](09_LEADERSHIP_AND_NEXT.md) |

## How to verify a project responsibly

1. **Start with the README:** identify what the author claims is implemented versus planned.
2. **Look at source and tests:** a file or PR exists, but check what actually executes.
3. **Check CI on the relevant commit:** historical green status does not certify a new head.
4. **Check release status:** staging, pilot, private experiment and production are different environments.
5. **Check privacy boundaries:** absence of client source code is often appropriate, not evidence the engagement never occurred.
6. **Ask about limitations:** I want a reviewer to challenge architectural and evidence assumptions.

## Other long-form references

- [Client case studies](../CLIENT_CASE_STUDIES.md): roles, sectors and engagement-level technical history.
- [Project atlas](../PROJECT_PORTFOLIO.md): catalogue and stage of visible independent products.
- [Technical skills and evidence](../TECHNICAL_SKILLS.md): honest skills matrix.
- [Engineering mission dossiers](../OMNIMASTER_MISSION_DOSSIERS.md): deeper system context.
- [System design playbook](../OMNIMASTER_SYSTEM_DESIGN.md): practices and trade-offs.
- [Engineering field notes](../ENGINEERING_FIELD_NOTES.md): current workstreams and lessons.
- [Runnable labs](../../projects/README.md): reviewable Python, SQL and evaluation examples.

## Epilogue

I want my GitHub to be useful to three kinds of readers: somebody who wants to understand me as an engineer, somebody who wants to inspect how I think, and somebody who wants to verify code rather than trust a headline.

That is why this handbook contains **career history, real project constraints, executable examples and limitations side by side**.

**One mind. Every layer. No pretending a roadmap is a release.**

[← Previous](09_LEADERSHIP_AND_NEXT.md) · [Back to the handbook](../OMNIMASTER_HANDBOOK.md) · [GitHub cover](../../README.md)
