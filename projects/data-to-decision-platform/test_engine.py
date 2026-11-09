"""Invariants for the synthetic and disposable data-to-decision lab."""
import sqlite3
import unittest
from dataclasses import replace

from engine import Event, Pipeline, sample_events, validate
from cli import demonstrate, failure_demonstration


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline()
        self.events = sample_events()

    def tearDown(self):
        self.pipeline.db.close()

    def test_sample_metrics(self):
        stats = self.pipeline.apply_batch(self.events)
        self.assertEqual(stats["accepted"], 8)
        self.assertEqual(self.pipeline.metrics_for("fictional-alpha")["balance_cents"], 23000)
        self.assertEqual(self.pipeline.metrics_for("fictional-beta")["balance_cents"], 37000)
        self.assertEqual(self.pipeline.metrics_for("fictional-alpha")["active_accounts"], 2)

    def test_idempotent_replay(self):
        self.pipeline.apply_batch(self.events)
        before = self.pipeline.snapshot()
        again = self.pipeline.apply_batch(self.events)
        self.assertEqual(again["duplicates"], 8)
        self.assertEqual(len(self.pipeline.events()), 8)
        self.assertEqual(before, self.pipeline.snapshot())

    def test_delete_preserves_bronze_and_tombstone(self):
        self.pipeline.apply_batch(self.events)
        row = self.pipeline.db.execute(
            "SELECT is_deleted,amount_cents FROM silver_accounts "
            "WHERE tenant='fictional-alpha' AND account='acct-b'"
        ).fetchone()
        self.assertEqual(row, (1, 0))
        self.assertTrue(any(e.operation == "DELETE" for e in self.pipeline.events()))

    def test_same_account_id_separate_tenants(self):
        self.pipeline.apply_batch(self.events)
        alpha = self.pipeline.db.execute(
            "SELECT amount_cents FROM silver_accounts WHERE tenant=? AND account=?",
            ("fictional-alpha", "acct-a"),
        ).fetchone()
        beta = self.pipeline.db.execute(
            "SELECT amount_cents FROM silver_accounts WHERE tenant=? AND account=?",
            ("fictional-beta", "acct-a"),
        ).fetchone()
        self.assertEqual(alpha, (14000,))
        self.assertEqual(beta, (32000,))

    def test_same_event_id_different_payload_fails(self):
        self.pipeline.apply_batch(self.events)
        conflict = replace(self.events[0], amount_cents=9999)
        with self.assertRaisesRegex(ValueError, "event ID reused"):
            self.pipeline.apply_batch((conflict,))
        self.assertEqual(len(self.pipeline.events()), 8)

    def test_duplicate_source_position_fails(self):
        self.pipeline.apply_batch(self.events)
        conflict = replace(self.events[0], event_id="evt-99", version=99)
        with self.assertRaises(sqlite3.IntegrityError):
            self.pipeline.apply_batch((conflict,))

    def test_atomic_rollback_on_invalid_later_event(self):
        self.pipeline.apply_batch(self.events)
        before = self.pipeline.snapshot()
        good = replace(self.events[0], event_id="evt-09", position=9, version=3)
        bad = replace(self.events[1], event_id="evt-10", position=10, version=3, amount_cents=-1)
        with self.assertRaises(ValueError):
            self.pipeline.apply_batch((good, bad))
        self.assertEqual(before, self.pipeline.snapshot())
        self.assertEqual(len(self.pipeline.events()), 8)

    def test_late_arriving_lower_version_is_recorded_but_not_projected(self):
        self.pipeline.apply_batch(self.events)
        before = self.pipeline.snapshot()
        old = replace(self.events[0], event_id="evt-09", position=9)
        stats = self.pipeline.apply_batch((old,))
        self.assertEqual(stats["stale"], 1)
        self.assertEqual(before, self.pipeline.snapshot())
        self.assertEqual(len(self.pipeline.events()), 9)
        self.assertTrue(self.pipeline.reconciles())

    def test_conflicting_same_account_version_fails(self):
        self.pipeline.apply_batch(self.events)
        # acct-a is at version 2 after the sample batch; a second distinct
        # event at version 2 is a true version conflict, not a stale v1 arrival.
        invalid = replace(self.events[0], event_id="evt-09", position=9, version=2, amount_cents=100)
        with self.assertRaisesRegex(ValueError, "conflicting events"):
            self.pipeline.apply_batch((invalid,))

    def test_batch_rollback_on_version_conflict(self):
        self.pipeline.apply_batch(self.events)
        good = replace(self.events[0], event_id="evt-09", position=9, version=3)
        bad = replace(self.events[0], event_id="evt-10", position=10, version=3)
        with self.assertRaisesRegex(ValueError, "conflicting events"):
            self.pipeline.apply_batch((good, bad))
        self.assertEqual(len(self.pipeline.events()), 8)

    def test_invalid_negative_balance(self):
        with self.assertRaises(ValueError):
            validate(replace(self.events[0], amount_cents=-1))

    def test_invalid_boolean_amount(self):
        with self.assertRaises(ValueError):
            validate(replace(self.events[0], amount_cents=True))

    def test_delete_carries_no_balance(self):
        with self.assertRaises(ValueError):
            validate(replace(self.events[0], operation="DELETE"))

    def test_naive_timestamp_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            validate(replace(self.events[0], occurred_at="2026-01-02T12:01:00"))

    def test_invalid_source_position(self):
        with self.assertRaises(ValueError):
            validate(replace(self.events[0], position=0))

    def test_invalid_tenant_identifier(self):
        with self.assertRaises(ValueError):
            validate(replace(self.events[0], tenant=""))
        with self.assertRaises(ValueError):
            self.pipeline.metrics_for("tenant'; DROP TABLE silver_accounts; --")

    def test_reconciliation_detects_projection_drift(self):
        self.pipeline.apply_batch(self.events)
        self.assertTrue(self.pipeline.reconciles())
        self.pipeline.db.execute(
            "UPDATE silver_accounts SET amount_cents=1 "
            "WHERE tenant='fictional-alpha' AND account='acct-a'"
        )
        self.pipeline.db.commit()
        self.assertFalse(self.pipeline.reconciles())

    def test_cli_demo(self):
        output = demonstrate()
        self.assertEqual(output["alpha_gold"]["balance_cents"], 23000)
        self.assertEqual(output["replay_batch"]["duplicates"], 8)
        self.assertTrue(output["reconciled"])

    def test_cli_failure(self):
        output = failure_demonstration()
        self.assertTrue(output["all_or_nothing"])
        self.assertTrue(output["event_log_unchanged"])
        self.assertTrue(output["error"])
        self.assertTrue(output["reconciled"])

    def test_invalid_event_type(self):
        with self.assertRaises(ValueError):
            self.pipeline.apply_batch(("not an event",))


if __name__ == "__main__":
    unittest.main()
