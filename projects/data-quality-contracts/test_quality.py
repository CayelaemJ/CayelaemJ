import unittest
from datetime import datetime, timedelta, timezone

from quality import check_records


class DataQualityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 9, 9, tzinfo=timezone.utc)

    def row(self, **changes):
        return {**{"id": "row-1", "amount": "10.20", "updated_at": self.now.isoformat()}, **changes}

    def test_clean_contract_passes(self):
        self.assertEqual(check_records([self.row()], now=self.now)["status"], "PASS")

    def test_duplicate_and_missing_column(self):
        result = check_records([self.row(), self.row(), {"id": "bad"}], now=self.now)
        self.assertEqual({f["rule"] for f in result["findings"]}, {"unique_key", "schema"})

    def test_decimal_and_timestamp_safety(self):
        result = check_records([
            self.row(amount="NaN"),
            self.row(id="row-2", updated_at="2026-11-01T09:00:00Z"),
            self.row(id="row-3", updated_at="2026-11-09 09:00:00"),
        ], now=self.now)
        self.assertEqual({f["rule"] for f in result["findings"]}, {"amount", "freshness", "timestamp"})

    def test_future_time_and_empty_id(self):
        result = check_records([self.row(id=" ", updated_at=(self.now + timedelta(hours=1)).isoformat())], now=self.now)
        self.assertEqual({f["rule"] for f in result["findings"]}, {"primary_key", "future_timestamp"})

    def test_naive_now_refused(self):
        with self.assertRaises(ValueError):
            check_records([self.row()], now=datetime(2026, 11, 9))


if __name__ == "__main__":
    unittest.main()
