# Chapter 08 | Reproduce the work

[← Previous](07_SECURITY_AND_DELIVERY.md) · [Contents](../OMNIMASTER_HANDBOOK.md) · [Next →](09_LEADERSHIP_AND_NEXT.md)

A recruiter can read an architecture paragraph in sixty seconds. An engineer should also be able to inspect code and run a small example. These four labs are designed for exactly that: **synthetic inputs, no cloud credentials, no customer data and explicit tests**.

## Quick-start

Requires Python 3.12 or a compatible modern Python environment.

~~~bash
git clone https://github.com/CayelaemJ/CayelaemJ.git
cd CayelaemJ

cd projects/cdc-replay-lab
python -m unittest discover -v
cd ../data-quality-contracts
python -m unittest discover -v
cd ../sql-query-plans
python -m unittest discover -v
cd ../ai-output-evaluation
python -m unittest discover -v
~~~

The [GitHub Actions lab workflow](../../.github/workflows/engineering-labs-ci.yml) also runs all four suites on relevant PRs. Inspect the latest run before claiming that a new change passed.

## Lab 1. CDC Replay

**Path:** [projects/cdc-replay-lab](../../projects/cdc-replay-lab/)  
**Concepts:** immutable event ID log, latest-state projection, idempotency, order-by-source-sequence, tombstones and atomic failure.

**Exercise:** apply an account UPSERT, update it, DELETE it, then replay the same event IDs. The Gold aggregate should not double-count, and the Bronze record should show what happened.

**Production boundary:** no live binlog reader, distributed checkpointing, encryption, service identity or multi-writer transaction guarantee.

## Lab 2. Data Quality Contracts

**Path:** [projects/data-quality-contracts](../../projects/data-quality-contracts/)  
**Concepts:** required schema, duplicate keys, decimals, timezone-aware timestamps and freshness.

**Exercise:** pass a valid row, then a duplicate ID, a future timestamp and a NaN amount. Inspect the structured violations rather than silently modifying the input.

**Production boundary:** these are illustrative policies, not the actual validation rules of a bank or regulated system.

## Lab 3. SQL Query Plans

**Path:** [projects/sql-query-plans](../../projects/sql-query-plans/)  
**Concepts:** query-plan inspection, composite indexes, date-range filtering, sargability and unchanged aggregation results.

**Exercise:** compare a query plan before and after adding an index. Then wrap the indexed date in a function and examine what part of the index SQLite can use.

**Production boundary:** the in-memory SQLite result is not a cloud warehouse, Fabric or SQL Server benchmark.

## Lab 4. Offline AI Output Evaluation

**Path:** [projects/ai-output-evaluation](../../projects/ai-output-evaluation/)  
**Concepts:** evidence IDs, exact source quotes, structured outputs, invalid confidence, unsupported answer additions and human-review flags.

**Exercise:** invent a citation, alter an evidence quote, append an unsupported conclusion or introduce sensitive text. Observe how the evaluation refuses the response.

**Production boundary:** no external LLM is called. Quote matching is not semantic truth, model calibration, privacy certification or prompt-injection resistance.

## What the tests prove

| Lab | Local unit tests added and exercised | What is still outside scope |
|---|---:|---|
| CDC Replay | 5 | Actual source CDC and distributed recovery |
| Data Quality | 5 | Enterprise-specific policies and large datasets |
| SQL Plans | 6 | Production DB performance |
| AI Evaluation | 8 | Empirical LLM quality and complete safety |
| **Total** | **24** | The tests establish toy-example behaviour, not whole-product readiness |

The four suites have a passing GitHub Actions verification on the preceding portfolio CI work, and the handbook documentation must be checked separately. See the workflow for current evidence.

## Suggested review questions

- Which event or record is authoritative, and how is it identified?
- What invariant would fail if the same input arrived twice?
- Which outcome cannot be inferred from a unit-test success?
- If I changed the business grain or row-level access scope, what would have to change in the model?
- What happens when an AI provider fails or the input contains untrusted instructions?

That is the kind of conversation I prefer: working through assumptions and evidence, not counting badges.

[Browse all labs](../../projects/README.md) · [Back to my profile](../../README.md)

[← Chapter 07](07_SECURITY_AND_DELIVERY.md) · [Next: Leadership and future →](09_LEADERSHIP_AND_NEXT.md)
