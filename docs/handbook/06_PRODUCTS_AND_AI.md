# Chapter 06 | Software products and responsible AI

[← Previous](05_ANALYTICS_ENGINEERING.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](07_SECURITY_AND_DELIVERY.md)

I became more interested in full-stack development as I discovered how often the useful outcome was **an action, not a chart**. A user may need to complete onboarding, verify an enrolment, correct a record, approve a financial entry or receive a trustworthy explanation.

## The system underneath the screen

~~~mermaid
flowchart TD
    UI["React / native client"] --> API["Authenticated API boundary"]
    API --> POLICY["Roles, validation and business rules"]
    POLICY --> DB["Transactional database"]
    POLICY --> EVENTS["Jobs, audit events, notifications"]
    POLICY --> AIB["Optional AI service boundary"]
    AIB --> EVAL["Schema validation, source evidence, fallback"]
    EVAL --> REVIEW["Human review when consequential"]
    EVENTS --> OBS["Observability and recovery"]
~~~

This is an architectural pattern, not a statement that every public project implements every component.

## Three product examples

### A. Data integration and reporting: The Fixer

The Fixer crosses application and analytical boundaries. Users configure permitted sources, inspect ingestion, review reporting, interact with dashboards and administer permissions. That creates a requirement to protect both **data-plane** access and **control-plane** changes.

**Engineering questions:** Who may change a source URL? Can a source connection reach a private network address? How are invalid files rejected? What does an audit event prove? Can an administrator bypass step-up authentication through a different route?

**Public evidence:** [NewChanges](https://github.com/CayelaemJ/NewChanges). Active release/security PRs remain separate from any public claims of deployment readiness.

### B. Learning and assessment: CABO Learning Hub

The Learning Hub explores source-grounded exams, written responses, marking feedback and long-term education journeys. It combines document ingestion, user-scoped records, educators, guardians and institutional permissions.

**Engineering questions:** Can a model invent a question unsupported by the document? Does marking exceed the rubric's maximum score? Can staff inspect another learner's record? Who can correct an AI-suggested grade? How do school transfers affect data ownership?

**Public evidence:** [Training-and-Development-Hub](https://github.com/CayelaemJ/Training-and-Development-Hub). High-stakes academic decisions must remain human-governed.

### C. Accounting and audit: CABO Financial Intelligence

The product explores a double-entry ledger, reconciliations, immutable audit context and optional AI-powered *explanation*. Transactions and controls must be deterministic. A generated sentence should never be treated as a write instruction.

**Public evidence:** [Accounting, Audit and Analytics Software](https://github.com/CayelaemJ/Accounting-Audit-And-Analytics-Software). Staging status and functional limits are documented in the repository.

## The difference between an AI integration and an AI feature

Calling a language model is easy. Delivering a responsible feature needs more:

| Design dimension | What I ask |
|---|---|
| **Task** | What useful action does this support, and what remains deterministic? |
| **Input** | Is the source authorised, bounded, relevant and appropriately redacted? |
| **Output contract** | Does the response conform to a validated schema and business rules? |
| **Grounding** | Can the response point back to approved documents or facts? |
| **Human control** | Can someone review, reject, override and contest the result? |
| **Failure behaviour** | Is the feature useful when an AI provider is unavailable? |
| **Operating cost** | Is model selection appropriate for latency, quota and budget? |
| **Safety** | Can prompts, attachments or outputs leak information or bypass roles? |

In Learning Hub experiments, I have explored task-aware routing across Groq and Hugging Face with fallback. A previous isolated provider test demonstrated Groq operation and degradation fallback, while Hugging Face's live response was blocked by an HTTP 402 billing/credit condition at the time. **A fallback demonstration is not proof that both providers work in production.**

[AI routing workstream](https://github.com/CayelaemJ/Training-and-Development-Hub/pull/95)

## A deliberately small evaluator

My [Offline AI Output Evaluation Lab](../../projects/ai-output-evaluation/) does not call a model. It validates synthetic *extractive* answers for known source IDs, exact quotations, expected shape and explicit human-review requirements. It deliberately rejects unsupported freeform additions.

It is useful as a teaching example precisely because its limits are visible. A matching quote does not prove the source is true or safe, a caller-supplied confidence score is not calibration, and a simple email-pattern check is not privacy protection.

## The cost of a careless automated decision

Children's learning, employment and financial decisions affect real lives. I favour:

- Documented purpose and lawful access before processing.
- Access-scoped retrieval and data minimisation.
- Quality evaluation with synthetic and approved representative cases.
- A meaningful path for a person to challenge or correct the result.
- Auditable decisions, cautious retention and carefully bounded provider calls.
- Explicit release blockers when legal, privacy or security review is outstanding.

For the Botswana education direction, jurisdiction and data-transfer requirements require verified legal and hosting assessments **before any live learner-data rollout**. A product roadmap is not legal approval.

[System-design playbook](../OMNIMASTER_SYSTEM_DESIGN.md) · [Learning Hub repository](https://github.com/CayelaemJ/Training-and-Development-Hub)

[← Chapter 05](05_ANALYTICS_ENGINEERING.md) · [Next: Security and delivery →](07_SECURITY_AND_DELIVERY.md)
