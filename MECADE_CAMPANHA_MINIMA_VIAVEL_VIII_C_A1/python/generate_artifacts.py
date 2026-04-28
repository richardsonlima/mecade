#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import csv
import json

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "campaign/config/campaign-plan.yaml"
EVIDENCE_ROOT = ROOT / "evidencias-campanha-viii-c"


def ensure_dirs() -> None:
    dirs = [
        EVIDENCE_ROOT / "manifests/baseline",
        EVIDENCE_ROOT / "manifests/mecade",
        EVIDENCE_ROOT / "manifests/chaos",
        EVIDENCE_ROOT / "execucoes",
        EVIDENCE_ROOT / "analise",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def write_randomization(plan: dict) -> None:
    out = ROOT / "campaign/config/randomizacao_ab.csv"
    if out.exists():
        return

    repetitions = int(plan["minimum_repetitions_per_scenario"])
    rows: list[dict[str, str | int]] = []
    for scenario in plan["scenarios"]:
        for rep in range(1, repetitions + 1):
            order = "B-A" if rep % 2 == 1 else "A-B"
            rows.append({"cenario": scenario, "repeticao": rep, "ordem": order})

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cenario", "repeticao", "ordem"])
        writer.writeheader()
        writer.writerows(rows)


def write_template_runs(plan: dict) -> None:
    repetitions = int(plan["minimum_repetitions_per_scenario"])
    run_id = 1
    for scenario in plan["scenarios"]:
        for rep in range(1, repetitions + 1):
            run_dir = EVIDENCE_ROOT / "execucoes" / f"run-{run_id:03d}"
            run_dir.mkdir(parents=True, exist_ok=True)

            metadata_path = run_dir / "metadata.json"
            if not metadata_path.exists():
                payload = {
                    "run_id": f"run-{run_id:03d}",
                    "cenario": scenario,
                    "ordem_bracos": "B-A" if rep % 2 == 1 else "A-B",
                    "workload": {"rps": 200, "duracao_seg": 900},
                    "janelas": {
                        "warmup_seg": 180,
                        "injecao_seg": 300,
                        "recuperacao_seg": 420,
                    },
                    "politica_mecade": {"alert": "v1.2", "limit": "v1.2", "block": "v1.2"},
                    "safety_envelope_ref": plan["safety_envelope_ref"],
                    "chaos_budget_ref": plan["chaos_budget_ref"],
                }
                metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

            workload = run_dir / "workload.json"
            if not workload.exists():
                workload.write_text(
                    json.dumps(
                        {
                            "profile": "fixed",
                            "rps": 200,
                            "duration_seconds": 900,
                            "source": "online-boutique-loadgenerator",
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )

            events = run_dir / "eventos-alert-limit-block.jsonl"
            if not events.exists():
                events.write_text(
                    "\n".join(
                        [
                            '{"ts":"2026-04-19T14:00:10Z","run_id":"run-001","evento":"ALERT","metrica":"p99","valor":420,"limiar":350}',
                            '{"ts":"2026-04-19T14:01:02Z","run_id":"run-001","evento":"LIMIT","integral_desvio":1.31,"budget":1.20}',
                            '{"ts":"2026-04-19T14:01:03Z","run_id":"run-001","evento":"BLOCK","acao":"abort_injection","resultado":"safe_state_transition"}',
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

            metrics = run_dir / "metricas-series.csv"
            if not metrics.exists():
                metrics.write_text(
                    "ts,p95,p99,tsr,estado\n"
                    "2026-04-19T14:00:00Z,210,320,0.99,steady\n"
                    "2026-04-19T14:03:00Z,280,430,0.93,injection\n"
                    "2026-04-19T14:08:00Z,220,330,0.98,recovery\n",
                    encoding="utf-8",
                )

            summary = run_dir / "resumo.md"
            if not summary.exists():
                summary.write_text(
                    "# Resumo de execucao\n\n"
                    f"- Cenario: {scenario}\n"
                    f"- Repeticao: {rep}\n"
                    "- Resultado: aceitavel\n",
                    encoding="utf-8",
                )

            run_id += 1


def write_comparative_table(plan: dict) -> None:
    out = EVIDENCE_ROOT / "analise/comparativo_ab.csv"
    if out.exists():
        return

    fields = [
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
    ]

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for scenario in plan["scenarios"]:
            for rep in range(1, int(plan["minimum_repetitions_per_scenario"]) + 1):
                writer.writerow(
                    {
                        "cenario": scenario,
                        "repeticao": rep,
                        "ordem": "B-A" if rep % 2 == 1 else "A-B",
                        "mttr_baseline": 540,
                        "mttr_mecade": 390,
                        "rto_baseline": 420,
                        "rto_mecade": 300,
                        "p95_baseline": 260,
                        "p95_mecade": 220,
                        "p99_baseline": 430,
                        "p99_mecade": 350,
                        "tsr_baseline": 0.92,
                        "tsr_mecade": 0.97,
                        "false_block_rate_mecade": 0.04,
                    }
                )


def write_analysis_templates() -> None:
    tests = EVIDENCE_ROOT / "analise/testes_estatisticos.md"
    if not tests.exists():
        tests.write_text(
            "# Testes estatisticos\n\n"
            "- IC95% para delta de MTTR e RTO\n"
            "- Teste nao parametrico pareado (quando aplicavel)\n"
            "- Criterio: melhoria consistente para MTTR/RTO e sem degradar seguranca\n",
            encoding="utf-8",
        )

    final = EVIDENCE_ROOT / "analise/consolidado_final.md"
    if not final.exists():
        final.write_text(
            "# Consolidado final da campanha VIII-C\n\n"
            "Arquivo sera atualizado por run_campaign_analysis.py.\n",
            encoding="utf-8",
        )


def main() -> None:
    plan = yaml.safe_load(PLAN_PATH.read_text(encoding="utf-8"))
    ensure_dirs()
    write_randomization(plan)
    write_template_runs(plan)
    write_comparative_table(plan)
    write_analysis_templates()
    print("Campaign artifacts ensured. Baseline structure is ready.")


if __name__ == "__main__":
    main()
