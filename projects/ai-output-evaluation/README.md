# Offline AI Output Evaluation Lab

A small, reproducible, model-agnostic **Python** example showing how an application can validate strictly structured, *extractive* answers against synthetic documents before presentation to a user. No model/API is contacted.

## Run locally

```bash
cd projects/ai-output-evaluation
python evaluate.py
python -m unittest discover -v
```

`evaluate(payload, sources, sensitive=False)` checks:

- Exact expected JSON shape with `answer`, `evidence`, `confidence` and `requires_human_review`.
- Every evidence entry references a provided source ID and quotes an exact substring of that source.
- The displayed answer contains **only the concatenated source quotes**. No freeform summary is accepted.
- Confidence is a finite number between 0 and 1, and low-confidence or flagged sensitive tasks require a human review marker.
- Illustrative email/key/password-pattern checks flag possible sensitive content.

Eight Python standard-library unit tests passed locally, covering valid output, invented citations, unsupported additions, malformed schema/confidence, and review flags.

## What this does **not** establish

A matching substring is **not proof of truth, safe advice, source authenticity, legal permission, bias/fairness, correct attribution, or protection from prompt injection**. Source text itself can be misleading or malicious. Regex patterns are demonstrative and cannot replace privacy/security safeguards. The confidence value is claimed by the caller; it is **not calibrated** here. No external model was evaluated.

For a real applied-AI release, layer in independently curated ground-truth datasets, semantic/quality review, privacy redaction, abuse tests, per-task metrics, human decision controls, provider fallback, latency and cost budgets. Do not use this toy evaluator to approve real learner, financial or employment decisions.
