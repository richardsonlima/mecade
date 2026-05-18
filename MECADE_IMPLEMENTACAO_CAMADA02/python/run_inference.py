#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "planning" / "layer2" / "evidence"
INPUT = EVIDENCE / "experiment-mttr.csv"
OUTPUT = EVIDENCE / "inference-summary.json"


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Missing input file: {INPUT}")

    baseline: list[float] = []
    mecade: list[float] = []

    with INPUT.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            baseline.append(float(row["baseline_mttr_seconds"]))
            mecade.append(float(row["mecade_mttr_seconds"]))

    if len(baseline) < 3:
        raise SystemExit("At least 3 runs are required for inference.")

    deltas = [m - b for b, m in zip(baseline, mecade)]
    mean_delta = statistics.fmean(deltas)
    sd_delta = statistics.stdev(deltas)
    n = len(deltas)
    se = sd_delta / math.sqrt(n)
    z95 = 1.96
    ci_low = mean_delta - z95 * se
    ci_high = mean_delta + z95 * se

    baseline_mean = statistics.fmean(baseline)
    effect_percent = (-mean_delta / baseline_mean) * 100.0

    ci95_below_zero = ci_high < 0
    effect_pass = effect_percent >= 10.0
    approved = ci95_below_zero and effect_pass

    payload = {
        "n_runs": n,
        "mean_delta_mttr_seconds": round(mean_delta, 4),
        "ci95": [round(ci_low, 4), round(ci_high, 4)],
        "effect_percent": round(effect_percent, 4),
        "decision": {
            "ci95_below_zero": ci95_below_zero,
            "effect_ge_10_percent": effect_pass,
            "approved": approved,
        },
    }

    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
