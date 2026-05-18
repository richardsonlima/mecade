#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = {
    ROOT / 'planning/layer3/detection-contract.yaml': 'service: checkout\nsteady_state:\n  p99_latency_seconds: 0.300\n  error_rate: 0.010\nhard_safety_limits:\n  max_p99_latency_seconds: 0.600\n  max_error_rate: 0.030\nadaptive_zone:\n  alert_relative_deviation: 0.20\n  limit_relative_deviation: 0.40\nwindows:\n  instant: 60s\n  accumulated: 10m\nrequired_evidence:\n  - metric_signal\n  - trace_or_log_corroboration\n',
    ROOT / 'planning/layer3/models/risk-posterior-model.md': '# Modelo de risco posterior (Camada 3)\n\nPosteriorRisk = P(falha_critica | sinais) * ImpactoDominio\n\nRegra:\n- ALERT quando PosteriorRisk >= 0.30\n- LIMIT quando PosteriorRisk >= 0.55\n- BLOCK quando PosteriorRisk >= 0.80 ou hard_safety_limits violados\n',
    ROOT / 'observability/rules/alert-limit-block.rules.yaml': 'groups:\n  - name: mecade-layer3-scientific\n    interval: 15s\n    rules:\n      - record: mecade:checkout:p99\n        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="checkout"}[1m])) by (le))\n\n      - record: mecade:checkout:error_rate\n        expr: sum(rate(http_requests_total{service="checkout",status=~"5.."}[1m])) / sum(rate(http_requests_total{service="checkout"}[1m]))\n\n      - record: mecade:checkout:relative_deviation\n        expr: (mecade:checkout:p99 - 0.300) / 0.300\n\n      - record: mecade:checkout:accum_dev_10m\n        expr: sum_over_time(clamp_min(mecade:checkout:relative_deviation, 0)[10m:15s])\n\n      - alert: MECADEAlert\n        expr: mecade:checkout:relative_deviation > 0.20\n        for: 1m\n        labels:\n          severity: warning\n          mecade_axiom: ALERT\n\n      - alert: MECADELimit\n        expr: mecade:checkout:relative_deviation > 0.40 or mecade:checkout:accum_dev_10m > 8\n        for: 30s\n        labels:\n          severity: critical\n          mecade_axiom: LIMIT\n\n      - alert: MECADEBlockHardSafety\n        expr: mecade:checkout:p99 > 0.600 or mecade:checkout:error_rate > 0.030\n        for: 15s\n        labels:\n          severity: critical\n          mecade_axiom: BLOCK\n',
    ROOT / 'observability/patterns/gray-failure-cep.yaml': 'pattern_id: gray_failure_latency_drift\nwindow: 12m\nconditions:\n  - metric: p99_latency\n    trend: increasing\n    min_slope_per_minute: 0.01\n  - metric: error_rate\n    op: lte\n    value: 0.01\n  - metric: retry_rate\n    op: gte\n    value: 0.12\ndecision:\n  emit_event: GRAY_FAILURE_SUSPECTED\n  confidence_min: 0.8\n',
    ROOT / 'planning/layer3/false-positive-negative-tracker.md': '# Tracker de falsos positivos/negativos e latencia de decisao\n\nRegistre por ciclo experimental:\n\n1. Precision e recall para eventos criticos.\n2. Taxa de falso positivo ALERT/LIMIT.\n3. Taxa de falso negativo em gray failure.\n4. Lead-time-to-failure (tempo entre ALERT e violacao LIMIT/BLOCK).\n5. Tempo de decisao (detectar -> acionar BLOCK).\n\n| ciclo | precision | recall | fp_alert_limit | fn_gray_failure | lead_time_s | decision_latency_ms |\n|------:|----------:|-------:|---------------:|----------------:|------------:|--------------------:|\n| 1     | 0.90      | 0.83   | 0.09           | 0.17            | 75          | 980                 |\n',
    ROOT / 'automation/block/block-decision-policy.yaml': 'block_policy:\n  trigger_any:\n    - alert_name: MECADEBlockHardSafety\n    - posterior_risk_gte: 0.80\n  require_evidence:\n    - metric_signal\n    - trace_or_log_corroboration\n  actions:\n    - stop_fault_injection: true\n    - apply_safe_state_runbook: true\n  max_decision_latency_ms: 1500\n  audit_required: true\n',
    ROOT / 'planning/layer3/validation-protocol.md': '# Protocolo de Validacao - Camada 3\n\nCenario A - Drift progressivo sem outage:\n- aumentar latencia em degraus a cada 2 minutos\n- validar deteccao de gray failure antes de 5xx massivo\n\nCenario B - Ruido sem falha real:\n- injetar variabilidade controlada de curta duracao\n- validar que LIMIT/BLOCK nao disparam indevidamente\n\nCenario C - Hard safety:\n- violar limite duro de p99/error_rate\n- validar BLOCK em tempo alvo e transicao para estado seguro\n\nCenario D - Ablacao de sinais:\n- remover log/trace e repetir cenario\n- medir degradacao da qualidade de decisao do comite\n',
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured for layer 3. New files created: {created}")


if __name__ == "__main__":
    main()
