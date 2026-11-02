# Professional engineering and data case studies
*Career evidence drawn from my master CV, prior reporting work and current project documentation · 2 November 2026.*

Client names and employment timelines reflect earlier CV material. These descriptions are an **experience record**, not a release certification or a claim that client-owned source code is publicly available. Figures below are those documented in the master CV and should be reconfirmed when used in high-stakes applications or client-facing marketing.

## 1. Bitberry / Bestbar — Australia: data platform, manufacturing and delivery analytics
**Role:** Contract data engineer and Power Automate engineer, January–August 2026 (remote, Western Australian operations).  
**Stack:** SQL Server/T-SQL, SSIS, SQL Server Agent, Power BI, DAX, Power Query M, Microsoft Fabric, Power Automate, ConnX, Dynamics GP, ERP and logistics event data.

**Challenge.** Multi-state rebar/mesh manufacturing and dispatch analytics were distributed across operational SQL databases and sensitive to dataflow failures, evolving query schemas and grain mismatches.

**My work.**
- Built SQL extracts, transformations, dataflows, reporting models and automated distribution as a sole data-engineering resource.
- Designed a scheduler-performance dashboard with a 15-temp-table SQL architecture across eight Australian states, 35 DAX measures and 11 relationships (as documented in my existing CV).
- Developed reporting for rebar/mesh stock and forecast, scrap and cutting production, workforce time versus output, production and delivery performance, near-real-time plant status and management PDFs.
- Implemented mill-certificate attachment workflows for new and backfilled messages, metadata extraction and organized storage.
- Diagnosed SQL deadlocks, cascading dataflows, pivot column drift, renamed columns, malformed event records and a mesh production-hours calculation in which a stored duration required minutes-to-hours conversion.

**A deeper logistics-data example.** Delivery KPIs were designed at **ManifestStatusID + Schedule# grain**, preserving multiple schedules attached to one manifest. Schedule joins needed both manifest and schedule keys; blindly joining on ManifestID duplicated tonnage, drops and costs. Carrier relationships were verified using the carrier table rather than guessed truck-type joins. Route plans could themselves have duplicate manifest IDs. Weight source, cost fields and status partitions were inspected independently. Per-drop distance and site/yard waiting-time source mapping still required GPS and timestamp validation, so these should be presented as investigations, not a fully shipped result.

**Engineering takeaways.** Data-model integrity is more important than adding measures quickly: establish grain, classify events, verify relationships, distinguish planned and completed facts and prevent silent overcounting.

## 2. Empower Financial Services — financial-wellness SaaS and reporting automation
**Role:** Data/BI, full-stack and software engineering, August 2026 onward.  
**Stack:** Node.js, TypeScript, Fastify, PostgreSQL/Prisma, React migration, SQL Server/MySQL read-only sources, API/file ingestion, Power BI/reporting concepts, scheduled SMTP.

**Challenge.** Employer and channel-partner users needed timely and governed financial-wellness analysis from several independent source formats without manual exports or ambiguous historical interpretation.

**My work.**
- Designed a multi-tenant employer/portfolio dashboard and channel-partner experiences, integrating data, dashboards, role-based admin, identity controls and branded exports.
- Worked with a ten-dataset canonical contract across API, read-only SQL views and file imports; separated source-change timestamps, business-event dates and historical “as at” reporting semantics.
- Developed null-safe score/driver logic, data-quality states, cohort comparisons, snapshot read modelling, indexed performance and import error handling.
- Designed scheduled reports, retry/delivery logging, model governance, audit records and privacy-aware reduction of personal ID usage in analytics.
- Supported accessible dashboard migration, security reviews and automated checks across permissions, data quality, integration, accessibility and release gates.

**Caveat.** Historical repo documentation still refers to Railway; later work moves toward Cloudflare/Render and evaluates Aiven. Do not claim a migration is completed without validated deployment/database state.

## 3. FNB — IQbusiness consulting: commercial/retail analytics
**Dates:** 2024–2025 engagements, Johannesburg and African market reporting.  
**Stack:** Power BI, DAX, Power Query, Microsoft Fabric, composite models, row-level security.

**My work.** Built commercial and retail trackers, a documented group of 18 dashboards across South Africa, Namibia, Botswana and Zambia; optimized dynamic DAX, access boundaries and transformations. Automated previously manual preparation and produced market-aware segmentation and performance reporting. Existing CV reports a **40% dashboard load-time improvement**; regard it as CV-reported, not independently benchmarked here.

## 4. Johannesburg Stock Exchange (JSE) — IQbusiness: support and HR reporting
**Dates:** July–December 2024.  
**Stack:** Power BI, Power Automate, SharePoint, Jira, DAX.

**My work.** Service desk SLA/resolution/breach analysis, HR operations dashboards and time-triggered extraction/reporting. Existing CV reports a **70% reduction in recurring manual reporting**, replacing a weekly 4–5 hour Excel process.

## 5. Diageo Africa — IQbusiness: large-scale brand analytics
**Dates:** April–December 2024.  
**Stack:** Power BI, Power Query M, DAX, SAP/Excel and research sources.

**My work.** Cleansing, modelling and visualizing a **270M+ survey-row** dataset according to prior CV; brand tracking, distribution, outlets, share and campaign reporting with data-quality rules. Focus: scalable model semantics, query efficiency and stakeholder-ready metrics.

## 6. AB InBev Africa — IQbusiness: commercial analytics and Fabric modelling
**Dates:** 2024–2025 client engagement, including senior-associate expansion.  
**Stack:** Fabric Lakehouse, Power Query, Power BI, DAX, source integrations.

**My work.** Data preparation across surveys, campaigns and sales, surrogate matching and performance tuning, and reporting for brand health, marketing campaigns, samples and outlets. Collaborated with business owners on definitions and review. Prior CV estimates a **35% reporting speed/accuracy improvement**; confirmation required for external use.

## 7. MultiChoice — CX, sentiment and broadcast operations
**Dates:** Internship Dec 2023–Jan 2024; IQbusiness client work 2024–2025.  
**Stack:** Power BI, Power Query, Python, MS Access SQL, automation.

**My work.** Analysed broadcast playout timing and automated Access-driven reports during internship; later built NPS/customer-service, repeat contact, SLA, cohort and sentiment reporting for media CX operations, combining social/call-centre sources and data preparation. Prior CV cites **60% faster analyst-ready insight** for the latter workstream.

## 8. VKB Group — agricultural enterprise BI
**Dates:** September 2025–January 2026.  
**Stack:** MDX, SQL Server and Microsoft NAV-derived reporting, Power BI, Power Automate, Power Apps, DAX.

**My work.** KPI definitions, dashboard maintenance, SQL/MDX reporting and automation. Prior CV cites a 50% shorter report cycle, 40% reporting-efficiency gain and 30% fewer manual data capture errors. Validated NAV staging and warehouse mappings.

## 9. Jozi My Jozi — social-impact analysis
**Dates:** May–September 2025, volunteer.  
**Stack:** Power Apps, SharePoint, Power BI.

**My work.** Shelter/admission/intervention/outcome capture, dashboard definitions, data quality, occupancy/throughput analysis, documentation and training for non-technical staff. Avoid publishing beneficiary-level data.

## 10. Seemanns Quality Meats — independent customer analytics
**Dates:** November–December 2022.  
**Stack:** R/RStudio, regression, segmentation, Excel/VBA.

**My work.** Customer purchase/survey analysis, buyer segments, business recommendations, a 25-page write-up and spreadsheet automation. Prior CV reports 15+ hours per week saved.

## Other standalone case studies
- **Customer churn:** University/independent statistical modelling, RFM features and classifier comparisons; any claimed impact on actual customers must be separated from test-cohort projections.
- **Sales forecasting and logistics P&L:** Forecasting, truck-cost/profitability concepts and reporting for manufacturing operations; distinguish synthetic data from real operational outcomes.
- **Discovery Bank rewards prediction experiment:** Personal experimental model; prior CV records 6 of 10 predictions correct. Not an official bank product.
- **NIQita:** Early AI chatbot research, Teams/SharePoint workflow concepts, sentiment and operational design.
- **People Sense:** Survey analysis, API integrations and dashboards relating geography and self-reported perceptions.
- **Power BI embedding and interactive web reporting:** React/JavaScript and client-facing embedded analytics.
- **Teaching and knowledge transfer:** BI/data/analytics workshops and full-stack data masterclass material, stakeholder walkthroughs and junior analyst mentoring.

## Collaboration and delivery pattern
Requirements and evidence gathering → source systems and grain → transformation/semantic model → user-facing visualization/API → security and permissions → automated tests and operational checks → stakeholder review → documentation/handover. Comfortable working directly with nontechnical leaders and coordinating with remote Australian time zones.

**Privacy:** Client examples are intentionally descriptive. Source datasets, employer identity records, authentication secrets and internal code do not belong in a public portfolio.