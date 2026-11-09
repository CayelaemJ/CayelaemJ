"""Regression and failure-path suite for the synthetic OmniMaster Reliability Lab."""
import unittest

from reliability import ReliabilityLab, backoff, clock, demonstration, identifier


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.lab = ReliabilityLab()

    def tearDown(self):
        self.lab.db.close()

    def submit(self, job="job-one", tenant="tenant-one", effect="effect-one",
               message="fictional notice", now=0):
        return self.lab.submit(job, tenant, effect, {"message": message}, now)

    def test_submit_initial_status(self):
        self.assertTrue(self.submit())
        self.assertEqual(self.lab.jobs_for("tenant-one")[0]["status"], "PENDING")
        self.assertEqual(self.lab.history_for("job-one", "tenant-one"), [("SUBMITTED", 0, 0)])

    def test_replay_identical_job_id_is_harmless(self):
        self.submit()
        self.assertFalse(self.submit())
        self.assertEqual(len(self.lab.jobs_for("tenant-one")), 1)
        self.assertEqual(len(self.lab.history_for("job-one", "tenant-one")), 1)

    def test_reused_job_id_different_payload_is_rejected(self):
        self.submit()
        with self.assertRaisesRegex(ValueError, "job ID reused"):
            self.submit(message="changed")
        self.assertEqual(self.lab.jobs_for("tenant-one")[0]["status"], "PENDING")

    def test_reused_job_id_different_tenant_is_rejected(self):
        self.submit()
        with self.assertRaises(ValueError):
            self.submit(tenant="tenant-two")

    def test_invalid_identifiers_rejected(self):
        for invalid in ("", "invalid tenant", "Uppercase", "sql';DROP", "a" * 60):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.lab.submit("job-one", invalid, "effect-one", {"message": "ok"})

    def test_invalid_payload_rejected(self):
        for invalid in ({}, {"extra": "x", "message": "x"}, {"message": ""},
                        {"message": " "}, {"message": 123}, {"message": "x" * 161}, "x"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.lab.submit("job-one", "tenant-one", "effect-one", invalid)

    def test_invalid_timeline_rejected(self):
        for invalid in (-1, 1.2, True, "5"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                clock(invalid)

    def test_invalid_limit_rejected(self):
        self.submit()
        for invalid in (0, -1, 1001, True, "2"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.lab.run_due(0, limit=invalid)

    def test_fault_script_validation(self):
        self.submit()
        for invalid in ({"a": "bad"}, {("job-one", 0): "error"}, {("job-one", 1): "Bad Error"}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.lab.run_due(0, faults=invalid)
        self.assertEqual(self.lab.jobs_for("tenant-one")[0]["attempts"], 0)

    def test_backoff_is_bounded(self):
        self.assertEqual([backoff(i) for i in (1, 2, 3, 4, 100)], [2, 4, 8, 8, 8])

    def test_backoff_rejects_invalid_attempts(self):
        for invalid in (0, -1, True, 1.5):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                backoff(invalid)

    def test_successful_work_creates_single_local_effect(self):
        self.submit()
        outcome = self.lab.run_due(0)
        self.assertEqual(outcome[0]["state"], "DONE")
        self.assertEqual(self.lab.jobs_for("tenant-one")[0]["status"], "DONE")
        self.assertEqual(self.lab.effects_for("tenant-one"), ["effect-one"])

    def test_completed_jobs_not_reprocessed(self):
        self.submit()
        self.lab.run_due(0)
        self.assertEqual(self.lab.run_due(999), [])
        self.assertEqual(len(self.lab.effects_for("tenant-one")), 1)

    def test_first_fault_retries_after_two_ticks(self):
        self.submit()
        outcome = self.lab.run_due(0, {("job-one", 1): "source_unavailable"})
        self.assertEqual(outcome, [{"job": "job-one", "state": "RETRY", "attempt": 1, "next_due": 2}])
        self.assertEqual(self.lab.run_due(1), [])
        self.assertEqual(self.lab.effects_for("tenant-one"), [])
        result = self.lab.run_due(2)
        self.assertEqual(result[0]["attempt"], 2)
        self.assertEqual(result[0]["state"], "DONE")
        self.assertEqual(len(self.lab.effects_for("tenant-one")), 1)

    def test_two_faults_schedule_capped_backoff(self):
        self.submit()
        faults = {("job-one", 1): "timeout", ("job-one", 2): "timeout"}
        self.lab.run_due(0, faults)
        second = self.lab.run_due(2, faults)
        self.assertEqual(second[0]["next_due"], 6)
        self.assertEqual(self.lab.run_due(5), [])
        self.assertEqual(self.lab.run_due(6, faults)[0]["state"], "DONE")

    def test_dead_after_three_failures(self):
        self.submit()
        faults = {("job-one", 1): "down", ("job-one", 2): "down", ("job-one", 3): "down"}
        for now in (0, 2, 6):
            self.lab.run_due(now, faults)
        row = self.lab.jobs_for("tenant-one")[0]
        self.assertEqual(row["status"], "DEAD")
        self.assertEqual(row["attempts"], 3)
        self.assertEqual(row["last_error"], "down")
        self.assertEqual(self.lab.effects_for("tenant-one"), [])
        self.assertEqual(self.lab.run_due(100, faults), [])

    def test_requeue_dead_job_then_finish(self):
        self.submit()
        faults = {("job-one", i): "down" for i in (1, 2, 3)}
        for now in (0, 2, 6):
            self.lab.run_due(now, faults)
        self.lab.requeue_dead("job-one", "tenant-one", 20)
        row = self.lab.jobs_for("tenant-one")[0]
        self.assertEqual((row["status"], row["attempts"], row["next_due"]), ("RETRY", 0, 20))
        self.assertEqual(self.lab.run_due(19), [])
        self.assertEqual(self.lab.run_due(20)[0]["state"], "DONE")
        self.assertIn(("MANUAL_REQUEUE", 0, 20), self.lab.history_for("job-one", "tenant-one"))

    def test_wrong_tenant_cannot_requeue_dead_job(self):
        self.submit()
        faults = {("job-one", i): "down" for i in (1, 2, 3)}
        for now in (0, 2, 6):
            self.lab.run_due(now, faults)
        with self.assertRaises(ValueError):
            self.lab.requeue_dead("job-one", "tenant-other", 20)

    def test_pending_cannot_be_manually_requeued(self):
        self.submit()
        with self.assertRaises(ValueError):
            self.lab.requeue_dead("job-one", "tenant-one", 1)

    def test_completed_cannot_be_manually_requeued(self):
        self.submit()
        self.lab.run_due(0)
        with self.assertRaises(ValueError):
            self.lab.requeue_dead("job-one", "tenant-one", 4)

    def test_second_job_with_same_effect_is_deduplicated(self):
        self.submit()
        self.submit(job="job-two")
        outcome = self.lab.run_due(0)
        self.assertEqual(len(outcome), 2)
        self.assertTrue(any(x.get("deduplicated_effect") for x in outcome))
        self.assertEqual(self.lab.effects_for("tenant-one"), ["effect-one"])
        self.assertEqual(self.lab.jobs_for("tenant-one")[1]["status"], "DONE")

    def test_effect_key_collision_across_tenants_fails(self):
        self.submit(job="job-a", tenant="tenant-a", effect="shared")
        self.lab.run_due(0)
        self.submit(job="job-b", tenant="tenant-b", effect="shared")
        with self.assertRaisesRegex(ValueError, "effect key collision"):
            self.lab.run_due(0)
        self.assertEqual(self.lab.effects_for("tenant-b"), [])
        self.assertEqual(self.lab.jobs_for("tenant-b")[0]["status"], "PENDING")

    def test_effect_key_collision_with_different_payload_fails(self):
        self.submit(job="job-one")
        self.lab.run_due(0)
        self.submit(job="job-two", message="different")
        with self.assertRaisesRegex(ValueError, "effect key collision"):
            self.lab.run_due(0)

    def test_tenant_scoped_views_hide_other_tenant_records(self):
        self.submit()
        self.submit(job="job-two", tenant="tenant-two", effect="effect-two")
        self.lab.run_due(0)
        self.assertEqual(len(self.lab.jobs_for("tenant-one")), 1)
        self.assertEqual(len(self.lab.jobs_for("tenant-two")), 1)
        self.assertEqual(self.lab.effects_for("tenant-one"), ["effect-one"])
        self.assertEqual(self.lab.effects_for("tenant-two"), ["effect-two"])
        self.assertEqual(self.lab.history_for("job-two", "tenant-one"), [])

    def test_limit_only_processes_one_due_job(self):
        self.submit()
        self.submit(job="job-two", tenant="tenant-two", effect="effect-two")
        one = self.lab.run_due(0, limit=1)
        self.assertEqual(len(one), 1)
        self.assertEqual(len(self.lab.run_due(0)), 1)

    def test_audit_history_retains_failures_and_success(self):
        self.submit()
        self.lab.run_due(0, {("job-one", 1): "timeout"})
        self.lab.run_due(2)
        self.assertEqual(
            self.lab.history_for("job-one", "tenant-one"),
            [("SUBMITTED", 0, 0), ("RETRY", 1, 0), ("DONE", 2, 2)],
        )

    def test_demo_timeline_and_final_state(self):
        result = demonstration()
        self.assertTrue(result["synthetic_only"])
        self.assertEqual(result["alpha"][0]["status"], "DONE")
        self.assertEqual(result["alpha"][0]["attempts"], 3)
        self.assertEqual(result["beta"][0]["status"], "DONE")
        self.assertEqual(result["alpha_effects"], ["effect-alpha"])
        self.assertEqual(result["beta_effects"], ["effect-beta"])
        self.assertEqual(result["timeline"][1]["outcomes"], [])
        self.assertEqual(result["timeline"][3]["outcomes"], [])


if __name__ == "__main__":
    unittest.main()
