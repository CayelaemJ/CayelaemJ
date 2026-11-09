# Personal Chapter 04 | How to work with me (and a few quirks)

[← My range across IT](03_IT_RANGE_AND_LIMITS.md) · [Operating manual](../OMNIMASTER_OPERATING_MANUAL.md) · [Enter the arcade →](../OMNIMASTER_ARCADE.md)

I want my work to be serious. I don't need the GitHub to be solemn.

## A collaborator's cheat sheet

| If you want to… | The best way to work with me |
|---|---|
| **Describe a business problem** | Tell me who is affected, what the current result is and what correct would look like |
| **Report a bug** | Include an example, expected/actual outcome and the environment; a screenshot can help but source data semantics matter more |
| **Suggest an architecture** | Explain the constraints and why the trade-off is worthwhile; I don't need every answer to use my favourite stack |
| **Review my work** | Challenge assumptions and failure cases directly; specific feedback is useful |
| **Give me autonomy** | Agree on the outcome, guardrails and decision points; then let me investigate and show evidence |
| **Ask for an update** | I should distinguish done, tested, staging, blocked and proposed, with links to evidence |
| **Disagree with me** | Show the counterexample; if the evidence changes, the design should change |

## My default thinking pattern

**Problem → source → constraints → model → implementation → tests → release evidence.**

If I sound overly interested in the source table for a UI bug, it's probably because I have seen a clean interface present incorrect information before.

## Things I enjoy

I like engineering puzzles that require a little detective work. I enjoy taking a vague business request and making the invisible system visible. I like the point where a query plan, data model, API contract and UI all tell the same story. And I enjoy building things independently, not only to ship products but to test ideas that cross disciplines.

Some of that shows up in my OmniMaster persona. The superhero theme is playful. The desire to connect systems, learn deeply and solve real problems is sincere.

## A tiny personality stress test

<details>
<summary>Someone says: “We only need a simple dashboard.”</summary>

My first thoughts: What is the business grain? Where does the data come from? What is the access boundary? Is the refresh promise accurate? Are we about to spend two months on a problem that needs one good SQL query?

Then I remember the useful skill is not listing every possible failure. It is asking the **few questions that change the design**.

</details>

<details>
<summary>Someone says: “The CI passed so production is ready.”</summary>

I would ask what CI actually tested and on which commit. Unit tests, integration checks, migration rehearsal, real privileges and rollback all prove different things. “Green” is a claim with a scope.

</details>

<details>
<summary>Someone says: “Let's add AI to everything.”</summary>

I'd start with the user problem. If deterministic software solves it, use that. If AI meaningfully helps, define the source evidence, permitted data, output contract, evaluation and human control. A model call shouldn't become a product requirement by accident.

</details>

## The part I actively work on

I enjoy independence and control over a complete problem. That can become a trap if I take on too much, overengineer a solution or communicate after the fact. The improvement is practical: smaller milestones, documented decision points, early feedback, clear ownership and the humility to ask a specialist.

I want to be the person who can diagnose across layers **and** bring other people into the work.

## A personal code of conduct

- No pretending a prototype is a shipped product.
- No exposing client records to prove my ability.
- No demeaning the person who spotted a bug.
- No confusing a clever technical answer with a useful one.
- No hiding uncertainty behind a personality label.
- No treating the hardware team as somehow less technical because their expertise is different.
- Keep the fun. Real engineering has enough incident reports already.

## The unofficial scorecard

| Attribute | What I aspire to |
|---|---|
| Curiosity | High enough to ask a second question |
| Rigour | High enough to test the first answer |
| Adaptability | High enough to change the design |
| Communication | Clear enough that someone else can use it |
| Humility | High enough to say “I don't know yet” |
| Playfulness | Enough to make the repository enjoyable |

## What is an OmniMaster?

Not somebody who is magically certified in every technology. An OmniMaster is the character I use to express an engineering ambition: **understand enough of every connected layer to make the whole system better**, while respecting the specialists and people who make it possible.

And yes, it is perfectly reasonable to have a technical autobiography with an arcade. If a repository can contain a YAML file that controls a release, it can survive a small personality.

[Visit the OmniMaster Arcade](../OMNIMASTER_ARCADE.md) · [Study in the Academy](../OMNIMASTER_ACADEMY.md) · [Back to the operating manual](../OMNIMASTER_OPERATING_MANUAL.md)
