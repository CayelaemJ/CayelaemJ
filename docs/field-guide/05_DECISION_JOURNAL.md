# Field Guide 05 | Architecture decision journal

[← Role and evidence map](04_ROLE_AND_EVIDENCE_MAP.md) · [Volume II](../OMNIMASTER_FIELD_GUIDE.md) · [Main handbook](../OMNIMASTER_HANDBOOK.md)

The choice of technology matters less than the reasoning and trade-offs behind it. I like to keep decisions inspectable: **context, options, decision, risks, verification and revisit triggers**.

These are teaching-oriented decision records reflecting questions in my work. They are not a complete history of formal company approvals or claims that each option was deployed.

## ADR-01 | Where should data transformation happen?

**Status:** Context-dependent design principle, not a blanket implementation.

**Problem:** An application ingests data from SQL, API and file sources. Repeatedly moving whole datasets into an application database to perform report-only calculations increases latency, duplication and reconciliation burden.

### Options

| Option | Strength | Weakness |
|---|---|---|
| All transformations in app code | Flexible domain rules and common programming tooling | May duplicate large datasets and bypass database optimisation |
| Push all rules to source SQL | Less data transfer and efficient set-based processing | Couples business logic to source schema and database permissions |
| Hybrid source projection + curated semantics | Can keep heavy filtering/joins near data while preserving app policy | Needs explicit ownership and consistent contract versioning |

**My preferred approach:** place large, set-based, source-specific calculations where the engine can do them safely; keep cross-source policy, access decisions and application transactions in the appropriate service boundary. Define the data contract once and validate the highest-risk invariants, rather than multiplying inconsistent checks.

**How I test the decision:** compare plans, data movement, transformation ownership, result reconciliation, security scope and end-to-end freshness on a disposable environment.

**Revisit if:** source systems cannot support required indexes/privileges; business rules change frequently; multiple consumers need a shared versioned curated layer.

**Related:** [Data architecture atlas](01_ARCHITECTURE_ATLAS.md) · [The Fixer](https://github.com/CayelaemJ/NewChanges).

---

## ADR-02 | How do we capture source changes?

**Status:** A real design question under investigation; no completed production CDC claim.

**Problem:** A polling approach can miss timestamp collisions and physical deletes. A binlog reader introduces privileges, transaction semantics and operational overhead.

**Options:** stable incremental queries plus reconciliation, transaction/binlog CDC, source event publishing or periodic full snapshots.

**Decision criterion:** the **actual freshness and completeness contract**, not the marketing phrase “real time.”

If the business can tolerate scheduled reporting and a reliable source version is available, simpler incremental extraction may be right. If every mutation and delete must be represented, CDC/event logs become more compelling.

**Verification:** same-second updates, deletes, restart at the checkpoint boundary, oversized event handling, retention expiry, duplicate delivery, source snapshot consistency and measured consumer lag.

**Public work:** [CDC source adapter issue #241](https://github.com/CayelaemJ/NewChanges/issues/241) · [CDC educational lab](../../projects/cdc-replay-lab/).

---

## ADR-03 | How should we move a live application between database providers?

**Status:** Release principle drawn from guarded Neon/Aiven work. A migration candidate is not a completed switch.

**Problem:** Backups, application identity, active writers and audit data must agree at cutover. Schema parity alone is insufficient.

**Options considered:** in-place upgrade, offline snapshot copy, managed replication/CDC or a timed maintenance-window switch.

**Preferred policy:** no live switch until there is a verified final source state, final sync, writer fencing, least-privileged credentials, tested auth/MFA, complete required data reconciliation, an approved traffic plan and a recovery route. Do not let a cost-saving target or a green migration script waive these gates.

**Verification:** restore test, extension/function/privilege review, source-target parity, single-writer invariant, application smoke tests, rollback rehearsal and explicit sign-off.

**Revisit if:** the application supports online dual-read/single-writer migration, the outage tolerance changes or the provider's runtime/connection limits differ materially.

**Related:** [Migration PR #225](https://github.com/CayelaemJ/NewChanges/pull/225) · [Debugging casebook](02_DEBUGGING_CASEBOOK.md).

---

## ADR-04 | How should privileged actions prove identity?

**Status:** Active security design, not an unconditional production guarantee.

**Problem:** An administrator can possess a valid login session without having recently proved control of a strong authentication factor. Enrolment and recovery are frequent bypass risks.

**Options:** password-only, session-wide TOTP, WebAuthn/passkeys with step-up and controlled recovery, or externally managed identity with equivalent enforced claims.

**Preferred policy:** server-enforced role and tenant checks for every privileged operation; fresh strong MFA evidence for high-risk actions; no first-time-enrolment bypass granting general admin access; replay-resistant recovery and auditability.

**Verification:** route enumeration, direct HTTP negative requests, ordinary-user denial, session revocation, TOTP replay prevention, passkey origin binding, recovery separation and production secret configuration.

**Revisit if:** federated enterprise identity becomes authoritative or legal/operational requirements change.

**Related:** [Fixer admin MFA PR #219](https://github.com/CayelaemJ/NewChanges/pull/219) · [Security chapter](../handbook/07_SECURITY_AND_DELIVERY.md).

---

## ADR-05 | What role should AI have in consequential workflows?

**Status:** Applied-AI product design direction with selected code experiments, not independent certification.

**Problem:** A model can be helpful at drafting, explaining and evaluating source-bound responses, but it may fabricate evidence, expose data or give inconsistent advice.

**Options:** unconditional autonomous decisions, no AI at all, or bounded AI assistance with source provenance and human oversight.

**Preferred policy:** use AI where it makes a specific workflow more useful and where there is a deterministic boundary for identity, permission, output structure and irreversible changes. Human review is required for consequential learner, candidate and finance decisions.

**Verification:** source-grounded evaluation sets, refusal/unknown handling, tenant isolation, prompt-injection attacks, output schema checks, latency/cost budgets, failover, fairness review and appeals.

**Revisit if:** assessment requirements, provider costs, model reliability, regulations or allowed data flows change.

**Related:** [Learning Hub](https://github.com/CayelaemJ/Training-and-Development-Hub) · [Offline AI evaluation lab](../../projects/ai-output-evaluation/).

---

## ADR-06 | What should a “green” CI status actually mean?

**Status:** Engineering release philosophy and an implemented test boundary in this profile.

**Problem:** A workflow can complete successfully even when it did not test the real deployment surface, the latest commit or the relevant negative paths.

**Preferred policy:** make each status precise. **Green lab CI** means the local synthetic labs and documentation checks passed at the commit under test. **Green release gate** would require the applicable application, browser, database, security, migration and operational validation on the intended release artifact.

A documentation change should not assert a Fixer MFA release merely because the profile's Python tests passed.

**Evidence:** [Profile CI workflow](../../.github/workflows/engineering-labs-ci.yml). It tests four self-contained labs and the handbook's local navigation, not The Fixer's live infrastructure.

**Revisit if:** a project adds more consumers, secrets, external integrations, supported runtimes or new legal/release requirements.

---

## The decision-record template I use

~~~text
Decision:
Status: proposed / accepted / implemented / verified / superseded
Date and context:
Owner and reviewers:

Problem and invariant:
Requirements:
Constraints (security, cost, compliance, latency, skills):
Options considered:
Chosen option and why:
Rejected options and why:

Known risks:
Operational impact:
How we will test:
Evidence required for release:
Rollback:
Revisit conditions:
References:
~~~

## My broader view

Choosing the newest platform is easy. Choosing a platform whose costs, failure modes, governance and maintenance fit the problem is more demanding. That's the practice I want to deepen as I grow toward solution architecture and technical leadership.

[← Role map](04_ROLE_AND_EVIDENCE_MAP.md) · [Return to Volume II](../OMNIMASTER_FIELD_GUIDE.md) · [Volume I: career and technical handbook](../OMNIMASTER_HANDBOOK.md)
