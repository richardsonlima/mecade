#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYER2 = ROOT / "planning" / "layer2"
DATA_QUALITY = LAYER2 / "data-quality"
STATS = LAYER2 / "stats"
EVIDENCE = LAYER2 / "evidence"
DASHBOARDS = ROOT / "observability" / "dashboards"


TEMPLATES: dict[Path, str] = {
    LAYER2 / "metric-dictionary.yaml": """service: checkout
metrics:
  - id: availability
    definition: \"Proporcao de requisicoes bem-sucedidas\"
    formula: \"sum(rate(http_requests_total{service=\\\"checkout\\\",status!~\\\"5..\\\"}[5m])) / sum(rate(http_requests_total{service=\\\"checkout\\\"}[5m]))\"
    unit: ratio
    expected_range: [0.0, 1.0]
    sampling_window: 5m
    uncertainty: bootstrap_ci_95
""",
    LAYER2 / "sli-slo-contract.yaml": """version: 1
service: checkout
objectives:
  - id: slo_availability_30d
    sli: availability
    target: 0.995
    window: 30d
    error_budget: 0.005
""",
    LAYER2 / "rrindex-definition.md": """# RRIndex

RRIndex = w1 * (1 - norm_mttr) + w2 * norm_availability + w3 * (1 - norm_p99) + w4 * norm_tsr
""",
    DATA_QUALITY / "gx-suite.yaml": """expectations:
  - expect_column_values_to_not_be_null:
      column: timestamp
""",
    STATS / "decision-rule.md": """# Regra de decisao

- H0: delta_MTTR >= 0
- H1: delta_MTTR < 0
""",
    LAYER2 / "validation-rules.yaml": """experiment: net-latency-800ms
window: 10m
""",
    EVIDENCE / "sample-observations.csv": """cycle,mttr_seconds,availability,p99_latency_seconds,tsr
1,120,0.992,0.420,0.954
2,108,0.993,0.390,0.960
""",
    EVIDENCE / "experiment-mttr.csv": """run_id,baseline_mttr_seconds,mecade_mttr_seconds
1,180,140
2,175,132
""",
    DASHBOARDS / "layer2-scientific-overview.json": """{\"title\": \"MECADE Layer2 Scientific Overview\", \"panels\": []}\n""",
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured. New files created: {created}")


if __name__ == "__main__":
    main()
