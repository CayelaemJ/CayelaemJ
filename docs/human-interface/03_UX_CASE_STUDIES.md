# Human Interface 03 | UI/UX case studies from my engineering work

[← Human-centred design](02_HUMAN_CENTRED_DESIGN.md) · [Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: Design systems →](04_DESIGN_SYSTEMS_AND_ACCESSIBILITY.md)

These are **practice-based design analyses** informed by projects I've worked on. Some features are implemented in public source; others are design decisions or active workstreams. They are not presented as completed formal user-research studies.

## 01. The Fixer: make importing data understandable

**Context:** source connections, staged ingestion, validation, synchronisation and administrative workflows.  
**Public evidence:** [NewChanges](https://github.com/CayelaemJ/NewChanges).

### User goal

A permitted user wants to connect a source, understand what is being imported, fix errors and know whether the records are actually synchronised.

### UX risks

- Buttons called “Test,” “Preview,” “Stage” and “Sync” can look interchangeable even though their consequences differ.
- A successful connection does not mean data is valid or published.
- An ambiguous error may encourage repeated submission and duplicate actions.
- Advanced settings can overwhelm users who only need to complete a routine import.

### A clearer task design

1. **Select source:** show supported types and exactly what credentials are required.
2. **Test access:** communicate connection status without claiming data was imported.
3. **Preview:** show representative, access-scoped records and field mappings.
4. **Validate:** group issues by field, row and action needed.
5. **Confirm and sync:** distinguish draft/staging from durable publication.
6. **Review result:** show processed, rejected, skipped and pending counts from authoritative backend state.

**Review criterion:** a new user can tell whether a preview is read-only, when records become durable and what happens after failure.

### Engineering connection

The UI must reflect the real transaction boundary. The [Fixer security workstream](https://github.com/CayelaemJ/NewChanges/pull/233) highlights the same principle in email delivery: a message sent and an audit status saved are separate outcomes. The interface shouldn't turn one into a misleading generic failure.

## 02. Enterprise BI: visual clarity is analytical correctness

**Context:** banking, commercial research, Australian manufacturing and operational reporting.  
**Evidence:** [Professional case studies](../CLIENT_CASE_STUDIES.md).

### User goal

A stakeholder wants to identify the correct trend or exception and act, often under time pressure.

### UX risks

- An attractive chart can conceal the measure's grain.
- Colour alone cannot safely communicate a critical status.
- Important filters may be hidden, duplicated or silently persisted.
- A dashboard can look current when its source is stale.
- Dense layouts can become unusable on smaller screens.

### My design principles

Give each important measure a clear unit, time period, definition and context. Emphasise comparisons that answer a known decision. Put exceptions ahead of vanity metrics. Make the date range, market and source freshness visible where they change interpretation.

**Review criterion:** the intended audience can explain what a KPI counts and which period or organisation it represents.

**Evidence limit:** historical performance and data-volume metrics are CV-reported; this chapter does not claim a formally measured UX uplift.

## 03. CABO Learning Hub: one platform, very different people

**Context:** learners, guardians, teachers and administrative roles.  
**Public evidence:** [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub).

### Different user needs

| Person | Common goal | Design priority |
|---|---|---|
| Learner | Understand a task and improve | Age-appropriate clarity, motivation and readable feedback |
| Teacher | Plan, assign and review work | Efficient workflows, correct cohort scope and controllable assessments |
| Guardian | Follow progress safely | Understandable summaries, lawful access and contextual explanations |
| Administrator | Manage institutions, transfers and policies | Accurate state changes, warnings and auditability |

A single screen cannot serve all these contexts by merely hiding menu items. The information architecture, language, navigation depth and permissions must be evaluated for each role.

### One concrete failure class

In an active progression review, a previously loaded candidate list could become inconsistent with a newly selected academic year. The UI must bind decisions to the **reviewed year and candidate context**, invalidate stale selections and recheck server-side.

[Year-end progression issue](https://github.com/CayelaemJ/Training-and-Development-Hub/issues/163).

**Review criterion:** a teacher cannot accidentally submit a cohort progression against a different year after changing a filter.

**Evidence limit:** broad child-data, inclusive design and cross-country governance goals remain subject to implementation and relevant legal review.

## 04. Mobile interfaces and visual regression

**Context:** responsive layouts, iOS/Android parity and dashboard theme testing in The Fixer and mobile workstreams.

A desktop interface may rely on hover, wide tables and fine-grained controls. Phones demand sensible touch targets, readable charts, navigation that does not hide state and appropriate platform behaviour.

My work includes test-driven attention to **mobile fit, dark mode, theme correctness, chart rendering and accessibility**. Automated screenshots and layout checks are useful, but they cannot tell whether a real person understands the workflow.

**Review criterion:** complete a task on a narrow viewport using touch and keyboard input as relevant, with readable error messages and no horizontal data loss.

## 05. OmniMaster Study Room: the link *is* part of usability

**Context:** a public technical learning site built from this GitHub repository.

The initial “Interactive Study Room” link targeted a GitHub source file. GitHub showed the HTML source instead of the interactive experience. The code existed, but the user's task failed at navigation.

**Repair:** host the HTML as a real website and label its source code separately. Then confirm that local progress and scenario interactions work and that source/lesson links go to useful reading material.

**Review criterion:** someone clicking “Launch Study Room” sees an interactive page rather than a code viewer.

This is a practical example of a UX defect caught by actual feedback, not a fabricated user-study result.

## A review framework you can reuse

For any interface, write **who it serves → what they must do → where they may fail → how the UI responds → what system truth it relies on → how to verify usability**.

That is the relationship between design and full-stack engineering I want my portfolio to demonstrate.

[← Human-centred design](02_HUMAN_CENTRED_DESIGN.md) · [Next: Design systems →](04_DESIGN_SYSTEMS_AND_ACCESSIBILITY.md)
