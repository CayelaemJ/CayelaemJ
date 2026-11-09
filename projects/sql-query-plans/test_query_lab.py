import unittest

from query_lab import (
    AGGREGATE_SQL, NON_SARGABLE_SQL, build_synthetic_store,
    create_composite_index, demonstrate, plan, result,
)


class QueryPlanTests(unittest.TestCase):
    def setUp(self):
        self.db = build_synthetic_store()
        self.params = ("tenant-02", "POSTED", "2026-02-01", "2026-03-01")

    def tearDown(self):
        self.db.close()

    def test_without_index_scans(self):
        self.assertTrue(any("SCAN orders" in line for line in plan(self.db, AGGREGATE_SQL, self.params)))

    def test_composite_index_gives_range_search(self):
        create_composite_index(self.db)
        details = " ".join(plan(self.db, AGGREGATE_SQL, self.params))
        self.assertIn("USING INDEX idx_orders_tenant_status_date", details)
        self.assertIn("created_on>?", details)

    def test_index_does_not_change_aggregation(self):
        before = result(self.db, AGGREGATE_SQL, self.params)
        create_composite_index(self.db)
        after = result(self.db, AGGREGATE_SQL, self.params)
        self.assertEqual(before, after)
        self.assertGreater(after[0], 0)
        self.assertGreater(after[1], 0)

    def test_date_function_prevents_date_range_search(self):
        create_composite_index(self.db)
        details = " ".join(plan(self.db, NON_SARGABLE_SQL, self.params[:2] + ("2026-02",)))
        self.assertNotIn("created_on>?", details)
        self.assertEqual(result(self.db, AGGREGATE_SQL, self.params),
                         result(self.db, NON_SARGABLE_SQL, self.params[:2] + ("2026-02",)))

    def test_rejects_invalid_inputs_and_writes(self):
        with self.assertRaises(ValueError):
            build_synthetic_store(0)
        with self.assertRaises(ValueError):
            plan(self.db, "DELETE FROM orders", ())

    def test_cli_demonstration(self):
        example = demonstrate()
        self.assertEqual(example["row_count"], 2400)
        self.assertGreater(example["result"]["orders"], 0)
        self.assertIn("without_index", example)


if __name__ == "__main__":
    unittest.main()
