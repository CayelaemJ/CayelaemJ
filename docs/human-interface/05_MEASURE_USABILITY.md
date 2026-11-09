# Human Interface 05 | Testing whether an experience works

[← Design systems](04_DESIGN_SYSTEMS_AND_ACCESSIBILITY.md) · [Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: UX workbook →](06_UX_WORKBOOK.md)

**A successful build is not evidence that a person completed their task.** My experience engineering reporting and applications taught me to care about functional correctness. UX requires an additional question: can a person find, understand and accomplish the goal in their context?

## Define a testable task

Bad test: “What do you think of this dashboard?”

Better task: “Find the three deliveries needing attention today, and explain which one you would investigate first.”

The second reveals navigation, information hierarchy, comprehension and decision-making. It doesn't ask the participant to validate your taste.

## Five practical measurements

| Measurement | What it tells us | Limitation |
|---|---|---|
| **Task completion** | Did the person reach the defined result? | A completion can still be slow or stressful |
| **Time on task** | How much effort does the journey require? | Faster is not always better for consequential decisions |
| **Error rate** | How often are mistakes or invalid submissions made? | System constraints can create artificial errors |
| **Recovery success** | Can the person correct an error without help? | Requires a meaningful error scenario |
| **Understanding / confidence** | Can they interpret the result and next action? | Self-reported confidence isn't proof of correctness |

For data-heavy interfaces, include **time to correct insight**: how long until the user identifies the actual business exception, not merely a visible number.

## How I'd run a small study

1. **Choose a representative task** and one realistic scenario.
2. **Recruit an appropriate participant** with consent; explain purpose and privacy.
3. **Avoid leading language.** Ask what the person expects the control to do.
4. **Observe actions and hesitation** without teaching during the task.
5. **Record outcome**, errors, confusing labels, and recovery attempts.
6. **Change one high-impact issue** and test the revision.
7. **Report limitations:** small samples produce leads, not statistical certainty.

You can start with a colleague and fictional data, but don't claim broad user validation from one session.

## Ethical research boundaries

Do not record sensitive financial, school or employee records simply because a test involves such a product. Use approved fictional accounts and get permission before collecting video, audio, feedback or identifiers. Store only what the study needs, restrict access and set a retention plan.

If a participant needs assistive technology, let them use their normal setup; don't treat accessibility as a trick question.

## Example usability study: the Study Room link

**Observed feedback:** a reader clicks “Interactive Study Room” and lands in GitHub's HTML source viewer instead of a usable learning interface.

**Task:** open the study room and answer the first question.

**Original outcome:** task blocked at navigation.

**Intervention:** host the HTML as an actual web experience, replace the prominent link, and retain a separate link for source inspection.

**Acceptance check:** the live URL returns a rendered HTML page and the first scenario can be selected and explained using keyboard or pointer. Check the deployment and real browser behaviour separately; a CI source check alone is not enough.

A small bug, but a useful teaching example of why **link destination, naming and expectation are UX work**.

## A study report template

~~~text
Study objective:
User group / context:
Task:
What success looks like:
Device / accessibility context:
Consent and data policy:
Observed completion:
Wrong turns and errors:
Where the participant hesitated:
Direct quotes (with permission):
Interpretation versus actual observation:
Proposed change:
Verification after change:
Remaining uncertainty:
~~~

## Don't optimise the wrong thing

A page loading in 400 milliseconds is irrelevant if people cannot find the action. A high click-through rate can be misleading if users click repeatedly because feedback is absent. A beautiful graph is not a correct business explanation.

Metrics should connect to **human outcomes** and system correctness, not simply demonstrate activity.

## Learning exercise

Take the [OmniMaster Arcade](../OMNIMASTER_ARCADE.md) or [online Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/). Ask a friend to begin a scenario with no instructions. Observe whether they understand the choices, find feedback, navigate to the next case and interpret their progress.

Write three improvements ranked by impact and effort. Implement one, then test again.

[← Design systems](04_DESIGN_SYSTEMS_AND_ACCESSIBILITY.md) · [Next: UX workbook →](06_UX_WORKBOOK.md)
