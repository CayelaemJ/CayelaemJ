# Build With Me 04 | Take a number from SQL to a useful decision

[← Projections](03_PROJECTIONS_AND_GRAIN.md) · [Volume V](../OMNIMASTER_BUILD_WITH_ME.md) · [Next: Failure lab →](05_FAILURE_LAB.md)

## A number is only useful inside its meaning

I learned in banking, manufacturing and BI delivery that a dashboard metric is a **contract**. If two people read the same number differently, the software may be technically consistent but operationally misleading.

Our miniature pipeline returns two numbers: active-account count and a sum of fictional balances.

## Define the metric as if it mattered

| Property | Definition in this demo |
|---|---|
| **Name** | Current active-account balance |
| **Audience** | Hypothetical authorised member of one fictional tenant |
| **Grain** | Latest state per tenant/account |
| **Included** | Latest UPSERT versions not marked deleted |
| **Excluded** | DELETE tombstones and stale versions |
| **Currency** | Integer cents as a fictional unit, not a real banking ledger |
| **Time interpretation** | State resulting from applied events, not a guaranteed source-as-of timestamp |
| **Freshness** | The last applied event batch; no external source latency promise |
| **Trust** | Rebuild comparison from Bronze helps detect projection drift |

## Run the local calculation

~~~bash
python cli.py demo
~~~

Find the `alpha_gold` and `beta_gold` JSON objects. Explain why the total for alpha is **23,000** and for beta **37,000**.

Try dividing the total by the number of active accounts. It is mathematically possible, but is “average active-account balance” meaningful for the consumer? That depends on business intent and the distribution, not on how easy the expression is to write.

## The most important security caveat

The lab method `metrics_for(tenant)` takes a caller-provided tenant name and runs parameterised SQL. **That is not authentication or authorisation.** If someone published an HTTP endpoint accepting arbitrary tenant IDs, callers might request other tenants' figures.

In a real product, the server must authenticate the user, resolve their permitted tenant IDs from a trusted identity/relationship store, enforce the requested operation and test cross-tenant denial. The database's read-only role and row-level security can provide additional boundaries.

**Do not put this toy method on the public internet.**

## Your API design exercise

Without implementing a network server, write a design for:

~~~text
GET /api/reports/account-summary

Identity: signed, verified server session
Tenant scope: derived from authorised membership
Permission: reports.read
Response:
  tenant
  active_accounts
  balance_cents
  source_as_of (if the pipeline can truly provide it)
  freshness_status
Denial:
  unauthenticated -> 401
  insufficient permission -> 403
  wrong tenant -> 403/404 with no existence leak
~~~

Now write **negative tests first**: ordinary user, expired session, revoked membership, cross-tenant query, malformed account identifier and unexpected source lag.

## Data visualization exercise

Create a simple bar chart or console table for fictional-alpha and fictional-beta. Choose labels that disclose exactly what is represented. Then deliberately use the wrong label “real-time revenue” and explain why it is false.

**A dashboard tells a story. The best engineer makes sure it tells a true one.**

### Completion test

You can explain the metric to a non-technical person, identify its freshness limitations and design a server-side trust boundary before exposing it to users.

[← Chapter 03](03_PROJECTIONS_AND_GRAIN.md) · [Next: Break the system →](05_FAILURE_LAB.md)
