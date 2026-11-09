# SQL Query Plans Lab

A runnable analytics-engineering lab using deterministic fictional order data and the Python standard library's SQLite driver.

## Run

```bash
cd projects/sql-query-plans
python query_lab.py
python -m unittest discover -v
```

The demo creates **2,400 synthetic orders** (tenant, status, date, amount in integer cents) in a disposable in-memory database and compares the same analytical aggregation before and after a composite index on `(tenant_id, status, created_on)`. The result must remain identical.

**Observed locally (SQLite, Python 3.13):**

- Before index: `SCAN orders`.
- After index: `SEARCH orders USING INDEX idx_orders_tenant_status_date (tenant_id=? AND status=? AND created_on>? AND created_on<?)`.
- Filtering with `substr(created_on, 1, 7)` prevents the date-range portion of that index from being used.
- Six local unit tests passed.

This is **not a production throughput benchmark**. SQLite's optimizer, data distribution and in-memory storage differ from PostgreSQL, SQL Server, Fabric and cloud warehouses. Validate real query plans, selectivity, cardinality, grain, statistics, network and concurrent load on the actual target engine.

No accounts, credentials, external databases or real customer records are used.
