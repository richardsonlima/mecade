#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = {
    ROOT / 'chaos/layer4/dsl/scenario-spec.yaml': 'scenario_id: S4_NET_LATENCY_PROGRESSIVE\nservice_under_test: checkout\nhypothesis_ref: H1\nfault_model:\n  type: network_latency\n  target: checkout->payment\n  profile:\n    - step: 1\n      delay_ms: 150\n      duration_s: 120\n    - step: 2\n      delay_ms: 400\n      duration_s: 120\n    - step: 3\n      delay_ms: 800\n      duration_s: 120\nblast_radius:\n  namespace: shop\n  max_replicas_affected: 1\n',
    ROOT / 'chaos/layer4/safety/preflight-checklist.yaml': 'checks:\n  - id: min_replicas_ready\n    query: "k8s_deployment_ready_replicas{deployment=\'checkout\'} >= 3"\n  - id: budget_available\n    query: "mecade_remaining_error_budget_ratio > 0.20"\n  - id: no_active_incident\n    query: "incident_open_critical == 0"\non_fail: block_experiment\n',
    ROOT / 'chaos/layer4/experiments/fault-library.yaml': 'faults:\n  - id: pod_delete\n    tool: litmus\n    layer: compute\n    expected_effect: short_availability_drop\n  - id: network_latency\n    tool: istio\n    layer: network\n    expected_effect: p99_drift_and_timeout\n  - id: cpu_hog\n    tool: chaos-mesh\n    layer: compute\n    expected_effect: queue_growth\n',
    ROOT / 'chaos/layer4/workflows/progressive-chaos.yaml': 'workflow:\n  id: progressive-chaos-layer4\n  stages:\n    - name: canary\n      scope: 1_pod\n      proceed_if: safety_gate_pass\n    - name: limited_blast\n      scope: 10_percent\n      proceed_if: no_hard_abort\n    - name: controlled_expansion\n      scope: 25_percent\n      proceed_if: effect_within_expected_band\n',
    ROOT / 'chaos/layer4/evaluation/effect-size-criteria.md': '# Critérios de tamanho de efeito\n\n- Delta MTTR >= 15%: efeito operacional relevante.\n- Delta p99 <= 10% apos mitigacao: estabilidade aceitavel.\n- IC95% nao cruza zero para diferenca principal.\n',
    ROOT / 'chaos/layer4/evaluation/ablation-plan.md': '# Plano de ablacao\n\nComparar cenarios:\n1. sem mitigacao\n2. com mitigacao baseline\n3. com mitigacao proposta\n\nObjetivo: atribuir causalidade da melhoria observada.\n',
    ROOT / 'chaos/layer4/validation-protocol.md': '# Validation protocol - Layer 4\n\n1. Preflight deve aprovar todos os checks.\n2. Workflow progressivo deve respeitar gates.\n3. Evidencias devem conter baseline, tratamento e ablacao.\n4. Rollback deve ser confirmado no encerramento.\n',
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured for layer 4. New files created: {created}")


if __name__ == "__main__":
    main()
