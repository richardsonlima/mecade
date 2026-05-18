#!/usr/bin/env python3
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import csv
import json
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "evidencias-campanha-viii-c/analise"
COMPARATIVE_CSV = ANALYSIS_DIR / "comparativo_ab.csv"


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def main() -> None:
    if not COMPARATIVE_CSV.exists():
        raise SystemExit(f"Missing comparative table: {COMPARATIVE_CSV}")

    rows = list(csv.DictReader(COMPARATIVE_CSV.open(encoding="utf-8")))
    if not rows:
        raise SystemExit("comparativo_ab.csv has no data rows")

    deltas_mttr = [as_float(r, "mttr_baseline") - as_float(r, "mttr_mecade") for r in rows]
    deltas_rto = [as_float(r, "rto_baseline") - as_float(r, "rto_mecade") for r in rows]
    deltas_p99 = [as_float(r, "p99_baseline") - as_float(r, "p99_mecade") for r in rows]
    tsr_deltas = [as_float(r, "tsr_mecade") - as_float(r, "tsr_baseline") for r in rows]
    false_block = [as_float(r, "false_block_rate_mecade") for r in rows]

    summary = {
        "campaign": "VIII-C-A1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "runs_analyzed": len(rows),
        "mean_delta_mttr_seconds": round(mean(deltas_mttr), 3),
        "mean_delta_rto_seconds": round(mean(deltas_rto), 3),
        "mean_delta_p99_ms": round(mean(deltas_p99), 3),
        "mean_delta_tsr": round(mean(tsr_deltas), 6),
        "mean_false_block_rate_mecade": round(mean(false_block), 6),
        "favorable_for_a1": mean(deltas_mttr) > 0
        and mean(deltas_rto) > 0
        and mean(deltas_p99) > 0
        and mean(false_block) < 0.10,
    }

    (ANALYSIS_DIR / "analysis-summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    markdown = [
        "# Consolidado final da campanha VIII-C",
        "",
        f"- Runs analisados: {summary['runs_analyzed']}",
        f"- Delta medio MTTR (Baseline - MECADE): {summary['mean_delta_mttr_seconds']} s",
        f"- Delta medio RTO (Baseline - MECADE): {summary['mean_delta_rto_seconds']} s",
        f"- Delta medio P99 (Baseline - MECADE): {summary['mean_delta_p99_ms']} ms",
        f"- Delta medio TSR (MECADE - Baseline): {summary['mean_delta_tsr']}",
        f"- Taxa media de falsos bloqueios (MECADE): {summary['mean_false_block_rate_mecade']}",
        f"- Evidencia favoravel Tier A1: {'sim' if summary['favorable_for_a1'] else 'nao'}",
        "",
        "## Observacao",
        "",
        "Este consolidado e derivado do arquivo comparativo_ab.csv. Atualize as linhas com dados reais da campanha em Kubernetes para conclusao final de submissao.",
    ]
    (ANALYSIS_DIR / "consolidado_final.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")

    print(f"Campaign analysis summary written to {ANALYSIS_DIR / 'analysis-summary.json'}")


if __name__ == "__main__":
    main()
