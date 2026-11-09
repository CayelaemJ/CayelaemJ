# Lesson 02 | SQL, data grain and analytical meaning

[← Lesson 01](01_START_HERE.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Next →](03_PIPELINES_AND_CDC.md)

## What I learned from manufacturing and enterprise BI

A query returning rows is not the same as a query returning the right facts. In banking, manufacturing and commercial research, I've encountered analytical questions where the business process crosses orders, employees, deliveries and measurements. Your job is to understand the **grain** before combining them.

## Start with a fictional dataset

~~~sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0)
);

CREATE TABLE deliveries (
    delivery_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    delivered_on TEXT NOT NULL
);

INSERT INTO orders VALUES (10, 2, 500000);
INSERT INTO deliveries VALUES (1, 10, '2026-01-01');
INSERT INTO deliveries VALUES (2, 10, '2026-01-03');
~~~

**The trap:** if you join orders to deliveries and sum the order's amount, you will count one order twice. The correct total of order values is still **500,000 cents**.

## Reconciliation exercise

First write a query to count deliveries per order:

~~~sql
SELECT order_id, COUNT(*) AS delivery_count
FROM deliveries
GROUP BY order_id;
~~~

Then try an order-level financial total without multiplying it:

~~~sql
SELECT SUM(amount_cents) AS total_order_amount_cents
FROM orders
WHERE order_id IN (
  SELECT DISTINCT order_id FROM deliveries
);
~~~

This example uses a subquery to keep the order-grain calculation clear. Other models might use separate fact tables or pre-aggregations; the right choice depends on the business question.

## The six checks I make

1. **Primary key:** What uniquely identifies a record?
2. **Grain:** Is each row an order, delivery, transaction or observation?
3. **Join cardinality:** How many rows do you expect after each join?
4. **Measure semantics:** Is the number a count, sum, ratio or distinct population?
5. **Time:** Are you reporting when an event happened or when the source was corrected?
6. **Access:** Does every filter preserve the organisation or person's permitted scope?

A result can be mathematically valid and semantically wrong. That's why I document how a metric should be interpreted.

## Index and query-plan lab

Use [SQL Query Plans Lab](../../projects/sql-query-plans/) to observe how query shape changes the planner's choices.

~~~bash
cd projects/sql-query-plans
python query_lab.py
python -m unittest discover -v
~~~

It illustrates a full scan, a composite index and a date predicate that stops being sargable after a function wraps the column. The lab uses SQLite, **not** a production Fabric or SQL Server benchmark.

## Make it more realistic

Extend the fictional tables with status, country, currency and correction timestamp. Then test:

- A customer with no deliveries.
- Two deliveries against the same order.
- Two different orders with equal values, demonstrating why DISTINCT(amount) is unsafe.
- A cancellation or corrected event.
- A cross-market filter that must not leak another market's data.

## Checkpoint

**Pass when:** you can show the expected source total, the modelled total and a regression test that fails when someone introduces an unsafe join.

**Explain it to a stakeholder:** “We were counting the same order once for each delivery. The model now counts orders at the correct level, while still letting us analyse delivery events separately.”

Next reading: [Analytics engineering handbook](../handbook/05_ANALYTICS_ENGINEERING.md) · [Worked query exercises](../field-guide/03_ENGINEERING_WORKBOOK.md).

[← Lesson 01](01_START_HERE.md) · [Next: Data pipelines →](03_PIPELINES_AND_CDC.md)
