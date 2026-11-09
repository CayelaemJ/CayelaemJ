"""Offline regression tests for the fictional OmniMaster Incident Academy."""
import unittest

from quest import INCIDENTS, grade, play, rank


class IncidentAcademyTests(unittest.TestCase):
    def test_all_answers_are_valid_unique_incidents(self):
        self.assertEqual(len(INCIDENTS), 8)
        self.assertEqual(len({q.code for q in INCIDENTS}), 8)
        self.assertTrue(all(len(q.options) == 3 and q.answer in (1, 2, 3) for q in INCIDENTS))

    def test_all_correct_earns_maximum(self):
        result = grade(q.answer for q in INCIDENTS)
        self.assertEqual(result["correct"], 8)
        self.assertEqual(result["xp"], 80)
        self.assertEqual(result["rank"], "Systems Architect")
        self.assertEqual(result["review_codes"], [])

    def test_skip_earns_no_xp_and_is_reported(self):
        answers = [item.answer for item in INCIDENTS]
        answers[0] = 0
        result = grade(answers)
        self.assertEqual(result["correct"], 7)
        self.assertEqual(result["xp"], 70)
        self.assertEqual(result["review_codes"], ["GRAIN-01"])

    def test_wrong_answer_is_not_silently_accepted(self):
        answers = [1] * len(INCIDENTS)
        result = grade(answers)
        expected = sum(1 for item in INCIDENTS if item.answer == 1)
        self.assertEqual(result["correct"], expected)
        self.assertEqual(len(result["review_codes"]), len(INCIDENTS) - expected)

    def test_missing_answers_rejected(self):
        with self.assertRaises(ValueError):
            grade([1])

    def test_extra_answers_rejected(self):
        with self.assertRaises(ValueError):
            grade([1] * (len(INCIDENTS) + 1))

    def test_invalid_values_rejected(self):
        for bad in (-1, 4, True, 2.0, "1"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                grade([bad] + [0] * (len(INCIDENTS) - 1))

    def test_rank_thresholds(self):
        self.assertEqual(rank(8), "Systems Architect")
        self.assertEqual(rank(7), "Systems Architect")
        self.assertEqual(rank(6), "Incident Investigator")
        self.assertEqual(rank(4), "Curious Builder")
        self.assertEqual(rank(0), "Explorer")

    def test_invalid_rank_rejected(self):
        for value in (-1, 9, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                rank(value)

    def test_play_all_correct(self):
        answers = iter(str(item.answer) for item in INCIDENTS)
        output = []
        report = play(input_fn=lambda _: next(answers), output_fn=output.append)
        self.assertEqual(report["correct"], 8)
        self.assertTrue(any("COMPLETE" in line for line in output))

    def test_invalid_input_reprompts(self):
        answers = iter(["not a choice", "10", *[str(q.answer) for q in INCIDENTS]])
        output = []
        report = play(input_fn=lambda _: next(answers), output_fn=output.append)
        self.assertEqual(report["correct"], 8)
        self.assertEqual(sum("Please choose" in line for line in output), 2)

    def test_quit_does_not_write_state(self):
        output = []
        report = play(input_fn=lambda _: "q", output_fn=output.append)
        self.assertIsNone(report)
        self.assertTrue(any("Nothing was saved" in line for line in output))

    def test_eof_is_safe(self):
        output = []

        def ending(_):
            raise EOFError

        report = play(input_fn=ending, output_fn=output.append)
        self.assertIsNone(report)
        self.assertTrue(any("Session ended safely" in line for line in output))


if __name__ == "__main__":
    unittest.main()
