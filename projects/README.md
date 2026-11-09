# Hands-on engineering labs

These are **runnable portfolio exercises**, distinct from the larger product repositories and confidential client work. They use only synthetic sample data, Python standard library dependencies and local tests.

| Lab | Demonstrates | Run |
| --- | --- | --- |
| [CDC Replay Lab](cdc-replay-lab/) | Event IDs, replay safety, Bronze/Silver/Gold, delete tombstones, source ordering and atomicity | `cd projects/cdc-replay-lab && python -m unittest discover -v` |
| [Data Quality Contracts](data-quality-contracts/) | Ingestion schema, primary keys, finite decimals, timestamp freshness and machine-readable violations | `cd projects/data-quality-contracts && python -m unittest discover -v` |
| [SQL Query Plans](sql-query-plans/) | Composite indexing, sargable date filtering, SQLite EXPLAIN output and result consistency | `cd projects/sql-query-plans && python -m unittest discover -v` |
| [Offline AI Output Evaluation](ai-output-evaluation/) | Extractive answer evidence, schema checks, review gating and synthetic negative tests | `cd projects/ai-output-evaluation && python -m unittest discover -v` |
| [OmniMaster Incident Academy](omnimaster-incident-academy/) | Eight educational decision scenarios across data, BI, APIs, security, AI and release controls | `cd projects/omnimaster-incident-academy && python -m unittest discover -v` |

The labs do **not** imply production deployment, live connectors, customer data access or security certification. Larger systems, Cloudflare/AWS integrations and AI workloads are documented in the corresponding full project repositories.


## Verification

Each project has an isolated standard-library test suite. The [Engineering Labs workflow](../.github/workflows/engineering-labs-ci.yml) runs all five project suites on relevant pull requests and main-branch changes; its actual execution status must be checked in GitHub Actions. This is *not* the deployment or production-security gate for other repositories.


## Learn and play

Start with the [seven-module OmniMaster Academy](../docs/OMNIMASTER_ACADEMY.md), then practise decisions in the [Arcade](../docs/OMNIMASTER_ARCADE.md) or run `python projects/omnimaster-incident-academy/quest.py` from the repository root.
