# THE OMNIMASTER ACADEMY
### Volume III | Learn the engineering habits, build the systems, and explain the decisions

**A practical study guide by Cayelaem Jantjies · November 2026**  
[GitHub cover](../README.md) · [Volume I: My story](OMNIMASTER_HANDBOOK.md) · [Volume II: Field guide](OMNIMASTER_FIELD_GUIDE.md) · [The person behind the code](OMNIMASTER_OPERATING_MANUAL.md)

---

> Don't copy my job titles. Copy the process: understand the business event, reproduce the bug, model the facts, build the workflow, test the boundaries, and explain the trade-offs.

This is the part of my GitHub where I try to make myself *replaceable in the best possible way*: anyone who is curious and willing to practise should be able to follow the same engineering principles. It doesn't promise you my career or turn six weeks of tutorials into a senior engineer. It gives you a route from a blank repository to a defensible project.

**Who it's for:** a student, career-switcher, BI analyst moving toward engineering, software developer learning data, or engineer curious about applied AI and delivery.

**Cost and access:** the main exercises use Python, SQLite, Git and a code editor. They're designed to run locally with synthetic data, without an AWS account, paid AI API or work-owned credentials.

## Pick a route

| Track | Best for | Start |
|---|---|---|
| **New to engineering** | Build foundations one boundary at a time | [01 · Learn how to learn](academy/01_START_HERE.md) |
| **Already working in BI** | Move upstream to SQL, pipelines, contracts and APIs | [02 · The data model](academy/02_SQL_AND_MODELLING.md) |
| **Already building apps** | Make data and access boundaries trustworthy | [04 · Full-stack workflows](academy/04_BUILD_APPLICATIONS.md) |
| **Curious about applied AI** | Add models to workflows without trusting unvalidated output | [05 · Applied AI with guardrails](academy/05_APPLIED_AI.md) |
| **Preparing for senior interviews** | Prove understanding through negative tests and release criteria | [06 · Security and delivery](academy/06_SECURITY_AND_DELIVERY.md) |
| **Want a portfolio piece** | Build and explain an entire system | [07 · Capstones and evidence](academy/07_CAPSTONES.md) |

## The seven modules

1. [**01. Think like an investigator:** define the problem, tools and learning journal](academy/01_START_HERE.md)
2. [**02. SQL and modelling:** business grain, joins, measures, indexing and tests](academy/02_SQL_AND_MODELLING.md)
3. [**03. Reliable data movement:** ingestion, quality, CDC, retries and history](academy/03_PIPELINES_AND_CDC.md)
4. [**04. Full-stack engineering:** APIs, state transitions, tenant scope and UI](academy/04_BUILD_APPLICATIONS.md)
5. [**05. Applied AI responsibly:** evidence, evaluation, costs and human review](academy/05_APPLIED_AI.md)
6. [**06. Security, testing and release:** negative paths, CI and rollback](academy/06_SECURITY_AND_DELIVERY.md)
7. [**07. Capstones:** combine the layers into a real portfolio narrative](academy/07_CAPSTONES.md)

## A suggested 12-week route

| Weeks | Focus | Minimum evidence you should produce |
|---|---|---|
| 1–2 | Tools, data grain, SQL and modelling | A reproducible source table, schema, query tests and explanation |
| 3–4 | Ingestion, contracts, state changes and replay | Synthetic ETL/CDC simulation, duplicate/deletion tests and failure diary |
| 5–6 | API + database + minimal interface | Authenticated CRUD-style workflow, tests, schema and clear error behaviour |
| 7–8 | Applied AI and risk assessment | Offline evaluator, test cases, human-review logic and explicit no-model fallback |
| 9–10 | CI, secrets, release rehearsal | Automated tests, negative cases, restore/rollback document |
| 11–12 | One capstone and evidence-led communication | README, architecture diagram, demo steps, trade-offs, what failed, what's next |

This is a **suggested study cadence**, not a promise of completion or a qualification. Repeat any module until you can explain it without copying an answer.

## How to measure learning

Use **evidence**, not hours of videos watched. At the end of a module, ask:

1. Can I reproduce the behaviour from clean inputs?
2. Can I explain why the design has this grain and these boundaries?
3. Which failure case did I intentionally create?
4. Can a stranger run the test without my machine or credentials?
5. What remains unproved, and how would I verify it in production?

Write one short engineering journal entry after each module: **problem → hypothesis → experiment → result → decision → remaining risk**.

## Practice repository

Start with the four [public engineering labs](../projects/README.md). They include a CDC replay, data quality contracts, SQL query plans and a synthetic source-grounding evaluator. Next, play the [OmniMaster Incident Academy game](../projects/omnimaster-incident-academy/) to practise reasoning about failure modes.

For worked explanations and reviewer questions, use the [Volume II workbook](field-guide/03_ENGINEERING_WORKBOOK.md). For the story behind these habits, read [Why I work this way](personal/02_WHY_I_THINK_IN_SYSTEMS.md).

## The rules of this classroom

- Never paste employer data, production secrets or real learner/customer records into a tutorial.
- Do not present a lab as a production CDC service, live AI system or security certification.
- Prefer a boring correct solution to an impressive untestable one.
- Record what you couldn't solve. That is how a useful engineering notebook starts.
- Learning a language is not the same thing as understanding its underlying system.

**Graduation means you have a project that another engineer can question, run and improve.** There is no imaginary certificate. Your source, tests and explanations are the credential.

## Go beyond the course

[**Volume V: Build a System With Me**](OMNIMASTER_BUILD_WITH_ME.md) supplies a complete fictional SQLite pipeline with six guided engineering chapters, replay and failure tests. [The 30-day expedition](THIRTY_DAY_ENGINEERING_EXPEDITION.md) turns the syllabus into daily artifacts. For a more playful format, open the [live interactive Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/) in any browser.


[Start lesson 01 →](academy/01_START_HERE.md) · [Try the arcade →](OMNIMASTER_ARCADE.md)


**Design for people:** [Volume VI](OMNIMASTER_HUMAN_INTERFACE.md) adds a six-chapter UI/UX development and usability course.


### Read lessons without opening GitHub

The [live OmniMaster Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/) serves all Academy lessons directly as readable HTML. The [frontend/backend book](https://omnimaster-study-room.cabo-solutions-za.workers.dev/OMNIMASTER_FULLSTACK_PLAYBOOK.md) and its [PDF edition](https://omnimaster-study-room.cabo-solutions-za.workers.dev/downloads/omnimaster-fullstack.pdf) are part of the same public learning experience.
