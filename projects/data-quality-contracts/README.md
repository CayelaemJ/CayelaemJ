# Data Quality Contracts Lab

An executable, dependency-free **Python** mini-project for source-boundary quality gates. Given synthetic input rows, `check_records()` produces deterministic, machine-readable findings without silently modifying source values.

## Try it

```bash
cd projects/data-quality-contracts
python quality.py
python -m unittest discover -v
```

Checks: required fields, nonempty primary keys, duplicate IDs, finite non-negative decimal amounts, timezone-aware timestamps, future-clock skew, and freshness against a configurable SLA. The function returns `PASS` or `FAIL`, a count and row-level rule details; it never contacts a database or external API.

## Why

An ingestion pipeline needs a small number of clearly owned, testable contracts. Repeatedly validating the same field in incompatible ways across layers introduces latency without necessarily increasing correctness. This lab demonstrates useful checks at the boundary, with an explicit failure report rather than an invented 'cleaned' dataset.

## Limits

The rules are example policies, not universal accounting or banking standards. They do not include PII, production schemas, tenant context, data drift, statistical anomaly monitoring or any compliance certification. For high-volume processing, implement equivalent vectorized/distributed rules and write metrics, sample IDs and remediation decisions to an access-controlled store.
