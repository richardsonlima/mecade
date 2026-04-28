#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv
import json
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "campaign/config/campaign-plan.yaml"
RANDOMIZATION_PATH = ROOT / "campaign/config/randomizacao_ab.csv"
EVIDENCE_ROOT = ROOT / "evidencias-campanha-viii-c"

REQUIRED_FILES = [
    PLAN_PATH,
    RANDOMIZATION_PATH,
    EVIDENCE_ROOT / "analise/comparativo_ab.csv",
    EVIDENCE_ROOT / "analise/consolidado_final.md",
    EVIDENCE_ROOT / "analise/analysis-summary.json",
]


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def load_plan() -> dict:
    try:
        return yaml.safe_load(PLAN_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid campaign plan YAML: {exc}")


def validate_randomization(plan: dict) -> None:
    rows = list(csv.DictReader(RANDOMIZATION_PATH.open(encoding="utf-8")))
    if not rows:
        fail("randomizacao_ab.csv is empty")

    expected = int(plan["minimum_repetitions_per_scenario"])
    scenarios = set(plan["scenarios"])

    grouped: dict[str, list[str]] = {s: [] for s in scenarios}
    for row in rows:
        cenario = row.get("cenario", "")
        ordem = row.get("ordem", "")
        if cenario not in scenarios:
            fail(f"Unexpected scenario in randomization: {cenario}")
        if ordem not in {"A-B", "B-A"}:
            fail(f"Invalid randomization order: {ordem}")
        grouped[cenario].append(ordem)

    for scenario, orders in grouped.items():
        if len(orders) < expected:
            fail(f"Scenario {scenario} has fewer than {expected} repetitions")
        if len(set(orders)) < 2:
            fail(f"Scenario {scenario} does not alternate A/B order")


def validate_comparative_table(plan: dict) -> None:
    table = EVIDENCE_ROOT / "analise/comparativo_ab.csv"
    rows = list(csv.DictReader(table.open(encoding="utf-8")))
    if not rows:
        fail("comparativo_ab.csv has no rows")

    required_cols = {
        "cenario",
        "repeticao",
        "ordem",
        "mttr_baseline",
        "mttr_mecade",
        "rto_baseline",
        "rto_mecade",
        "p95_baseline",
        "p95_mecade",
        "p99_baseline",
        "p99_mecade",
        "tsr_baseline",
        "tsr_mecade",
        "false_block_rate_mecade",
    }
    missing = required_cols.difference(rows[0].keys())
    if missing:
        fail(f"comparativo_ab.csv missing required columns: {sorted(missing)}")

    scenarios = set(plan["scenarios"])
    counts = {s: 0 for s in scenarios}
    for row in rows:
        scenario = row["cenario"]
        if scenario not in scenarios:
            fail(f"Unexpected scenario in comparativo_ab.csv: {scenario}")
        counts[scenario] += 1
        try:
            float(row["false_block_rate_mecade"])
            float(row["mttr_baseline"])
            float(row["mttr_mecade"])
            float(row["rto_baseline"])
            float(row["rto_mecade"])
            float(row["p95_baseline"])
            float(row["p95_mecade"])
            float(row["p99_baseline"])
            float(row["p99_mecade"])
            float(row["tsr_baseline"])
            float(row["tsr_mecade"])
        except ValueError as exc:
            fail(f"Invalid numeric value in comparativo_ab.csv: {exc}")

    minimum = int(plan["minimum_repetitions_per_scenario"])
    for scenario, total in counts.items():
        if total < minimum:
            fail(f"Scenario {scenario} has {total} rows; minimum is {minimum}")


def validate_runs_have_audit_trace() -> None:
    run_dirs = sorted((EVIDENCE_ROOT / "execucoes").glob("run-*"))
    if not run_dirs:
        fail("No run-* directories found in execucoes")

    required = ["metadata.json", "workload.json", "eventos-alert-limit-block.jsonl", "metricas-series.csv", "resumo.md"]
    for run_dir in run_dirs:
        for name in required:
            if not (run_dir / name).exists():
                fail(f"Missing {name} in {run_dir}")


def validate_analysis_summary() -> None:
    summary_path = EVIDENCE_ROOT / "analise/analysis-summary.json"
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid analysis-summary.json: {exc}")

    for key in [
        "campaign",
        "runs_analyzed",
        "mean_delta_mttr_seconds",
        "mean_delta_rto_seconds",
        "mean_delta_p99_ms",
        "mean_false_block_rate_mecade",
    ]:
        if key not in summary:
            fail(f"analysis-summary.json missing key: {key}")


def main() -> None:
    for f in REQUIRED_FILES:
        if not f.exists():
            fail(f"Missing required file: {f}")

    plan = load_plan()
    validate_randomization(plan)
    validate_comparative_table(plan)
    validate_runs_have_audit_trace()
    validate_analysis_summary()

    print("[OK] Campanha VIII-C Tier A1 validada e pronta.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[FAIL] Unexpected error: {exc}")
        sys.exit(1)
