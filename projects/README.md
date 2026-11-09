# Hands-on engineering labs

These are **runnable portfolio exercises**, distinct from the larger product repositories and confidential client work. They use only synthetic sample data, Python standard library dependencies and local tests.

| Lab | Demonstrates | Run |
| --- | --- | --- |
| [CDC Replay Lab](cdc-replay-lab/) | Event IDs, replay safety, Bronze/Silver/Gold, delete tombstones, source ordering and atomicity | `cd projects/cdc-replay-lab && python -m unittest discover -v` |
| [Data Quality Contracts](data-quality-contracts/) | Ingestion schema, primary keys, finite decimals, timestamp freshness and machine-readable violations | `cd projects/data-quality-contracts && python -m unittest discover -v` |
| [SQL Query Plans](sql-query-plans/) | Composite indexing, sargable date filtering, SQLite EXPLAIN output and result consistency | `cd projects/sql-query-plans && python -m unittest discover -v` |
| [Offline AI Output Evaluation](ai-output-evaluation/) | Extractive answer evidence, schema checks, review gating and synthetic negative tests | `cd projects/ai-output-evaluation && python -m unittest discover -v` |
| [OmniMaster Incident Academy](omnimaster-incident-academy/) | Eight educational decision scenarios across data, BI, APIs, security, AI and release controls | `cd projects/omnimaster-incident-academy && python -m unittest discover -v` |
| [Data-to-Decision Platform](data-to-decision-platform/) | End-to-end synthetic event ingestion, atomic SQLite projection, tenant metrics, replay and reconciliation | `cd projects/data-to-decision-platform && python -m unittest discover -v` |
| [Reliability & Recovery Lab](reliability-recovery-lab/) | Job states, bounded retries, dead letters, duplicate effects, audit trail and safe recovery | `cd projects/reliability-recovery-lab && python -m unittest discover -v` |

The labs do **not** imply production deployment, live connectors, customer data access or security certification. Larger systems, Cloudflare/AWS integrations and AI workloads are documented in the corresponding full project repositories.


## Verification

Each project has an isolated standard-library test suite. The [Engineering Labs workflow](../.github/workflows/engineering-labs-ci.yml) runs all seven project suites plus the static browser study-room tests on relevant pull requests and main-branch changes; its actual execution status must be checked in GitHub Actions. This is *not* the deployment or production-security gate for other repositories.


## Learn and play

Start with the [seven-module OmniMaster Academy](../docs/OMNIMASTER_ACADEMY.md), then practise decisions in the [Arcade](../docs/OMNIMASTER_ARCADE.md) or run `python projects/omnimaster-incident-academy/quest.py` from the repository root.


## New end-to-end study path

[**Volume VII: Reliability Engineering & the Human Experience**](../docs/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md) teaches retry rules, dead-letter recovery, local audit traces and truthful UI status with a runnable lab.

[**Volume V: Build a System With Me**](../docs/OMNIMASTER_BUILD_WITH_ME.md) uses the complete synthetic Data-to-Decision lab to teach contracts, transactional ingestion, metric grain and failure recovery. Pair it with the [30-Day Engineering Expedition](../docs/THIRTY_DAY_ENGINEERING_EXPEDITION.md) and [offline study room](../docs/interactive/index.html).
