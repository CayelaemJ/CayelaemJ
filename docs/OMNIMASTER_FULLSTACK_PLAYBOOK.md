# THE OMNIMASTER FULL-STACK PLAYBOOK
### Frontend, backend, and everything that joins them
**Cayelaem Jantjies · Engineer's field textbook · Edition 2026**

[GitHub cover](../README.md) · [UI/UX development](OMNIMASTER_HUMAN_INTERFACE.md) · [Volume V: Build with me](OMNIMASTER_BUILD_WITH_ME.md) · [Interactive full-stack reader](fullstack/index.html)

---

> I don't call myself full-stack because I happen to know a frontend framework and a database. I use it to describe the work of turning a business need into a usable interface, a reliable API, a trustworthy data model, and a system people can operate.

My foundation is Statistics and Data Science. Professional work across banking, manufacturing, research, broadcasting, agriculture and social-impact analytics gradually pushed me upstream and downstream: source SQL, data transformations, dashboards, APIs, backend services, React interfaces, testing, security and cloud delivery. I grew curious about **why the whole system behaves as it does**, not just which line of code renders the answer.

This is a practical introduction to the separation between **frontend**, **backend**, and **full-stack integration**. It is for learners, recruiters and engineering reviewers. The exercises are synthetic and reproducible. They are not claims of production security certification or a transcript of private customer systems.

## Contents

1. [What is actually different?](#1-frontend-vs-backend-vs-full-stack)
2. [Frontend engineering: what people experience](#2-frontend-what-people-experience)
3. [Backend engineering: what the system guarantees](#3-backend-what-the-system-guarantees)
4. [A complete feature: from click to committed state](#4-trace-one-feature-across-the-stack)
5. [The third dimension: data and analytics engineering](#5-why-data-engineering-makes-me-a-different-full-stack-developer)
6. [Applied AI: how frontend and backend responsibilities differ](#6-applied-ai-across-the-stack)
7. [Testing and security: no layer gets a free pass](#7-testing-security-and-operations)
8. [UI/UX is a technical responsibility](#8-designing-for-people)
9. [My projects and the boundaries of my experience](#9-what-my-work-demonstrates)
10. [A study project you can build](#10-build-it-yourself)

## 1. Frontend vs backend vs full-stack

Think of a booking, application or reporting workflow. Someone wants to find a record, understand it, change something and receive confirmation.

**Frontend engineering** builds the experience: navigation, state, content, accessibility, visuals, charts, input and feedback. The frontend helps people understand and complete the task.

**Backend engineering** builds trusted operations: identity, access rights, domain rules, data persistence, transactions, integrations, retries, auditing and failures. The backend ensures the action is *allowed and correctly performed*.

**Full-stack engineering** connects them with explicit contracts and tests. It follows the user's intention through HTTP requests, policy checks, database writes and responses, and back to a meaningful interface.

| Dimension | Frontend | Backend | Their shared responsibility |
|---|---|---|---|
| Typical execution | Browser/mobile runtime | Server, worker, container or managed runtime | A clear request/response boundary |
| Primary focus | Usability and interaction | Correctness, data integrity and authorisation | Useful, reliable outcome |
| Typical tools in my work | React, TypeScript, CSS, charts, browser testing | Node.js/TypeScript, APIs, SQL, PostgreSQL/MySQL, background services | Tests, typed contracts, logs, review |
| Owns the visual loading state | Yes | Supplies the real operation state | Never show "complete" before completion |
| Owns permissions | Useful navigation hints | **Actual enforcement** | Test denied routes end-to-end |
| Owns form validation | Fast, helpful feedback | Authoritative rules | Consistent error contract |
| Owns durable writes | No | Transactions and persistence | Idempotent UI-to-server actions |
| Owns "real-time" meaning | Show freshness context | Source capture, processing and lag | Honest freshness expectations |
| Can be tested independently | Components and browser | Units, HTTP and database | Full workflow / user acceptance |

**Key distinction:** hiding the Admin button with CSS is not security. A frontend cannot decide for the server who may access a tenant's private data.

## 2. Frontend: what people experience

When I build the frontend, my job is not just to make the interface attractive. I ask whether a person understands what the data says and can complete their goal with reasonable effort.

### What frontend developers actually build

- **Information architecture:** page navigation, search, grouping and task prioritisation.
- **Components and interaction:** reusable controls, forms, modals, tables, charts, filters and details.
- **State management:** idle, loading, validating, queued, successful, partially successful, failed, cancelled and stale.
- **API consumption:** data fetching, type-safe response handling, cache invalidation and optimistic updates where safe.
- **Responsiveness:** layout and interaction across small phones, tablets and large screens.
- **Accessibility:** semantic HTML, labels, contrast, keyboard focus, zoom, reduced motion and assistive technology.
- **Performance:** fast first interaction, efficient rendering, small bundles and measured bottlenecks.
- **Error recovery:** preserve useful input, explain errors and avoid confusing repeated submissions.
- **Design quality:** hierarchy, consistency, typography and content that respects the user's mental model.

### Example: an import screen

A person selects a source, tests credentials, previews data, validates records and synchronises them. These stages are not equivalent. The user should know when an action merely *checks*, when it *prepares*, and when it changes persistent state.

A useful message is **"Preview complete: no records have been published."** A misleading message is **"All done!"** when the server only accepted an asynchronous job.

This is why I connect frontend work with UX research. Read [Volume VI: The Human Interface](OMNIMASTER_HUMAN_INTERFACE.md).

### Frontend sketch: model statuses explicitly

~~~tsx
type ImportState =
  | { kind: "idle" }
  | { kind: "queued"; jobId: string }
  | { kind: "running"; processed: number }
  | { kind: "done"; accepted: number; rejected: number }
  | { kind: "failed"; message: string; safeToRetry: boolean };

function ImportNotice({ state }: { state: ImportState }) {
  switch (state.kind) {
    case "queued": return <p role="status">Queued: {state.jobId}</p>;
    case "running": return <p role="status">Processed {state.processed} rows.</p>;
    case "done": return <p role="status">{state.accepted} imported; {state.rejected} rejected.</p>;
    case "failed": return <p role="alert">{state.message} {state.safeToRetry ? "Retry available." : "Check status first."}</p>;
    default: return <p>Choose a source to begin.</p>;
  }
}
~~~

This illustrates frontend state modelling, not a finished production feature. Actual values must come from the backend, and content needs complete form and accessibility testing.

## 3. Backend: what the system guarantees

When I work on the backend, I care about which operations can happen, whose data is involved, what is committed, and what a retry means.

### What backend developers actually build

- **API design:** routes, response codes, input schemas, error contracts and versioning.
- **Identity:** authentication, sessions, MFA and secure recovery policies.
- **Authorisation:** role, operation, tenant and record scope enforced server-side.
- **Domain logic:** business rules and valid state transitions, not rules scattered across browsers.
- **Database design:** keys, constraints, transactions, indexes, migrations and data consistency.
- **Integrations:** SQL sources, APIs, files, webhooks, third-party services and their failures.
- **Background work:** job queues, retries, backoff, idempotency and dead-letter handling.
- **Operations:** rate limits, observability, secure configuration, recovery and safe rollouts.
- **Data governance:** audit trails, retention, provenance and access boundaries.

### HTTP statuses must mean something

Imagine a user asks to synchronise data.

| Response | Accurate meaning | Interface implication |
|---|---|---|
| **202 Accepted** | Server accepted work for processing | Show Queued, not Completed |
| **200 OK** | The described synchronous operation succeeded | Show the actual result |
| **400 Bad Request** | Invalid shape or input | Highlight correctable fields |
| **401 Unauthorized** | No valid authentication | Prompt for sign-in safely |
| **403 Forbidden** | Authenticated but not permitted | Deny without leaking data |
| **409 Conflict** | State/version conflict | Ask user to reload or reconcile |
| **429 Too Many Requests** | Request limit reached | Explain safe retry timing |
| **5xx** | Unexpected service failure | Report uncertainty; don't assume write didn't happen |

### Backend sketch: enforce policy where it matters

~~~ts
// Pseudocode showing responsibilities; not a working Fastify route.
async function resolveException(request: RequestContext) {
  const actor = await authenticate(request);
  const input = validateResolution(request.body);
  const access = await authorise(actor, "exceptions.resolve", input.exceptionId);
  if (!access.allowed) return forbidden();

  return db.transaction(async (tx) => {
    const row = await tx.selectExceptionForUpdate(input.exceptionId, access.tenantId);
    if (!row) return notFound();
    if (row.status === "RESOLVED") return conflict("Already resolved");
    await tx.markResolved(row.id, input.reason);
    await tx.writeAudit(actor.id, "exceptions.resolve", row.id);
    return success({ status: "RESOLVED" });
  });
}
~~~

A transaction protects the combined state change inside the database. Real routes still need schema definitions, secure authentication, tenant lookup, consistent error handling, idempotency and integration tests.

## 4. Trace one feature across the stack

### Case: resolve a fictional delivery exception

~~~mermaid
sequenceDiagram
    actor Person
    participant UI as React screen
    participant API as Authenticated API
    participant DB as PostgreSQL
    participant Jobs as Background worker
    Person->>UI: Select Resolve
    UI->>UI: Validate required reason
    UI->>API: POST /exceptions/{id}/resolve
    API->>API: Verify actor + tenant + permission
    API->>DB: Atomic state and audit update
    DB-->>API: Commit or conflict
    API-->>UI: Verified status or safe error
    UI-->>Person: Explain what actually happened
    API->>Jobs: Queue post-commit notification
    Jobs-->>API: Record outcome and retries
~~~

**Frontend responsibility:** make Resolve discoverable, require a meaningful reason, show a submitting state, prevent confusing duplicate clicks and explain success, conflict or unknown outcome.

**Backend responsibility:** verify role and tenant, reject stale state, commit the change atomically, record the actor and protect the notification workflow against duplicates.

**Full-stack responsibility:** write tests that start from user action and inspect backend truth. A button labelled "Resolved" must never be a substitute for the committed state.

### Common failure: the ambiguous network timeout

The browser sends a request. The server commits. The response is lost.

The frontend cannot safely assume failure and resubmit. The backend should provide a stable operation identifier or idempotency mechanism, plus a status endpoint. The frontend should say, **"We couldn't confirm the result. Check its status before retrying."**

This is where real software engineering differs from demo tutorials.

## 5. Why data engineering makes me a different full-stack developer

My foundation is not only frontend and backend code. I have worked with SQL, Power BI, DAX, Fabric-related analytics, ETL/ELT, source integration, modelling and performance across organisations and industries.

That experience changes what I ask when building a product:

1. What is the authoritative event, and what does one row represent?
2. Can a join multiply a business amount?
3. How recent is the source, not merely the page render?
4. Can a changed record or delete be missed by an incremental pipeline?
5. Can access rules leak another market's or tenant's information?
6. Are the dashboard's numbers reproducible from source?

A product becomes trustworthy when its **data grain, business semantics, API contract and interface wording** agree.

### Learn by building

My [Data-to-Decision Platform](../projects/data-to-decision-platform/) demonstrates a synthetic source-event pipeline with versioning, atomic SQLite writes, current-state projection and tenant-specific metrics. It has no external identity layer or live CDC connection; it is an educational simulation.

## 6. Applied AI across the stack

An AI feature is not a magic box attached to a button. Different layers own different risks.

| Frontend / UX | Backend / data layer |
|---|---|
| Explain what the AI can and cannot do | Decide whether this task is permitted for the actor |
| Show sources, uncertainty and review status | Retrieve approved source material under tenant/role scope |
| Provide edit, reject, retry and human-review paths | Validate schema, source IDs, limits and content safety |
| Avoid a confident-looking answer with no evidence | Log bounded decisions, costs, failures and provenance |
| Preserve user control | Apply deterministic state transitions; no silent consequential writes |

### An education example

A teacher asks AI to suggest feedback on a fictional learner answer. The frontend should make the output recognisable as a suggestion, show the relevant rubric and source and offer a deliberate review action.

The backend should verify educator access, retrieve only the permitted learner and rubric, bound provider use, validate scoring constraints and require explicit human approval before an official grade changes.

My [Offline AI Output Evaluation Lab](../projects/ai-output-evaluation/) teaches a narrow extractive-evidence contract. It does **not** prove semantic truth, privacy compliance or production-level AI reliability.

## 7. Testing, security and operations

A meaningful "done" depends on the layer.

| Test class | Frontend evidence | Backend evidence | End-to-end question |
|---|---|---|---|
| Unit | Correct component state | Business-rule invariant | Are the parts internally coherent? |
| Integration | Correct API decoding | Actual database operation | Did they agree on schema and semantics? |
| Browser | User completes the task | Role/tenant denial is enforced | Does the user journey work? |
| Accessibility | Focus, labels, reflow, screen reader | Useful error information | Can different people understand and recover? |
| Security | No secrets or false trust assumptions | Auth, MFA, IDOR, input, SSRF and least privilege | Does an attacker bypass the intended boundary? |
| Reliability | Honest queued/failed states | Retry, checkpoint, rollback and alerting | What happens when a dependency fails? |
| Release | UI assets on intended version | Migration and config on intended version | Did this exact commit pass the right gates? |

A green unit suite is useful, but it does not prove a real deploy, accessibility compliance or authorisation on every route.

## 8. Designing for people is engineering

UI/UX development matters because a system's job is not just to compute the right output. It must help people *use* the output.

The questions I now ask about an interface are practical: can someone find the task, understand the meaning, tell whether something saved, recover when it fails, use the screen on a phone and know what happens to their information?

One lesson arrived directly from this portfolio: the "Interactive Study Room" link initially opened an **HTML source file in GitHub** instead of the actual experience. The code was there, but the person could not use it. Fixing the destination was a usability improvement, not a CSS improvement.

[Volume VI: The Human Interface](OMNIMASTER_HUMAN_INTERFACE.md) contains full chapters on task design, accessibility, design systems, user research and practical UX exercises.

## 9. What my work demonstrates

| Workstream | Frontend or UX work | Backend / data work | Status boundary |
|---|---|---|---|
| Enterprise BI engagements | Dashboards, reporting UX, semantic labels and visual performance | SQL modelling, transformations, metric definitions and data reconciliation | Historical professional work, proprietary source |
| The Fixer / NewChanges | Source previews, admin workflows, responsive/dashboard interfaces | TypeScript/Fastify APIs, PostgreSQL, imports, auth/MFA workstreams, tests | Public code with active gates; not a blanket production-readiness claim |
| CABO Learning Hub | Learner, teacher, guardian and admin journeys; assessments and mobile design | Identity, institutional roles, records, AI routing and validation | Active product development; no claimed government rollout |
| Financial and HR prototypes | Forms, review flows, reporting and role-aware UX | Transaction rules, auditability, data permissions and domain models | Prototypes/staging with project-specific limitations |
| OmniMaster Study Room | Interactive questions, progress, navigation and accessible controls | Hosted delivery and test checks; browser-local progress | Live teaching product; final manual QA remains separate |

I am strongest in data engineering, BI/analytics and full-stack application delivery, with growing exposure to cloud/platform operations, security engineering, mobile and AI. **My ability to contribute across much of software-oriented IT is not a claim to be an expert in every specialist niche. Hardware engineering and physical device repair are not my area of focus.**

## 10. Build it yourself: the exception tracker

Create a fictional two-tenant exception workflow. Build only one complete path first.

**Step A: define the data.** One exception has a stable ID, tenant, status, assigned actor, created timestamp and resolution history.

**Step B: design the frontend.** A list, detail page and Resolve action with loading, confirmation, conflict and error states. Test keyboard navigation and a narrow mobile viewport.

**Step C: design the backend.** Use an authenticated API, role/tenant checks, valid state transitions, transaction/audit consistency, and an idempotency strategy.

**Step D: prove denial.** Try a wrong-tenant ID, a revoked session and a duplicate resolution attempt. Verify no unauthorised state change or leakage.

**Step E: make failure understandable.** Disconnect the browser after request submission. Does the frontend promise a retry it cannot justify? Does the backend expose enough state to reconcile what happened?

**Step F: document the boundary.** Write a README saying what was implemented, what was tested and what is missing before real deployment.

### Five review questions

1. What must happen on the server even if the browser lies?
2. How does a frontend distinguish "queued" from "done"?
3. Why does a transaction matter for state change plus audit?
4. What happens to the user if a request commits but the response disappears?
5. Which tests prove a feature, and which merely prove a toy component?

**The most interesting full-stack skill is not knowing every syntax rule. It is knowing which part of the system owns the truth, how the layers cooperate and what a real person experiences when something goes wrong.**

---

**Explore further:** [The OmniMaster Academy](OMNIMASTER_ACADEMY.md) · [Engineering Field Guide](OMNIMASTER_FIELD_GUIDE.md) · [Build With Me](OMNIMASTER_BUILD_WITH_ME.md) · [UI/UX Development](OMNIMASTER_HUMAN_INTERFACE.md) · [Interactive Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)

*Educational text written as a first-person field guide. Examples are synthetic. Private client information is intentionally excluded.*