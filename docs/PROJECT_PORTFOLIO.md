# Complete project and portfolio atlas
*Public engineering portfolio · Updated 2 November 2026 · Cayelaem (Thabo) Jantjies*

This document inventories the repositories presently visible through my GitHub account and the important professional case studies that cannot be shared as source code. It distinguishes **demonstrated implementation**, **active development / pilot**, **prototype**, **design or roadmap**, and **legacy/supporting repository**. A repository, feature proposal, or deployment configuration does not by itself prove that a service is production-ready.

## Portfolio navigation
- [Professional client engagements and case studies](CLIENT_CASE_STUDIES.md)
- [Engineering skills and evidence](TECHNICAL_SKILLS.md)
- [GitHub overview](../README.md)

## Education, learning and applied AI

### 01. CABO Learning Hub
**Repository:** [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub)  
**Status:** Active development across implemented workflows, feature branches and pilot concepts; enterprise-wide and native parity are not complete.

**Problem:** Learner support cannot be reduced to course content; schools need continuity of academic history, interventions, development milestones and coordinated educator/guardian visibility.

**My contribution:** Architecture and development of connected learner, teacher and institution experiences; assessment workflows; API/database integration; security/role design; product positioning, documentation, proof-of-concept demos and testing strategy. Technology evident in the repository includes React, TypeScript, Express, PostgreSQL/Drizzle, file/material ingestion and AI-assisted assessment.

**Documented functionality:** Individual materials uploads; multiple-choice practice; document-grounded written examinations; short/long/scenario questions; partial-credit AI assessment and review flags. Other documented phases include organization spaces, teaching/assessment roles, academic gradebooks, learner progression, school reports, interventions, education governance and demonstrations with synthetic schools. The repo's own delivery register is authoritative for per-phase completeness.

**My engineering priorities:** Tutor/teacher workflow usability; explicit separation of AI suggestions and human-approved marks; parent/guardian and institutional boundaries; learner history transfers; audit trails; support for school/district/province scale; WCAG 2.2 AA design goals; POPIA/Botswana privacy review; synthetic demonstration reliability.

**Cross-platform work:** Genuine Kotlin/Android Studio and native iOS experiences are target implementations, not web wrappers. Full feature parity, tested release binaries and device QA are outstanding goals, not completed releases.

**AI architecture:** Multi-provider orchestration using Groq/Hugging Face has been explored and actively worked on; model availability, routing, fallback and end-to-end reliability must be verified from the relevant branch and environment. Do not infer universal availability from API credentials or prototype screens.

**Evidence / constraints:** [Repository README](https://github.com/CayelaemJ/Training-and-Development-Hub/blob/main/README.md) · [Delivery register](https://github.com/CayelaemJ/Training-and-Development-Hub/blob/main/docs/PHASES_1_TO_4_DELIVERY_REGISTER.md). Never assert fully launched national deployment.

## Data platforms, engineering and enterprise apps

### 02. empower-fin Dashboard Portal / EFS Optimise / NewChanges–The Fixer workstream
**Repository:** [NewChanges](https://github.com/CayelaemJ/NewChanges)  
**Status:** Substantial existing TypeScript/Fastify/PostgreSQL financial-wellness portal and React migration. *Naming/branding and intended The Fixer direction are being evolved; the repository README still describes empower-fin.* Infrastructure-migration work is not evidence of a completed production cutover.

**Problem:** Repetitive reporting and fragmented external sources make timely financial-wellness analysis and tenant-controlled administration difficult.

**My contribution:** End-to-end individual engineering across requirements, canonical data contracts, SQL/API/file ingestion, dashboards, semantic definitions, multi-tenant roles, white-label branding, scheduled reports, security, data-quality governance, model lifecycle and tests.

**Architecture / demonstrated design:** Node.js + TypeScript + Fastify API; PostgreSQL and Prisma; legacy canonical dashboard and separate React UI migration; 10 source feeds from read-only SQL views, HTTPS API and CSV/XLSX/JSON; date-aware historical reporting; employer/portfolio/channel-partner administration.

**Distinct technical achievements documented in the source CV/repository:** snapshot/cohort read caching for large employers, null-aware scoring, asynchronous import feedback, accessible metric definitions, brand-palette extraction with contrast checks, source-data guardrails, model version lifecycle, auditability, SMTP schedules and controlled refreshes.

**Operational direction:** Isolated Docker pre-push PostgreSQL tests, security/MFA reviews, Cloudflare edge and Render services, evaluation of Aiven PostgreSQL as a low-cost Neon alternative. Production migrations and rebranding must be validated separately. Older Railway deployment docs are historical architecture, **not** my preferred future hosting.

**Evidence / constraints:** [NewChanges README](https://github.com/CayelaemJ/NewChanges/blob/main/README.md). Do not publish credentials, employer records or client-specific raw data.

### 03. EFS React Migration
**Repository:** [EFS-React-Migration](https://github.com/CayelaemJ/EFS-React-Migration)  
**Status:** Supporting repo; minimal public README. The documented React migration is also described in the main NewChanges codebase. Preserve current canonical dashboard behavior while building UI parity; do not imply this standalone repository contains a finished independent release.

### 04. Testing-EFS
**Repository:** [Testing-EFS](https://github.com/CayelaemJ/Testing-EFS)  
**Status:** Historical/supporting snapshot of empower-fin portal documentation and releases. Shows earlier v0.5.x source contracts, reporting, tenant branding and dashboard caching work. Treat as an engineering chronology rather than a separate current product.

### 05. CABO Financial Intelligence — accounting, audit and analytics
**Repository:** [Accounting-Audit-And-Analytics-Software](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software)  
**Status:** Gated staging, not production or certified accounting/auditing software.

**Problem:** Small businesses need coherent transaction workflows, financial visibility and accountable controls, without confusing AI-generated explanations with accounting records.

**My work:** Next.js/TypeScript + PostgreSQL foundation; organization accounts, RLS tenant boundaries, ledger/journal design, chart of accounts, billing/payment allocation, CSV bank import, budget/actual reporting, audit engagements, evidence references and reviewer gates.

**Documented scope:** Exact-decimal double-entry records; immutable journals; period locks; management trial-balance/P&L and financial-position summaries; deterministic monitoring rules; read-only Groq explanation layer. The repository explicitly excludes some tax, year-end close, live bank-feed and verified evidence-file flows.

**Quality/ethics:** RLS tests, non-privileged app roles, separated migration role, deterministic calculations, staged migrations and reviewer separation. Outputs are **not** statutory financial statements, an audit opinion or regulatory certification.

**Evidence:** [Repository README](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software/blob/main/README.md).

### 06. CABO Human Capital — recruitment and workforce intelligence
**Repository:** [HR-Software](https://github.com/CayelaemJ/HR-Software)  
**Status:** Active demonstration and pilot-security development, *not* approved for genuine applicant or employee datasets.

**Problem:** Recruitment and employee operations need traceable evidence and reasons, not unexplained AI selection.

**My work:** Full-stack React/TypeScript + Express/PostgreSQL workflows, vacancies/candidate stages, provenance of qualifications and claimed skills, interviews/scorecards, employee operations and tenant-owned records. Authenticator-based MFA, tenant RLS, scoped operations and synthetic-demo controls are documented as evolving implementation phases.

**Principles:** Human review for hiring/compensation, explicit provenance, contested evidence, audit trails, privacy and retention, bias/fairness testing. Payroll export is a staged handoff, not a Sage or regulated payroll replacement.

**Evidence:** [Repository README](https://github.com/CayelaemJ/HR-Software/blob/main/README.md).

## CABO services, commerce and consumer experiences

### 07. CABO Solutions website and lead intake
**Repository:** [CABOSOLUTIONS](https://github.com/CayelaemJ/CABOSOLUTIONS)  
**Status:** Developed company website and enquiry API; public-ready operation depends on environment, backups, abuse prevention and privacy review.

**My work:** React/Vite/Three.js service presentation, responsive UI, Node.js enquiry endpoints, PostgreSQL persistence before success acknowledgement, admin-only review API and optional email notification. Corporate branding, usability, customer journey and deployment design are part of the work.

**Caution:** Sample showcased client work is illustrative unless independently consented and evidenced; README includes historic Railway instructions.

### 08. CABO Commerce / Botswana-first marketplace
**Repository:** [ecommerce-platform-for-botswana](https://github.com/CayelaemJ/ecommerce-platform-for-botswana)  
**Status:** Front-end/demo marketplace plus server-side fictional service-request queue; no real transactions.

**My work:** React shopping/search/cart, BWP-priced catalogue demo, simulated order milestones, seller views and multi-service prototype concepts: CABO Market, Now, Rides, Send and CrossBorder.

**Roadmap:** Secure seller/customer/driver accounts; inventory, payment-provider settlement/webhooks, delivery-zone logistics, consented GPS, verified merchants, dispute resolution and Botswana consumer/privacy compliance. None of this should be misrepresented as live payment or dispatch connectivity.

### 09. CABO Beauty / Grooming and beauty bookings
**Repository:** [Grooming-and-Beauty-Bookings](https://github.com/CayelaemJ/Grooming-and-Beauty-Bookings)  
**Status:** Customer-specialist booking and acceptance demonstration with PostgreSQL; not a production marketplace.

**My work:** React UI, booking states, server-side pricing, staff availability, transactional overlap protection, sessions and role-based admin; ZAR cents and Africa/Johannesburg booking semantics.

**Not yet live:** Provider verification, payment/payouts, GPS, emergency response, SMS, native Android/iOS and real-world professional marketplace operations.

### 10. CABO Artist Hub / artist career intelligence
**Repository:** [Artist-Management-Hub](https://github.com/CayelaemJ/Artist-Management-Hub)  
**Status:** Product prototype with fictional demonstration artists and staged account features.

**My work:** Artist discovery, private booking enquiries, management workflow, dashboard concepts for PR and Career Health indices, explanatory analytics, security controls, optional Groq support, recovery and notifications exploration.

**Do not overstate:** Synthetic social mentions and scores are not live social analytics or a medical assessment. Contracts, payments, invoices, verified industry integrations and fully hardened multi-user RBAC are not generally available.

## Supporting repositories and workspaces

### 11. Adhoc-Updates
**Repository:** [Adhoc-Updates](https://github.com/CayelaemJ/Adhoc-Updates). Supporting workspace; README was not found during this inventory. No technical claims made without code review.

### 12. Ecommerce-Platform-
**Repository:** [Ecommerce-Platform-](https://github.com/CayelaemJ/Ecommerce-Platform-). Currently reported empty by the connected GitHub interface; do not present as a delivered system.

### 13. c
**Repository:** [c](https://github.com/CayelaemJ/c). Minimal public README, insufficient evidence to describe a distinct product.

### 14. CayelaemJ / professional profile
**Repository:** [CayelaemJ](https://github.com/CayelaemJ/CayelaemJ). Public profile, case studies, career/skills matrix and project catalogue. This is documentation and employer-facing navigation, not production software.

## Additional work represented in conversation but not independently matched to a visible repository

- **OmniMaster / personal interactive engineering portfolio:** Website design, interactive case studies, Render hosting/recovery and weekly updates have been discussed. A currently active public URL and code ownership have **not** been verified in this repository inventory.
- **Cloudflare + Render infrastructure audit:** Staging-gated workers, queue systems, observability, tenant isolation tests, offline Docker checks and low-cost database evaluation span products rather than one repository. Work has varied from designs to PRs and local validation.
- **CABO native applications:** Kotlin/Android Studio and iOS development should appear as an active technical direction, but do not claim released apps until full feature parity, device tests and installable builds are proven.
- **Other CABO organization repositories:** The connected account did not expose additional organization repositories during this review; this inventory covers what was visible, not a claim that every organization repository has been audited.

## My delivery style and evidence standard

I combine SQL investigation, BI modelling, application/API development, UX, automated testing and infrastructure into one problem-solving practice. I prefer outcome-oriented case studies with **problem → constraints → architecture → my contribution → validation → status → next steps**. For confidential client engagements I describe techniques and approved metrics, not raw queries, customer data, credentials or employer proprietary artifacts.

*For detailed banking, manufacturing, FMCG, public-interest and financial-services case studies, see [CLIENT_CASE_STUDIES.md](CLIENT_CASE_STUDIES.md).*