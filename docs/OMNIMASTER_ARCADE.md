# THE OMNIMASTER ARCADE
### Learn something, break something safely, and solve it like an engineer

[← GitHub cover](../README.md) · [Academy](OMNIMASTER_ACADEMY.md) · [Personal manual](OMNIMASTER_OPERATING_MANUAL.md) · [Play the terminal game](../projects/omnimaster-incident-academy/)

---

## 01. Incident Academy | The executable game

**Eight cases. Three choices each. Explanations after every decision.**

The game runs entirely offline using Python's standard library, with no personal data, scores uploaded, accounts or API keys.

~~~bash
git clone https://github.com/CayelaemJ/CayelaemJ.git
cd CayelaemJ/projects/omnimaster-incident-academy
python quest.py
~~~

The cases cover duplicated invoices, CDC freshness, cross-tenant access, AI citations, database cutovers, SQL indexing, MFA and release gates.

**[START THE INCIDENT ACADEMY →](../projects/omnimaster-incident-academy/)**

## 02. Choose your own production incident

You are the technical lead for a *fictional* analytics platform. It's Friday afternoon. A dashboard reports **6,000** in revenue while the source invoice shows **1,000**. One order has two deliveries and three inspections.

What's your first move?

<details>
<summary>A. Add a DISTINCT to the amount and send the release email</summary>

**Bad ending: The Mirage.** Two different orders can have the same amount. DISTINCT(amount) may hide duplication while losing legitimate revenue. You corrected a number without correcting its meaning.

**Recovery:** return to the source record, define each fact's grain, check join cardinality and write a reconciliation test. No production patch from this fictional story.

</details>

<details>
<summary>B. Check the join grain, then reconcile the source amount</summary>

**Good ending: The Investigator.** You discover 2 × 3 = 6 joined rows. Each repeats the original invoice value. Separate the invoice-grain measure from delivery and inspection counts, then verify the result remains stable when more inspections arrive.

**Unlocked skill:** trace a KPI defect upstream rather than reformatting the visual.

</details>

<details>
<summary>C. Rebuild the dashboard in an entirely different framework</summary>

**Bad ending: The Expensive Detour.** The wrong SQL can look wrong in any frontend. The root cause moves with the data. You're now debugging a new framework *and* the original accounting error.

**Recovery:** isolate the correct source measure before choosing any new platform.

</details>

## 03. A small gallery of fictional engineering villains

| Villain | Signature move | How to defeat it |
|---|---|---|
| **Count Duplicator** | Turns a one-to-many join into inflated revenue | Declare grain, reconcile counts, test cardinality |
| **The Green Pipeline** | Marks a batch successful without checkpoint progress | Progress invariant, retries, negative tests |
| **Captain Stale Cache** | Serves yesterday's truth with today's timestamp | Freshness SLA, provenance and invalidation |
| **The Privilege Phantom** | Hides a button but leaves the endpoint unguarded | Server-side permission and tenant checks |
| **Citation Phantom** | Invents a source the model never read | Grounded evidence and human review |
| **The Friday Cutover** | Wants to migrate without final sync or rollback | Writer fencing, parity, staged rollout |

They are invented characters. The failure classes are real engineering concerns.

## 04. Mini puzzles you can solve without a terminal

<details>
<summary>SQL puzzle: three sales rows total 120, 120, 80. What happens with SUM(DISTINCT amount)?</summary>

You get **200**, not the correct **320**. DISTINCT(amount) removes a legitimate duplicate value. Uniqueness belongs to the business event ID, not the amount column.

</details>

<details>
<summary>CDC puzzle: why doesn't filtering UPDATED_AT >= last_watermark give perfect event history?</summary>

It helps replay boundary rows but cannot reconstruct multiple changes overwritten in the same current-state record or physical deletes with no retained event. Replayed rows also need idempotent handling. Choose capture semantics that match the actual requirement.

</details>

<details>
<summary>Security puzzle: a React screen refuses a cross-tenant ID, but direct HTTP accepts it. Is the app secure?</summary>

No. Client-side rejection is useful feedback but not an authorisation boundary. The API must verify identity, operation and data scope server-side.

</details>

<details>
<summary>AI puzzle: the assistant claims 99.9% confidence, but its quote is not in the document. Should the answer pass?</summary>

No. Self-reported confidence is not proof. Check approved sources, actual evidence and task-level accuracy. Consequential decisions require human oversight.

</details>

## 05. The XP board (on the honour system)

| Badge | Earn it by doing this | Proof to keep |
|---|---|---|
| **Schema Sleuth** | Explain a grain mismatch and write a test | Before/after totals and query |
| **Replay Ranger** | Show that duplicate events don't duplicate state | Idempotency test |
| **API Gatekeeper** | Deny a cross-tenant request at the backend | Negative HTTP test |
| **Evidence Guardian** | Reject a fabricated AI citation | Input, expected result and test |
| **Rollback Pilot** | Demonstrate a reversible migration in a local environment | Restore/rollback transcript |
| **Documentation Wizard** | Teach someone how to run your system without help | Clean-run README and reviewer notes |

These are **self-study milestones**, not certifications, GitHub achievements or endorsed credentials. Don't make fake commits or issues to collect them.

## 06. Play the multiplayer version

Try this with a friend or study group:

1. **Investigator:** read a fictional defect and identify the invariant.
2. **Sceptic:** challenge the first proposed fix with a counterexample.
3. **Builder:** implement the smallest change in an isolated environment.
4. **Reviewer:** reproduce the negative test and check the documentation.
5. **Teacher:** explain the result in plain language.

Switch roles after each case. Nobody gets to solve a data-grain bug by changing CSS.

## 07. The easter egg: my real “superpowers”

<details>
<summary>Click to reveal the secret identity</summary>

I'm a developer who spent a lot of time making dashboards and slowly discovered that most important bugs live **behind** the dashboard.

I enjoy following those bugs until I understand SQL, backend logic, permissions, infrastructure or the business process well enough to explain what went wrong.

My current weakness: there is always another interesting system to investigate.

My preferred power-up: a smaller scope, a test that reproduces the problem and someone who challenges the assumptions.

</details>

## 08. More levels

[Volume III: Take the seven-module engineering course](OMNIMASTER_ACADEMY.md) · [Volume II: Work through seven technical exercises](field-guide/03_ENGINEERING_WORKBOOK.md) · [Run the four original labs](../projects/README.md) · [The INTJ chapter](personal/01_INTJ_AND_ME.md)

The game is fiction. The habit it teaches is simple:**New challenge:** build the real educational capstone in [Volume V](OMNIMASTER_BUILD_WITH_ME.md), follow the [30-day expedition](THIRTY_DAY_ENGINEERING_EXPEDITION.md), or open the [offline interactive study room](interactive/index.html).

 **question the easy answer, verify the invariant, and leave the system more understandable than you found it.**
