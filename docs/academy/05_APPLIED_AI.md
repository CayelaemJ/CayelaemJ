# Lesson 05 | Applied AI that earns its place in the product

[← Lesson 04](04_BUILD_APPLICATIONS.md) · [Academy](../OMNIMASTER_ACADEMY.md) · [Next →](06_SECURITY_AND_DELIVERY.md)

## AI isn't the product just because you called an API

I've explored AI inside learner assessment, operational assistance and independent software workflows. The interesting question is not how to obtain a chatbot response. It is how to make the result **useful, properly scoped and safe to reject**.

## An applied AI workflow

**Example:** a fictional school teacher wants help creating a question from an approved reading passage.

1. Confirm the teacher's permitted document and role.
2. Retrieve only an approved, scoped passage.
3. Ask the model for a bounded structured response.
4. Validate required fields and evidence references.
5. Reject unsupported claims or uncertain output.
6. Require educator review before anything becomes an official assessment.
7. Record outcome and measured cost/latency, without logging unnecessary learner data.

~~~mermaid
flowchart LR
    A["Permitted task"] --> B["Approved source"]
    B --> C["Model call"]
    C --> D["Schema + evidence checks"]
    D --> E{"Passes?"}
    E -->|"Yes"| H["Human review if needed"]
    E -->|"No"| F["Safe no-answer / correction"]
~~~

This diagram describes an approach, not a claim of all flows being live in CABO.

## Start without an LLM

A good evaluator should also work on known synthetic examples. Study the [Offline AI Output Evaluation Lab](../../projects/ai-output-evaluation/).

~~~bash
cd projects/ai-output-evaluation
python evaluate.py
python -m unittest discover -v
~~~

The demo checks exact source quotations, identifiers, fields and review flags. **It is intentionally not a semantic or privacy certification.**

## Build your own evaluation set

Make fictional documents and at least eight test cases:

| ID | Scenario | Correct disposition |
|---|---|---|
| E01 | Exact answer with correct quoted source | Accept extractive response |
| E02 | Source ID does not exist | Reject |
| E03 | Quote does not appear in source | Reject |
| E04 | Model adds unsupported conclusion | Reject |
| E05 | Source document contains conflicting facts | Refer for review |
| E06 | Document includes instruction to ignore system policy | Ignore untrusted instructions |
| E07 | Provider times out or refuses | Safe fallback or no-decision |
| E08 | Personal information appears in output | Block or route to approved privacy workflow |

You must write a **clear rubric** for each test before evaluating a model. Otherwise the benchmark can be changed until the model seems accurate.

## The design decisions that cost real money

- **Latency:** can the user wait? Should the application respond asynchronously?
- **Cost:** how many tokens and calls does a typical workflow use?
- **Provider failure:** what happens on HTTP 402, 429, 500 or timeout?
- **Privacy:** do you have authority to send this data to that provider?
- **Quality:** do your tests measure the actual outcome, not only well-formed JSON?
- **Human review:** who accepts responsibility for consequential actions?

Model fallback can help availability but is not necessarily safer. Different providers can disagree in ways you must evaluate.

## Learning checkpoint

**Pass when:** your demo rejects fabricated evidence and has a documented human/no-answer path. You should be able to explain where semantic truth, calibration, fairness and legal checks are still missing.

**Stretch challenge:** compare two models on a synthetic benchmark, record accuracy, latency and cost, but only if you have authorised access and understand the provider's data terms. The core module requires no paid account.

Related: [Applied AI chapter](../handbook/06_PRODUCTS_AND_AI.md) · [Architecture atlas](../field-guide/01_ARCHITECTURE_ATLAS.md).

[← Lesson 04](04_BUILD_APPLICATIONS.md) · [Next: Security and delivery →](06_SECURITY_AND_DELIVERY.md)
