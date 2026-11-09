# Reliability Chapter 04 | Truthful frontend status and operational UX

[← Dead letters](03_DEAD_LETTERS_AND_RECONCILIATION.md) · [Volume VII](../OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) · [Next: Production boundaries →](05_PRODUCTION_BOUNDARIES.md)

## A backend failure becomes a human experience

I have learned that an interface can be technically valid and still lie to its user. The common pattern is simple: an action is queued, a network response is late, and the UI announces success because it received *something*.

In a reliable product, **the language of the interface must correspond to a genuine system state**.

## Frontend status contract

| Backend truth | Avoid saying | Say something useful instead |
|---|---|---|
| Queued but not attempted | "Completed" | "Your task has been queued" |
| In progress | "Saved" | "Processing; you can check its status here" |
| Retry scheduled | "Failed" without context | "We're retrying after a temporary problem" |
| Automatic retries exhausted | "Try again" as if risk-free | "This needs review before another attempt" |
| Local effect committed | "Everything sent" when external outcome unknown | "Local processing finished; delivery confirmation pending" |
| Result unknown after timeout | "Nothing happened" | "We couldn't confirm the result; check status before retrying" |

Every sample message must be backed by real behaviour before it is used in a production product.

## A UI component is a state machine in disguise

The frontend needs a typed status contract, accessible labels, focus management and careful error recovery. A status view could show:

~~~tsx
type JobStatus =
  | { state: "queued"; id: string }
  | { state: "retrying"; attempt: number; nextCheckAt: string }
  | { state: "done"; completedAt: string }
  | { state: "needs_review"; incidentId: string }
  | { state: "unknown"; id: string };

function JobNotice({ job }: { job: JobStatus }) {
  switch (job.state) {
    case "queued": return <p role="status">Queued. Reference {job.id}.</p>;
    case "retrying": return <p role="status">Attempt {job.attempt} failed; retry planned.</p>;
    case "done": return <p role="status">Processing finished at {job.completedAt}.</p>;
    case "needs_review": return <p role="alert">Review required. Case {job.incidentId}.</p>;
    case "unknown": return <p role="status">Outcome not confirmed. Check reference {job.id}.</p>;
  }
}
~~~

This is a **teaching fragment**, not a full authenticated React application. In a real system, UI status must be fetched from a backend endpoint authorised for the user's verified identity and tenant.

## Reliability is also information architecture

A frustrated user should not have to understand message brokers, transaction logs or process IDs. They need to know whether to **wait, retry, review, cancel or contact support**.

An operator needs richer detail: attempt history, failure category, correlation ID, source state, last successful checkpoint, incident owner and safe remediation options.

The two interfaces serve different people and should not simply render the same raw JSON.

## How I would validate the experience

1. Give a participant a fictional task and deliberately make the source fail.
2. Ask them to interpret the status without explaining the system.
3. Observe whether they click Retry repeatedly or wait when appropriate.
4. Test a lost response after a committed action.
5. Verify keyboard access, screen-reader announcements and mobile layout.
6. Compare every displayed promise with the actual backend state.

This is a proposed usability method, not a claim that a formal study has already been completed.

## What metrics would help?

| Metric | Why it matters |
|---|---|
| Oldest due job age | Identifies backlog and stalled work |
| Retry count by error category | Distinguishes dependency instability from invalid input |
| Dead-letter count and age | Reveals tasks needing human attention |
| Time to verified completion | Connects processing performance to user expectation |
| Status uncertainty rate | Measures lost/ambiguous outcomes |
| Cross-tenant denial tests | Confirms that status visibility is not a data leak |

Avoid collecting sensitive content as a shortcut for observability. Structured, minimal event metadata is usually preferable.

**Pass criterion:** a person knows what the system has actually completed and how they should proceed without understanding the infrastructure.

[Next: Production design →](05_PRODUCTION_BOUNDARIES.md)
