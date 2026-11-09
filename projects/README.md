# Hands-on engineering labs

These are **runnable portfolio exercises**, distinct from the larger product repositories and confidential client work. They use only synthetic sample data, Python standard library dependencies and local tests.

| Lab | Demonstrates | Run |
| --- | --- | --- |
| [CDC Replay Lab](cdc-replay-lab/) | Event IDs, replay safety, Bronze/Silver/Gold, delete tombstones, source ordering and atomicity | `cd projects/cdc-replay-lab && python -m unittest discover -v` |
| [Data Quality Contracts](data-quality-contracts/) | Ingestion schema, primary keys, finite decimals, timestamp freshness and machine-readable violations | `cd projects/data-quality-contracts && python -m unittest discover -v` |

The labs do **not** imply production deployment, live connectors, customer data access or security certification. Larger systems, Cloudflare/AWS integrations and AI workloads are documented in the corresponding full project repositories.
