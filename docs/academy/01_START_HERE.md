# Lesson 01 | Learn how to learn engineering

[← Academy](../OMNIMASTER_ACADEMY.md) · [Next →](02_SQL_AND_MODELLING.md)

## Why I start with questions, not frameworks

My background in Statistics and Data Science taught me to separate a hypothesis from evidence. My time in BI, manufacturing and full-stack work taught me something less academic: most expensive software mistakes start with a **bad assumption about what a record or action means**.

Before opening the code editor, answer: What problem exists? Who experiences it? What would success change? Which system knows the truth? How would a wrong result hurt someone?

## Your starter toolkit

**Minimum:** Python 3.12+, Git, a text editor, a terminal and SQLite (the Python sqlite3 module is sufficient). Node.js and a browser are useful later for application work. Everything here can be done with fictional data.

**Recommended folder convention:**

~~~text
my-engineering-workbook/
  README.md
  docs/
    problem.md
    architecture.md
    decisions.md
    incident-log.md
  data/
    sample.csv
  src/
  tests/
  .gitignore
~~~

Do not copy your employer's configuration into the repo. Use fake values in documentation and keep secrets outside source control.

## First exercise: turn a vague request into a contract

**Request:** “Make our deliveries dashboard accurate.”

Define a fictional order system with an order ID, delivery ID, delivery status, event time and updated time.

Write down:

1. What does **delivered** mean: dispatch recorded, customer signed, or carrier confirmed?
2. Can one order have several deliveries?
3. What happens when a delivery is cancelled or corrected?
4. Which people can see the records?
5. What would an automatic test need to assert?

**My working answer:** I would not start by making a graph. I'd define the source grain (one row per delivery event), stable keys, status transitions and a reconciliation baseline. Then I would build a small query that answers a testable question, for example: how many distinct orders have at least one completed delivery during a fixed period?

The definition is more important than the syntax.

## The investigation loop

~~~mermaid
flowchart LR
    Q["Question"] --> H["Hypothesis"]
    H --> E["Small experiment"]
    E --> O["Observed result"]
    O --> D["Document decision"]
    D -->|"New evidence"| Q
~~~

Use this loop every time you hit an unfamiliar tool. It is faster than changing seven things at once and then guessing which one mattered.

## What to commit

- A one-page problem statement with the business event and expected output.
- A fictional dataset with at least one duplicate, one missing value and one correction.
- A test that currently fails because the contract is unclear.
- A short decision record explaining how you resolved the ambiguity.

## Checkpoint

**You pass when:** another person can explain what your program will count and what it will reject before seeing its source code.

**Common failure:** jumping into cloud hosting because a diagram looks more professional. The same mistake is now remote and has a bill.

Further reading: [Volume I: The engineer](../handbook/01_THE_ENGINEER.md) · [Personal systems-thinking story](../personal/02_WHY_I_THINK_IN_SYSTEMS.md).

[← Academy](../OMNIMASTER_ACADEMY.md) · [Next: SQL and modelling →](02_SQL_AND_MODELLING.md)
