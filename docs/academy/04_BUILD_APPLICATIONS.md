# Lesson 04 | Build an application around a real business event

[← Lesson 03](03_PIPELINES_AND_CDC.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Next →](05_APPLIED_AI.md)

## From a dashboard to a system

A report tells you something happened. An application lets someone do something about it.

My move from analytics into React, TypeScript, Node.js and PostgreSQL did not change my core habit: I still start by defining the authoritative event, who may change it, and how to prove the state is correct.

## Example project: a fictional delivery exception tracker

**User:** operations manager.

**Task:** review an undelivered item, assign a responsible person and record a resolution.

**Entities:** delivery, exception, assignment, actor, audit event.

**States:** OPEN → INVESTIGATING → RESOLVED. Any transition to another state must be explicit and authorised.

~~~mermaid
sequenceDiagram
    actor Manager
    participant UI as React UI
    participant API as HTTP API
    participant Policy as Server policy
    participant DB as Database
    Manager->>UI: Resolve exception
    UI->>API: POST /exceptions/{id}/resolve
    API->>Policy: Check identity, tenant, role and state
    alt Allowed
      Policy->>DB: Atomic state change and audit
      DB-->>API: Committed new state
      API-->>UI: 200 with updated record
    else Denied or stale
      Policy-->>API: Deny or conflict
      API-->>UI: 403 or 409 with safe error
    end
~~~

This is a teaching design, not a copy of a client's API.

## Define your API contract first

| Endpoint | Who may call it | Invariant |
|---|---|---|
| GET /exceptions | Authenticated operator in tenant | Only authorised tenant's records |
| GET /exceptions/:id | Allowed tenant member | No cross-tenant disclosure |
| POST /exceptions/:id/assign | Manager in tenant | Assignee belongs to permitted scope |
| POST /exceptions/:id/resolve | Manager in tenant | Cannot resolve twice without explicit policy |
| GET /exceptions/:id/history | Authorised reviewer | Immutable evidence of changes |

**Important:** a React component hiding the Resolve button is not an authorisation check. The backend must enforce it on every request.

## A build sequence I prefer

1. Draw the state machine on paper.
2. Create schema constraints and test realistic invalid states.
3. Write the API contract and denial cases before the UI.
4. Build one complete vertical slice: open → assign → resolve.
5. Add a clear, accessible interface with loading/error/empty states.
6. Add audit information and a recoverable error path.
7. Test an attacker changing the exception ID or tenant ID.

A narrow complete workflow teaches more than twelve disconnected interfaces.

## Sample state-transition exercise

Write a pure function that accepts current state, requested state and role, and returns a decision. Test invalid transitions before connecting a database. Then ensure the database transaction rechecks the authorised current state to prevent concurrent writes using stale UI state.

**Failure scenario:** two managers try to resolve the same exception simultaneously. How do you prevent duplicate notifications and conflicting audit records? Discuss optimistic version checking, database transactions and idempotency keys.

## Accessibility is engineering

Test keyboard navigation, focus order, mobile width, meaningful form errors, chart alternatives and screen-reader labels. A beautiful admin tool that cannot be used under real device constraints is incomplete.

## Learning checkpoint

**Pass when:** a stranger can launch your fictional application, complete one authorised workflow, see useful errors for bad input, and run tests that prove cross-tenant requests fail.

**Expansion:** add an ingestion simulation and update the exception dashboard from it. Keep the source identity separate from the user interface.

Reference projects: [The Fixer](https://github.com/CayelaemJ/NewChanges) · [CABO Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) · [Full-stack systems chapter](../handbook/06_PRODUCTS_AND_AI.md).

[← Lesson 03](03_PIPELINES_AND_CDC.md) · [Next: Applied AI →](05_APPLIED_AI.md)
