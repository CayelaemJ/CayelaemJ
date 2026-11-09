# Human Interface 06 | Practical UI/UX workbook

[← Measuring usability](05_MEASURE_USABILITY.md) · [Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Academy](../OMNIMASTER_ACADEMY.md)

This workbook teaches you to improve an interface through observation, not by guessing which design trend is fashionable.

All scenarios use fictional data. You can work in plain HTML, React or a design tool, but at least one exercise must become a usable browser interaction.

## Mission A. Rewrite a confusing flow

**Scenario:** a fictional integration platform has four identical-looking buttons: Test, Preview, Stage and Sync.

**Goal:** distinguish operations with labels, descriptions and appropriate confirmation.

**Deliverable:** a before/after flow diagram and prototype.

**Pass criterion:** a new user can correctly explain which actions read data and which persist changes before clicking.

<details>
<summary>My reasoning</summary>

I would show tasks in the order users need them, explain consequences and make the confirmed durable-write step distinct. “Preview” should be clearly read-only. The response must reflect actual backend semantics.

</details>

## Mission B. Fix an error message

**Scenario:** “Error 500: upload failed.”

**Goal:** help a user recover without falsely claiming that nothing changed.

**Deliverable:** error-state component with message, reference ID and safe next step.

**Pass criterion:** the person knows whether to retry, inspect a status or contact support. Verify every factual promise against backend behaviour.

## Mission C. Redesign a dashboard for a phone

**Scenario:** a desktop dashboard contains twelve cards, a wide chart and four global filters.

**Goal:** prioritise the one operational decision the person needs on a narrow screen.

**Deliverable:** mobile wireframe, prioritisation rationale, reflow and keyboard/touch check.

**Pass criterion:** the primary task can be completed without zooming to find an unlabeled control.

## Mission D. Make a chart accessible

**Scenario:** status is shown using red, amber and green lines with no textual explanation.

**Goal:** communicate series, units, changes and actions without colour-only meaning.

**Deliverable:** accessible chart label, legend, text equivalent and summary table.

**Pass criterion:** a user can determine the important status using text alone.

## Mission E. Build a form people can repair

**Scenario:** a school assessment form clears all answers after one invalid field.

**Goal:** preserve valid work, identify the problem and communicate what was and was not saved.

**Deliverable:** form states, validation strategy and failure simulation.

**Pass criterion:** a user corrects the field and completes the task without unnecessary re-entry.

## Mission F. Design a human AI review

**Scenario:** an AI system suggests a learner grade with a quote from an approved passage.

**Goal:** ensure the educator can examine, reject or correct the suggestion.

**Deliverable:** review screen with source evidence, rubric boundaries, audit note and explicit approve/reject state.

**Pass criterion:** the grade is not silently accepted because the model sounded confident.

## Mission G. Repair a broken link journey

**Scenario:** a prominently labelled “Launch interactive experience” link opens a source-code viewer.

**Goal:** fix the information architecture and destination.

**Deliverable:** live-page link, separate source link and a user-journey test.

**Pass criterion:** the visitor reaches the interactive page and completes its first action; not merely a 200 response for a repository README.

## Mission H. Run a usability mini-study

Recruit a willing participant using fictional content. Give them one task without coaching. Record completion, errors, confusion and recovery. Document the problem, propose an intervention, retest and disclose the sample size.

**Deliverable:** one-page research note with observation and follow-up test.

**Pass criterion:** the change follows evidence rather than personal preference.

---

## A simple UX review rubric

| Area | Weak | Better | Strong |
|---|---|---|---|
| **Discoverability** | User guesses where to go | Navigation is labelled | The intended task is obvious and findable |
| **Clarity** | Jargon or unlabeled metrics | Helpful labels | Purpose, scope, period and consequences are clear |
| **Feedback** | Silent request | Success/error message | Accurate status, next step and recovery |
| **Accessibility** | Mouse/colour only | Basic semantic controls | Keyboard, contrast, focus, zoom and assistive-tech checks |
| **Responsive design** | Overflow | Screen fits | Priority and workflow adapt to device |
| **Trust** | Stale or AI output looks definitive | Some caveats | Provenance, uncertainty and decision ownership explicit |
| **Evidence** | “Looks good” | Peer opinion | Observed task outcomes and tested revisions |

Score yourself by identifying the weakest criterion and fixing it. A subjective sum across categories is not a certification.

## The personal challenge

Take one interface from your public portfolio. Explain **who it serves, what success means, which details matter to the user, and what you changed after observing friction**.

That is the kind of UI/UX case study I want to build more of: actual reasoning and measured improvement rather than a screenshot gallery.

[← Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [My UX story](01_MY_UX_JOURNEY.md) · [Interactive Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)
