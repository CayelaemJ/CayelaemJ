# Human Interface 02 | What actually matters to people

[← My UX journey](01_MY_UX_JOURNEY.md) · [Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: Case studies →](03_UX_CASE_STUDIES.md)

An interface is a contract between a person and a system. The person brings a goal, attention limits, habits, abilities and sometimes stress. The system should make the goal achievable without asking them to understand its internal architecture.

## The fundamentals I keep returning to

### 1. Start with the task, not the screen

Don't begin with “we need five dashboard cards.” Begin with “the operations manager needs to know which deliveries require action **today**.” The first version might be a prioritised queue, not a complicated dashboard.

**Exercise:** rewrite a feature request into **user → need → context → successful outcome**.

### 2. Make system status visible

People should know whether a task is loading, saved, failed, waiting for approval or genuinely complete. A spinner with no explanation cannot distinguish a slow request from a broken one.

**Good pattern:** “We received the file. 42 rows validated; 3 need correction. Nothing has been published yet.”

### 3. Speak the user's language

“Foreign key constraint violation” is actionable to a database engineer, not necessarily to an educator or payroll specialist. Translate technical failure into user-facing meaning while preserving a diagnostic reference for support.

**Useful error structure:** what happened → whether data was changed → what the user can do → where to get help.

### 4. Minimise memory and cognitive load

A user should not have to remember an identifier from a previous page or infer what an unlabeled icon means. Show relevant context, group related options and use defaults only when they are safe.

### 5. Make actions predictable and recoverable

Destructive changes deserve confirmation when consequences are significant. Avoid surprise navigation, silent writes and ambiguous double submissions. Provide undo or recovery where possible.

### 6. Design for varied access

Keyboard access, focus visibility, reduced motion, readable text, sufficient contrast, zoom, touch targets and assistive technologies are part of the experience. A mobile layout is not simply a desktop dashboard squeezed smaller.

### 7. Protect trust

If a dashboard is delayed, tell the user. If AI is suggesting a grade, distinguish a suggestion from an accepted decision. If permissions limit a view, explain the limitation without revealing restricted information.

## A simple before-and-after exercise

**Before:** “Sync failed. Error 500.”

**After:** “We couldn't finish syncing the file. No new records were published. Your uploaded file is still available for review. Try again, or use reference SYNC-104 when contacting support.”

The second message assumes the system actually guarantees those facts. Never claim a transaction rolled back unless it did. UX copy must agree with backend behaviour.

## The trade-offs I consider

| UX choice | Benefit | Risk to evaluate |
|---|---|---|
| Automatic save | Less manual effort | Hidden uncertainty about persistence or conflict |
| Wizard onboarding | Reduced complexity per step | Long workflow or hidden navigation |
| Dense dashboard | More information in one place | Poor scanability, especially on mobile |
| One-click destructive action | Fast operation | Irreversible mistakes |
| AI-generated explanation | Potentially clearer interpretation | False certainty and provenance loss |
| Role-aware navigation | Relevant options and less clutter | A hidden button must not replace server permissions |

## Build a human task-flow map

~~~mermaid
flowchart TD
    START["Person has a goal"] --> FIND{"Can they find the task?"}
    FIND -->|"No"| NAV["Improve naming and navigation"]
    FIND -->|"Yes"| ACT["Take action"]
    ACT --> RESULT{"System response?"}
    RESULT -->|"Success"| CONFIRM["Clear confirmation and next step"]
    RESULT -->|"Error"| RECOVER["Explain state, recovery and support"]
    RESULT -->|"Waiting"| PROGRESS["Show progress and expected behaviour"]
~~~

I use flows like this to connect screen states to technical states. Every arrow should correspond to an action the person understands or an observable state the system can actually guarantee.

## What to measure

Don't rely only on visual preference. Observe **task completion**, wrong turns, hesitation, repeated clicks, time-to-understanding and ability to recover from an error.

A usability test with three people will not establish population-wide confidence, but it can reveal obvious problems. Use research ethically, avoid collecting more personal data than needed, and report the limitations of the sample.

## Your assignment

Take an existing upload form or reporting dashboard. Define three user tasks, create one intentional error case and ask a peer to attempt the workflow. Write down observable behaviour without coaching them.

**Pass condition:** you identify at least one change justified by an observation and can explain how the system will behave afterward.

[← My UX journey](01_MY_UX_JOURNEY.md) · [Next: Case studies →](03_UX_CASE_STUDIES.md)
