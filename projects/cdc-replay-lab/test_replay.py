import unittest

from replay import Change, ReplayStore


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.store = ReplayStore()

    def test_replay_is_idempotent(self):
        event = Change("e1", "acct", 1, "UPSERT", "20.00")
        self.assertEqual(self.store.apply_batch([event])["applied"], 1)
        self.assertEqual(self.store.apply_batch([event])["duplicate"], 1)
        self.assertEqual(self.store.gold(), {"active_accounts": 1, "total_amount": "20.00"})

    def test_out_of_order_and_tombstone(self):
        result = self.store.apply_batch([
            Change("e3", "acct", 3, "DELETE"),
            Change("e2", "acct", 2, "UPSERT", "42"),
        ])
        self.assertEqual(result, {"applied": 1, "duplicate": 0, "stale": 1})
        self.assertEqual(self.store.gold()["active_accounts"], 0)
        self.store.apply_batch([Change("e4", "acct", 4, "UPSERT", "15")])
        self.assertEqual(self.store.gold()["total_amount"], "15")

    def test_invalid_batch_is_atomic(self):
        with self.assertRaises(ValueError):
            self.store.apply_batch([
                Change("good", "acct", 1, "UPSERT", "10"),
                Change("bad", "acct", 2, "UPSERT", "not-money"),
            ])
        self.assertEqual(self.store.state(), [])

    def test_conflicting_event_id_rejected(self):
        self.store.apply_batch([Change("e1", "acct", 1, "UPSERT", "10")])
        with self.assertRaises(ValueError):
            self.store.apply_batch([Change("e1", "acct", 1, "UPSERT", "999")])
        self.assertEqual(self.store.gold()["total_amount"], "10")

    def test_no_nan_or_negative_amount(self):
        for invalid in ("NaN", "Infinity", "-2"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.store.apply_batch([Change("e" + invalid, "acct", 1, "UPSERT", invalid)])


if __name__ == "__main__":
    unittest.main()
