# Personal Chapter 02 | Why I think in systems

[← INTJ and me](01_INTJ_AND_ME.md) · [Operating manual](../OMNIMASTER_OPERATING_MANUAL.md) · [Next →](03_IT_RANGE_AND_LIMITS.md)

## My professional curiosity has an origin

I studied **Statistics and Data Science at the University of Pretoria**, graduating with a BCom in 2023. That made me interested in what evidence can actually support. Later, professional BI work taught me that numbers become dangerous when they look authoritative but were modelled carelessly.

And the more operational systems I worked with, the more I learned that a report is only one surface of a larger machine.

## The journey that changed my questions

### First: make the analysis correct

In reporting work I cared about cleaning data, matching sources, writing useful DAX/SQL, and making results intelligible to business users.

That taught me that even a simple question like “how many?” depends on populations, relationships, dates and exclusions.

### Then: make the pipeline repeatable

When reports depend on manual exports, shifting schemas and complex operational source queries, the workflow becomes the real engineering problem.

Automation pushed my thinking toward staging, source contracts, retries, scheduler behaviour, transformations, monitoring and data governance.

### Then: make the application usable

A dashboard can explain a problem, but people may need to act on it. That draws in React, APIs, PostgreSQL, identity, admin tools, validation, transactions and interfaces.

I started thinking less about a single output and more about a full path from **user intent to an authorised, durable state change**.

### Then: make the system safe to operate

Security and infrastructure work exposed the uncomfortable part of building things: a branch can pass tests and still be unsafe to release. Credentials, MFA enrolment, tenant isolation, source access, database parity and rollback are not optional chapters in a real product.

### Now: ask whether intelligence improves anything

Applied AI interests me because it can assist with difficult tasks, especially learning, reporting and workflow analysis. But my instinct remains the same: where is the source evidence, what is deterministic, who reviews, and how does failure behave?

## What connects the industries

I have worked across banking, manufacturing, FMCG, media, agriculture and social impact. They have different terminology and users, but many recurring technical problems:

- A source record means something different from how a downstream user reads it.
- Two legitimate events are accidentally counted as one or one event is counted twice.
- Permissions are applied to a screen but not enforced on the backend.
- A complex process is repeated manually because the systems do not integrate.
- A confident-looking output hides uncertainty or stale data.
- An implementation is considered complete before its failure path has been tested.

These patterns made me increasingly curious about the **connections between disciplines**.

## One example of how I work

Imagine an operations dashboard has a wrong total.

**Shortcut:** alter the DAX formula until the visual matches an expected number.

**My preferred route:**

1. Define the business quantity and time period.
2. Reconcile raw source records and grain.
3. Check transformations and keys.
4. Inspect the semantic model and security filters.
5. Profile the query if latency is involved.
6. Fix the smallest layer that owns the error.
7. Add a regression test and explain the change to the business.

That method scales from a report to a platform.

## Why I build independent products

Client work gives me real constraints, stakeholders and delivery pressure. Independent projects let me explore how those disciplines meet across an entire product lifecycle, including architecture, onboarding, pricing ideas, privacy, user experience, tests and infrastructure.

That is why my portfolio spans learning systems, finance software, workforce tooling, data integration, commerce experiments and tiny synthetic labs. Not everything is released; the point is to learn the hard parts honestly.

## The contradiction I live with

I enjoy breadth. Engineering expertise also requires depth and restraint. Being able to move between topics is useful only when I know **when a specialist is needed**, what evidence is missing, and what not to claim.

That tension is part of why I am working toward solution architecture and technical leadership while remaining hands-on.

## A habit you can copy today

For your next bug, keep a tiny journal:

~~~text
What I saw:
What I assumed:
What the source really showed:
My smallest experiment:
The actual cause:
What I changed:
What would prove the fix:
What I still do not know:
~~~

Over time, this record explains how you think much more convincingly than a list of tools.

[Professional case studies](../CLIENT_CASE_STUDIES.md) · [Why my range matters](03_IT_RANGE_AND_LIMITS.md) · [Learn the workflow](../OMNIMASTER_ACADEMY.md).

[← INTJ and me](01_INTJ_AND_ME.md) · [Next: Across IT →](03_IT_RANGE_AND_LIMITS.md)
