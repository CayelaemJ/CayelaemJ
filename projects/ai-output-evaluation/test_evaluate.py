import unittest

from evaluate import evaluate


class OutputEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.quote = "Synthetic energy usage is aggregated by facility and week."
        self.sources = {"doc-1": self.quote + " No real user records are included."}
        self.payload = {
            "answer": self.quote,
            "evidence": [{"source_id": "doc-1", "quote": self.quote}],
            "confidence": 0.9,
            "requires_human_review": False,
        }

    def check_failure(self, expected, payload=None, **kwargs):
        outcome = evaluate(payload if payload is not None else self.payload, self.sources, **kwargs)
        self.assertEqual(outcome["status"], "FAIL")
        self.assertIn(expected, outcome["violations"])

    def test_valid_extractive_answer(self):
        self.assertEqual(evaluate(self.payload, self.sources)["status"], "PASS")

    def test_invented_source(self):
        changed = {**self.payload, "evidence": [{"source_id": "made-up", "quote": self.quote}]}
        self.check_failure("unknown_source", changed)

    def test_fabricated_quote(self):
        changed = {**self.payload, "evidence": [{"source_id": "doc-1", "quote": "Entirely fictional claim and evidence string."}]}
        self.check_failure("quote_not_in_source", changed)

    def test_answer_extra_claim(self):
        changed = {**self.payload, "answer": self.quote + " Costs are zero."}
        self.check_failure("non_extractive_answer", changed)

    def test_human_review_for_uncertain_or_sensitive(self):
        self.check_failure("human_review_required", {**self.payload, "confidence": 0.5})
        self.check_failure("human_review_required", sensitive=True)
        self.assertEqual(evaluate({**self.payload, "requires_human_review": True},
                                  self.sources, sensitive=True)["status"], "PASS")

    def test_sensitive_email_and_credentials(self):
        changed = {**self.payload, "answer": self.quote + " user@example.org"}
        self.check_failure("possible_sensitive_text", changed)
        changed = {**self.payload, "answer": self.quote + " password:secret"}
        self.check_failure("possible_sensitive_text", changed)

    def test_rejects_schema_and_invalid_confidence(self):
        self.check_failure("schema_mismatch", {"answer": self.quote})
        self.check_failure("invalid_confidence", {**self.payload, "confidence": float("nan")})
        self.check_failure("invalid_confidence", {**self.payload, "confidence": True})

    def test_empty_and_unknown_evidence(self):
        self.check_failure("invalid_evidence_count", {**self.payload, "evidence": []})
        self.check_failure("invalid_evidence_item", {**self.payload, "evidence": ["bad"]})


if __name__ == "__main__":
    unittest.main()
