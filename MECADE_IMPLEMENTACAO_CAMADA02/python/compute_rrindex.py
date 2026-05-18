#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "planning" / "layer2" / "evidence"
INPUT = EVIDENCE / "sample-observations.csv"
OUTPUT = EVIDENCE / "rrindex-summary.json"
TIMESERIES = EVIDENCE / "rrindex-timeseries.csv"


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Missing input file: {INPUT}")

    rows: list[dict[str, float]] = []
    with INPUT.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            rows.append(
                {
                    "cycle": float(raw["cycle"]),
                    "mttr": float(raw["mttr_seconds"]),
                    "availability": float(raw["availability"]),
                    "p99": float(raw["p99_latency_seconds"]),
                    "tsr": float(raw["tsr"]),
                }
            )

    if not rows:
        raise SystemExit("No data rows in sample-observations.csv")

    mttr_min = min(r["mttr"] for r in rows)
    mttr_max = max(r["mttr"] for r in rows)
    p99_min = min(r["p99"] for r in rows)
    p99_max = max(r["p99"] for r in rows)

    weights = {"w1": 0.35, "w2": 0.25, "w3": 0.25, "w4": 0.15}
    rr_rows: list[tuple[int, float]] = []

    for r in rows:
        mttr_den = max(mttr_max - mttr_min, 1e-9)
        p99_den = max(p99_max - p99_min, 1e-9)

        norm_mttr = clamp01((r["mttr"] - mttr_min) / mttr_den)
        norm_availability = clamp01(r["availability"])
        norm_p99 = clamp01((r["p99"] - p99_min) / p99_den)
        norm_tsr = clamp01(r["tsr"])

        rrindex = (
            weights["w1"] * (1 - norm_mttr)
            + weights["w2"] * norm_availability
            + weights["w3"] * (1 - norm_p99)
            + weights["w4"] * norm_tsr
        )
        rr_rows.append((int(r["cycle"]), round(rrindex, 6)))

    with TIMESERIES.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cycle", "rrindex"])
        writer.writerows(rr_rows)

    rr_values = [v for _, v in rr_rows]
    payload = {
        "weights": weights,
        "rrindex_min": min(rr_values),
        "rrindex_max": max(rr_values),
        "rrindex_last": rr_values[-1],
        "rrindex_improvement": rr_values[-1] - rr_values[0],
        "timeseries_file": str(TIMESERIES),
    }

    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"Saved: {OUTPUT}")
    print(f"Saved: {TIMESERIES}")


if __name__ == "__main__":
    main()
