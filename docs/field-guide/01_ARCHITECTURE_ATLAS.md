# Field Guide 01 | Annotated architecture atlas

[← Volume II contents](../OMNIMASTER_FIELD_GUIDE.md) · [Next: Debugging casebook →](02_DEBUGGING_CASEBOOK.md) · [Main handbook](../OMNIMASTER_HANDBOOK.md)

Architecture only becomes useful when it reveals who owns the facts, where trust changes and how a system handles failure. These are **reference architectures inspired by my work**, not exact deployment diagrams, infrastructure inventories or promises that every component is live.

## Map A. From operational updates to trustworthy analytics

**Context:** my current MySQL and PostgreSQL reporting experiments, historical enterprise BI work and the [CDC Replay Lab](../../projects/cdc-replay-lab/).

~~~mermaid
flowchart LR
    SRC["Operational system / MySQL"] --> CAP{"Capture contract"}
    CAP -->|"Reliable timestamp / batch"| POL["Incremental polling"]
    CAP -->|"Row changes available"| BIN["Binlog / CDC reader"]
    POL --> RAW["Auditable ingestion"]
    BIN --> RAW
    RAW --> VAL["Typed & keyed projections"]
    VAL --> SEM["Source-aware business model"]
    SEM --> BI["Dashboard / API"]
    RAW --> CP["Checkpoint & reconciliation"]
    CP -->|"Replay / repair"| VAL
~~~

**What matters at each boundary**

| Boundary | Question I ask | A useful test |
|---|---|---|
| Operational source → capture | Are deletes, corrections and same-timestamp updates observable? | Apply multiple writes with one timestamp; compare extracted changes |
| Capture → raw store | Is a source event durable before the checkpoint advances? | Crash between event write and checkpoint |
| Raw → curated state | What is the correct grain? Are duplicate messages harmless? | Replay the same event ID; verify unchanged totals |
| Curated state → metrics | Are changed and deleted accounts reflected without double counting? | Compare dashboard aggregates with controlled source truth |
| Metrics → user | What latency is promised, and what counts as “fresh”? | Measure end-to-end lag, not just UI polling interval |

**Trade-off:** binlog CDC can preserve deletion and change order better than naive timestamp polling, but introduces replication privileges, lifecycle, transaction boundaries, retention and operational complexity. It is not an automatically better answer for every low-volume reporting feed.

**Actual delivery boundary:** the [Fixer synthetic binlog work](https://github.com/CayelaemJ/NewChanges/pull/237) is distinct from the ten-feed reporting path; [issue #241](https://github.com/CayelaemJ/NewChanges/issues/241) tracks the needed adapter and proofs. This diagram is the target reasoning model, not a claim of a finished production connection.

## Map B. Semantic modelling that respects the business event

**Context:** banking, FMCG, agriculture and Australian manufacturing analytics. Proprietary source data is deliberately not shown.

~~~mermaid
flowchart TD
    ORD["Orders / dispatch events"] --> G["Declare source grain"]
    EMP["Workers / schedules"] --> G
    SUR["Surveys / campaigns"] --> G
    G --> CT["Cardinality & key tests"]
    CT --> F["Curated fact tables"]
    DIM["Conformed dates, products, locations"] --> MODEL["Governed semantic model"]
    F --> MODEL
    MODEL --> RLS["Market / employer restrictions"]
    RLS --> KPI["Power BI measures & decisions"]
    KPI --> REC["Source reconciliation & performance tests"]
~~~

**Why I draw this:** one delivery can have several processing events; one employee can have multiple shift records; one survey response can join to multiple classifications. Without grain contracts, a dashboard can be *precisely wrong* at impressive speed.

**My working rule:** reconcile a sum or count at each transformation boundary and after security filters. Performance optimisation is valid only if the intended business total survives it.

**Reproducible companion:** [SQL Query Plans Lab](../../projects/sql-query-plans/) illustrates filtering/indexing without claiming to benchmark Power BI or Microsoft Fabric.

## Map C. A full-stack administrative workflow

**Context:** The Fixer and independent full-stack applications.

~~~mermaid
sequenceDiagram
    actor User
    participant UI as Browser or native UI
    participant Auth as Session / MFA
    participant API as Authorised API
    participant DB as Transactional database
    participant Audit as Audit events
    User->>UI: Request sensitive change
    UI->>Auth: Present session and step-up
    Auth-->>UI: Verified proof or denial
    UI->>API: Submit action
    API->>API: Validate role, tenant and input
    alt Authorised
        API->>DB: Atomic write with constraints
        DB-->>API: Commit / failure
        API->>Audit: Record result with actor and scope
        API-->>UI: Correct response
    else Denied
        API->>Audit: Record attempted action as permitted
        API-->>UI: Deny without information disclosure
    end
~~~

**Critical engineering distinction:** front-end access control improves usability but cannot protect an endpoint. Each privileged request needs a server-enforced role and tenant boundary. For MFA, credential enrolment and emergency recovery must not open an unguarded parallel path.

**Actual delivery boundary:** [Fixer admin MFA PR #219](https://github.com/CayelaemJ/NewChanges/pull/219) remains a draft workstream with deployment and negative-test gates, not a completed production security guarantee.

## Map D. Applied AI inside a real product workflow

**Context:** Learning Hub assessment, document grounding and independently developed [AI output checks](../../projects/ai-output-evaluation/).

~~~mermaid
flowchart LR
    USER["Authorised educator / learner"] --> POLICY["Purpose, access and consent"]
    DOC["Approved reference documents"] --> RET["Retrieval & provenance"]
    POLICY --> ROUTER{"Task-specific AI routing"}
    RET --> ROUTER
    ROUTER --> MODEL["Approved model/provider"]
    MODEL --> CHECK["Schema & evidence evaluation"]
    CHECK --> DEC{"Consequential output?"}
    DEC -->|"Yes"| HUMAN["Educator / accountable reviewer"]
    DEC -->|"No"| OUTPUT["Scoped user response"]
    HUMAN --> OUTPUT
    MODEL -. "Unavailable" .-> FALL["Controlled fallback / no-decision state"]
    FALL --> OUTPUT
~~~

A model response is not automatically a grade, an employment decision or a financial posting. A safe process needs a valid input purpose, permitted documents, an output contract, evaluation and a human route for consequential decisions.

**Failure to simulate:** provider 429/402 responses, irrelevant retrieved material, prompt injection in documents, unsupported citations, confidence mismatch, timeout and leakage between learners or tenants.

**Actual delivery boundary:** the [CABO Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) has development and pilot work; its [provider routing PR](https://github.com/CayelaemJ/Training-and-Development-Hub/pull/95) does not establish fully verified multi-provider production availability.

## Map E. A release that remains reversible

~~~mermaid
flowchart TD
    CODE["Specific source commit"] --> T["Build, unit and integration tests"]
    T --> SEC["Negative security & browser checks"]
    SEC --> MIG["Migration / backup / restore rehearsal"]
    MIG --> READY{"All release gates pass?"}
    READY -->|"No"| HOLD["Hold, fix, retest"]
    READY -->|"Yes"| APPROVAL["Authorised rollout decision"]
    APPROVAL --> RAMP["Staged traffic & observability"]
    RAMP --> HEALTH{"Healthy & correct?"}
    HEALTH -->|"No"| ROLL["Rollback & investigate"]
    HEALTH -->|"Yes"| KEEP["Operate, document, monitor"]
~~~

**Why this matters to me:** I have seen work reach a promising branch or staging environment while remaining unfinished operationally. A migration requires writer fencing, reconciliation, privileged-role review, rollback and evidence tied to the exact change.

The [profile's lab CI](../../.github/workflows/engineering-labs-ci.yml) validates toy examples. It is *not* a substitute for The Fixer's Docker, database, security or actual deployment gates.

## How I use these diagrams in a design review

I ask five questions, in order:

1. Where does the authoritative event originate?
2. Which boundaries can lose or distort information?
3. Who can perform each action, and how is that enforced?
4. What happens when one component fails or retries?
5. Which measurements or tests would tell us the solution actually worked?

The diagram has value only when it gives a colleague something concrete to challenge.

[Next: Debugging casebook →](02_DEBUGGING_CASEBOOK.md)
