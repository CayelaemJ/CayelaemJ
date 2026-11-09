"""Data quality checks at the ingestion contract boundary, no dependencies."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation


def check_records(rows: list[dict], *, now: datetime, max_age_hours: int = 48) -> dict:
    """Fail on contract violations without rewriting or silently dropping rows."""
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must include a timezone")
    if max_age_hours < 1:
        raise ValueError("max_age_hours must be positive")
    findings = []
    seen = set()
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            findings.append({"row": index, "rule": "shape", "detail": "Expected object"})
            continue
        if any(key not in row for key in ("id", "amount", "updated_at")):
            findings.append({"row": index, "rule": "schema", "detail": "Missing required column"})
            continue
        ident = row["id"]
        if not isinstance(ident, str) or not ident.strip():
            findings.append({"row": index, "rule": "primary_key", "detail": "Invalid ID"})
        elif ident in seen:
            findings.append({"row": index, "rule": "unique_key", "detail": "Duplicate ID"})
        else:
            seen.add(ident)
        try:
            amount = Decimal(str(row["amount"]))
            if not amount.is_finite() or amount < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError, TypeError):
            findings.append({"row": index, "rule": "amount", "detail": "Non-finite or negative amount"})
        try:
            timestamp = datetime.fromisoformat(str(row["updated_at"]).replace("Z", "+00:00"))
            if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                raise ValueError("Timestamp has no timezone")
            age_hours = (now - timestamp).total_seconds() / 3600
            if age_hours < -0.05:
                findings.append({"row": index, "rule": "future_timestamp", "detail": "Timestamp is ahead of clock"})
            elif age_hours > max_age_hours:
                findings.append({"row": index, "rule": "freshness", "detail": "Timestamp exceeded freshness SLA"})
        except (ValueError, TypeError):
            findings.append({"row": index, "rule": "timestamp", "detail": "Invalid timezone-aware timestamp"})
    return {"status": "PASS" if not findings else "FAIL", "rows_checked": len(rows),
            "finding_count": len(findings), "findings": findings}


if __name__ == "__main__":
    import json
    moment = datetime.now(timezone.utc)
    synthetic = [{"id": "A-001", "amount": "10.50", "updated_at": moment.isoformat()}]
    print(json.dumps(check_records(synthetic, now=moment), indent=2))
