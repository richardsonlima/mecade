#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYER1 = ROOT / "planning" / "layer1"
PREREG = LAYER1 / "prereg"
EVIDENCE = LAYER1 / "evidence"


TEMPLATES: dict[Path, str] = {
    LAYER1 / "steady-state.openslo.yaml": """apiVersion: openslo/v1
kind: SLO
metadata:
  name: checkout-steady-state
spec:
  service: checkout
  indicators:
    - name: availability
      ratioMetric:
        counter: http_requests_total{service=\"checkout\",status!~\"5..\"}
        total: http_requests_total{service=\"checkout\"}
    - name: p99_latency
      thresholdMetric: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service=\"checkout\"}[5m])) by (le))
  objectives:
    - displayName: availability_target
      target: 0.995
      timeWindow: 30d
    - displayName: p99_latency_target
      target: 0.300
      operator: lte
      unit: seconds
      timeWindow: 5m
""",
    LAYER1 / "fmea-causal.csv": """failure_mode,cause,pathway,observable_effect,severity,occurrence,detection,rpn,owner
network_latency_800ms,mesh_delay_fault,checkout->payment->timeout,p99_up_and_tsr_down,9,6,4,216,platform
retry_storm,retry_policy_misconfig,checkout->retry_loop,error_rate_up_without_outage,8,5,6,240,sre
pod_kill_payment,node_pressure,payment->failover->recovery,short_unavailability,7,4,3,84,platform
""",
    LAYER1 / "risk-prior.yaml": """risk_prior:
  financial:
    p_critical_failure: 0.12
    impact_weight: 0.9
  aerospace:
    p_critical_failure: 0.08
    impact_weight: 1.0
  infrastructure:
    p_critical_failure: 0.15
    impact_weight: 0.85
""",
    LAYER1 / "chaos-budget-model.yaml": """service: checkout
window: 15m
risk_aware_budget:
  formula: "B = B0 * (1 - impact_weight * p_critical_failure)"
  B0: 15.0
  selected_domain: financial
constraints:
  max_error_rate_delta: 0.015
  max_p99_latency_seconds: 0.450
  max_unavailable_seconds: 60
integral_limit:
  max_accumulated_deviation: 12.0
""",
    LAYER1 / "hypotheses-causal.md": """# H1 - Efeito esperado do mecanismo de bloqueio

Intervencao: ativar controle ALERT/LIMIT/BLOCK durante falha de latencia progressiva.

Hipotese causal:
- O controle reduz MTTR em pelo menos 15% versus baseline reativo.

Metrica primaria:
- MTTR (s)

Metricas secundarias:
- p99 latency, error_rate, TSR

Criterio de sucesso:
- delta_MTTR <= -15% com IC95% excluindo 0.
""",
    LAYER1 / "power-analysis.md": """# Analise de poder amostral

Parametros iniciais:
- Efeito minimo detectavel (MTTR): 15%
- Poder alvo: 0.8
- Alpha: 0.05
- Repeticoes minimas por cenario: calcular com `python python/power_analysis.py`

Interpretacao:
- Sem poder amostral suficiente, os resultados sao apenas demonstrativos.
""",
    PREREG / "experiment-protocol.md": """# Pre-registro do experimento

- Pergunta de pesquisa
- Hipoteses H1..Hn
- Metricas primaria/secundarias
- Cenarios de falha
- Numero de repeticoes
- Regras de exclusao de execucao invalida
- Metodo estatistico
- Criterio de aceite/rejeicao
- Plano de rollback
""",
    LAYER1 / "acceptance-gate.yaml": """must_have:
  - steady_state_formalized
  - fmea_causal_complete
  - risk_prior_defined
  - chaos_budget_risk_aware
  - hypotheses_with_effect_size
  - power_analysis_documented
  - preregistration_done
hard_fail_if:
  - missing_any_must_have
  - no_primary_metric
  - no_statistical_decision_rule
  - no_rollback_plan
""",
}


def main() -> None:
    PREREG.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured. New files created: {created}")


if __name__ == "__main__":
    main()
