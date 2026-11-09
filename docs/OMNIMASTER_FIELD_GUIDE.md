# THE OMNIMASTER FIELD GUIDE
### Volume II of my living engineering textbook

**Cayelaem Jantjies · Engineering architectures, investigations, working exercises and technical conversations · November 2026**

[← Return to the main handbook](OMNIMASTER_HANDBOOK.md) · [GitHub profile](../README.md) · [Runnable labs](../projects/README.md)

---

> The main handbook explains where I came from and the systems I work on. This volume opens the engine room: the boundaries, choices, breakages and practical questions that shape my approach.

This is a companion to my ten-chapter [OmniMaster Handbook](OMNIMASTER_HANDBOOK.md). Read it as an engineering field manual and an invitation to inspect my thinking.

## Start where your curiosity leads

| Reader | Starting point | What you'll discover |
|---|---|---|
| **Recruiter or hiring manager** | [04 · Role and evidence navigator](field-guide/04_ROLE_AND_EVIDENCE_MAP.md) | My experience, roles I fit, concrete project references and honest limitations |
| **Data engineer / architect** | [01 · Annotated architecture atlas](field-guide/01_ARCHITECTURE_ATLAS.md) | End-to-end boundaries, CDC, semantics, AI and security |
| **Senior engineer / reviewer** | [02 · The debugging casebook](field-guide/02_DEBUGGING_CASEBOOK.md) | Failure symptoms, competing hypotheses, investigations and safe fixes |
| **Interview panel** | [03 · Engineering workbook](field-guide/03_ENGINEERING_WORKBOOK.md) | Worked problem-solving scenarios, tests and discussion prompts |
| **Technical lead** | [05 · Architecture decision journal](field-guide/05_DECISION_JOURNAL.md) | Trade-offs, alternatives, decision criteria and release evidence |

## Volume II chapters

1. [**Architecture atlas:** trace systems from operational truth to user outcome](field-guide/01_ARCHITECTURE_ATLAS.md)
2. [**Debugging casebook:** how I investigate things that break](field-guide/02_DEBUGGING_CASEBOOK.md)
3. [**Engineering workbook:** exercises, answers and reproducible code](field-guide/03_ENGINEERING_WORKBOOK.md)
4. [**Role and evidence map:** a guided tour for a recruiter or technical leader](field-guide/04_ROLE_AND_EVIDENCE_MAP.md)
5. [**Decision journal:** design records and the trade-offs they expose](field-guide/05_DECISION_JOURNAL.md)

## The central system question

~~~mermaid
flowchart LR
    P["People & business problem"] --> S["Source facts & constraints"]
    S --> E["Engineering decision"]
    E --> I["Implementation"]
    I --> V["Evidence & tests"]
    V --> O["Operating outcome"]
    O -->|"new information"| P
~~~

A strong engineer can move around this loop in either direction. From a failed KPI, trace the measure back to source records. From a security flaw, find the trust boundary. From an attractive product proposal, isolate the business event and the operating cost.

I want these materials to show **how I reason**, not invent achievements. Where a client record cannot be published, I use an explicitly hypothetical illustration. Where the public code contains unfinished work, I name the issue or pull request instead of claiming release success.

## Companion volumes and evidence

- **Volume I:** [The OmniMaster Handbook](OMNIMASTER_HANDBOOK.md), the career narrative and ten technical chapters.
- **Volume III:** [The OmniMaster Academy](OMNIMASTER_ACADEMY.md), seven study modules and capstone blueprints.
- **Volume IV:** [The Person Behind the Code](OMNIMASTER_OPERATING_MANUAL.md), INTJ as self-description and my approach to working across IT.
- **Arcade:** [The OmniMaster Arcade](OMNIMASTER_ARCADE.md), learning puzzles and a runnable incident game.
- **Volume V:** [Build a System With Me](OMNIMASTER_BUILD_WITH_ME.md), six guided lessons and a runnable end-to-end synthetic data platform.
- **Volume VI:** [The Human Interface](OMNIMASTER_HUMAN_INTERFACE.md), UI/UX development, accessibility, human research and measurable usability.
- **Daily practice:** [30-Day Engineering Expedition](THIRTY_DAY_ENGINEERING_EXPEDITION.md) and [offline interactive study room](interactive/index.html).
- **Source archive:** [Project portfolio atlas](PROJECT_PORTFOLIO.md) and [real-world mission dossiers](OMNIMASTER_MISSION_DOSSIERS.md).
- **Professional engagements:** [Client case studies](CLIENT_CASE_STUDIES.md), subject to appropriate confidentiality.
- **Code you can run:** [Four synthetic engineering labs](../projects/README.md), with tests and CI.
- **Live engineering issues:** [The Fixer](https://github.com/CayelaemJ/NewChanges/issues) and [Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub/issues), where some work is intentionally not declared complete.

**Evidence standard:** a design diagram is not proof of deployment. A scenario is not a disclosed client incident. A green unit test is not an operational acceptance test. A career metric from my CV is reported history, not a new benchmark.

[Begin with the architecture atlas →](field-guide/01_ARCHITECTURE_ATLAS.md)
