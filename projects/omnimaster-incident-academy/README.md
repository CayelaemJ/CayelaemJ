# OMNIMASTER INCIDENT ACADEMY
### A tiny engineering detective game by Cayelaem Jantjies

**Eight fictional incidents. Eight decisions. Your reasoning matters more than your rank.**

[Read the OmniMaster Arcade](../../docs/OMNIMASTER_ARCADE.md) · [Study the Academy](../../docs/OMNIMASTER_ACADEMY.md) · [GitHub cover](../../README.md)

## Play

Requires **Python 3.12+**. No packages, accounts, API keys, cloud services, persistence or network access.

~~~bash
cd projects/omnimaster-incident-academy
python quest.py
~~~

Run the tests:

~~~bash
python -m unittest discover -v
~~~

The game prints one situation and three actions. Choose **1**, **2**, **3**, **0** to skip or **q** to exit. Invalid input is explained and reprompted. After each decision, you see the correct option and an explanation. Finish all eight to receive a score, XP, rank and list of cases to review.

## The eight case files

| Case | Domain | What you practise |
|---|---|---|
| GRAIN-01 | Analytics | Invoice/delivery grain and double-counting |
| CDC-02 | Data engineering | Watermark collisions, replay and deletes |
| TENANT-03 | Backend security | Tenant and role enforcement at API boundaries |
| AI-04 | Applied AI | Grounded evidence versus fabricated confidence |
| CUTOVER-05 | Databases | Final sync, writer fencing and rollback |
| QUERY-06 | SQL performance | Indexes, sargability and query-plan verification |
| MFA-07 | Identity | Fresh step-up and server-side enforcement |
| RELEASE-08 | Release engineering | CI scope and actual deployment readiness |

## The scoring

You earn **10 XP per correct decision**, up to 80 XP. Ranks are Explorer, Curious Builder, Incident Investigator and Systems Architect. They're playful learning labels, not qualifications.

Each scenario is **synthetic or simplified**. The provided answer is appropriate to the described conditions but won't be universally correct for every system. Real architecture requires business constraints, legal/operational context and independent review.

## Learn instead of memorising

After finishing, choose a missed incident and write:

1. Which invariant is at risk?
2. Which layer owns the correction?
3. What test would reproduce the problem?
4. How would you know whether a production release is safe?
5. What does the proposed action *not* prove?

Continue with [the worked engineering workbook](../../docs/field-guide/03_ENGINEERING_WORKBOOK.md).

## Safety and privacy

The game runs **offline** with constant fictional scenarios. It makes no external requests, does not read local files, and doesn't save answers, profiles or scores. No hidden telemetry and no use of real customer, school, finance or employment data.

**The joke is that the strongest superpower here is a reproducible negative test.**
