"""Offline extractive-answer evidence checker, not a full AI safety evaluator."""
from __future__ import annotations

import json
import math
import re

# Illustrative detection only. Do not use regex-only scanning as a privacy boundary.
EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
CREDENTIAL = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{12,}|(?:password|api[_-]?key)\s*[:=]\s*\S+)", re.I)
REQUIRED = {"answer", "evidence", "confidence", "requires_human_review"}


def evaluate(payload: object, sources: dict[str, str], *, sensitive: bool = False) -> dict:
    """Require exact extractive text from known evidence, with explicit review gates.

    This verifies schema and substring grounding only, never semantic truth or permission.
    """
    violations: list[str] = []
    if not isinstance(payload, dict) or set(payload) != REQUIRED:
        return {"status": "FAIL", "violations": ["schema_mismatch"]}
    if not isinstance(sources, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in sources.items()
    ):
        return {"status": "FAIL", "violations": ["invalid_sources"]}
    answer, evidence, confidence, human = (payload[k] for k in (
        "answer", "evidence", "confidence", "requires_human_review"))
    if not isinstance(answer, str) or not answer.strip() or len(answer) > 750:
        violations.append("invalid_answer")
    if not isinstance(evidence, list) or not (1 <= len(evidence) <= 3):
        violations.append("invalid_evidence_count")
    else:
        quotes = []
        for item in evidence:
            if not isinstance(item, dict) or set(item) != {"source_id", "quote"}:
                violations.append("invalid_evidence_item")
                continue
            source_id, quote = item["source_id"], item["quote"]
            if not isinstance(source_id, str) or source_id not in sources:
                violations.append("unknown_source")
                continue
            if not isinstance(quote, str) or not (12 <= len(quote) <= 240):
                violations.append("invalid_quote")
                continue
            if quote not in sources[source_id]:
                violations.append("quote_not_in_source")
            quotes.append(quote)
        if isinstance(answer, str) and answer.strip() != "\n".join(quotes):
            violations.append("non_extractive_answer")
    if (isinstance(confidence, bool) or not isinstance(confidence, (int, float))
            or not math.isfinite(confidence) or not 0 <= confidence <= 1):
        violations.append("invalid_confidence")
    if type(human) is not bool:
        violations.append("invalid_review_flag")
    elif (sensitive or (isinstance(confidence, (int, float))
                        and not isinstance(confidence, bool)
                        and math.isfinite(confidence) and confidence < 0.8)) and not human:
        violations.append("human_review_required")
    if isinstance(answer, str) and (EMAIL.search(answer) or CREDENTIAL.search(answer)):
        violations.append("possible_sensitive_text")
    return {"status": "PASS" if not violations else "FAIL", "violations": sorted(set(violations))}


if __name__ == "__main__":
    source = {"example-1": "Water meters transmit measurements every fifteen minutes during the pilot."}
    quote = "Water meters transmit measurements every fifteen minutes"
    response = {"answer": quote, "evidence": [{"source_id": "example-1", "quote": quote}],
                "confidence": 0.92, "requires_human_review": False}
    print(json.dumps(evaluate(response, source), indent=2))
