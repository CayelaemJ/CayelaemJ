"""Run the synthetic data-to-decision pipeline or demonstrate fail-closed recovery."""
import argparse
from dataclasses import replace
import json
import sqlite3

from engine import Pipeline, sample_events


def demonstrate() -> dict:
    with Pipeline() as pipeline:
        baseline = pipeline.apply_batch(sample_events())
        duplicate = pipeline.apply_batch(sample_events())
        return {
            "dataset": "fictional-only",
            "bronze_event_count": len(pipeline.events()),
            "first_batch": baseline,
            "replay_batch": duplicate,
            "alpha_gold": pipeline.metrics_for("fictional-alpha"),
            "beta_gold": pipeline.metrics_for("fictional-beta"),
            "reconciled": pipeline.reconciles(),
        }


def failure_demonstration() -> dict:
    with Pipeline() as pipeline:
        pipeline.apply_batch(sample_events())
        before = pipeline.snapshot()
        valid = replace(sample_events()[0], event_id="evt-09", position=9, version=3)
        invalid = replace(sample_events()[1], event_id="evt-10", position=10, version=3, amount_cents=-10)
        failure = None
        try:
            pipeline.apply_batch((valid, invalid))
        except (ValueError, sqlite3.IntegrityError) as exc:
            failure = str(exc)
        return {
            "dataset": "fictional-only",
            "error": failure,
            "all_or_nothing": before == pipeline.snapshot(),
            "event_log_unchanged": len(pipeline.events()) == 8,
            "reconciled": pipeline.reconciles(),
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline synthetic data-to-decision platform")
    parser.add_argument("mode", nargs="?", choices=("demo", "failure"), default="demo")
    args = parser.parse_args()
    print(json.dumps(demonstrate() if args.mode == "demo" else failure_demonstration(), indent=2))
