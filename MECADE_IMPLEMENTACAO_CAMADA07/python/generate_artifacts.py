#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = {
    ROOT / 'improvement/layer7/contracts/learning-loop-contract.yaml': 'cadence: weekly\ninputs:\n  - layer3_detection_quality\n  - layer4_experiment_results\n  - layer5_release_decisions\n  - layer6_audit_proofs\noutputs:\n  - candidate_policy_version\n  - causal_effect_report\n  - promote_or_rollback_decision\nprimary_objective:\n  minimize: mttr_seconds\nconstraints:\n  - false_block_rate_lte: 0.10\n  - missed_gray_failure_rate_lte: 0.08\n  - safety_limit_violations_eq: 0\n',
    ROOT / 'improvement/layer7/models/policy-search-space.yaml': 'policy_parameters:\n  alert_threshold:\n    min: 0.10\n    max: 0.35\n  limit_threshold:\n    min: 0.25\n    max: 0.60\n  accumulated_deviation_budget:\n    min: 4\n    max: 15\n  block_risk_cutoff:\n    min: 0.70\n    max: 0.95\nmethod:\n  optimizer: bayesian_optimization\n  max_trials_per_cycle: 25\n  objective: min_mttr_subject_to_safety_constraints\n',
    ROOT / 'improvement/layer7/models/causal-evaluation-plan.md': '# Causal evaluation plan\n\nPergunta:\n- Qual o efeito causal da policy_version_k sobre MTTR e taxa de bloqueio falso?\n\nEstrategia:\n- Diferenca-em-diferencas com grupo de controle comparavel.\n- Ajuste por carga e sazonalidade.\n\nSaidas:\n- ATT para MTTR.\n- IC95% do efeito.\n- Analise de sensibilidade.\n',
    ROOT / 'improvement/layer7/workflows/continuous-policy-learning.yaml': 'workflow:\n  id: continuous-policy-learning\n  cadence: weekly\n  steps:\n    - ingest_layer_metrics\n    - run_policy_search\n    - causal_evaluation\n    - safety_gate\n    - promote_or_rollback\n',
    ROOT / 'improvement/layer7/evaluation/upgrade-gate.yaml': 'upgrade_gate:\n  approve_if:\n    - mttr_improvement_ratio >= 0.10\n    - false_block_rate <= 0.10\n    - safety_limit_violations == 0\n    - causal_confidence >= 0.95\n',
    ROOT / 'improvement/layer7/evaluation/regression-guardrails.yaml': 'guardrails:\n  - metric: p99_latency_seconds\n    max_relative_regression: 0.05\n  - metric: error_rate\n    max_absolute_regression: 0.003\n  - metric: audit_integrity_failures\n    allowed: 0\n',
    ROOT / 'improvement/layer7/reports/cycle-review-template.md': '# Template de revisao de ciclo\n\n## Hipotese\n\n## Mudanca de politica candidata\n\n## Resultado causal (ATT + IC95)\n\n## Decisao (promover/rollback)\n\n## Riscos residuais e acoes\n',
    ROOT / 'improvement/layer7/validation-protocol.md': '# Validation protocol - Layer 7\n\n1. Validar contrato do loop e espaco de busca.\n2. Validar workflow continuo e gates de upgrade.\n3. Garantir guardrails de regressao ativos.\n4. Exigir relatorio de ciclo com decisao auditavel.\n',
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured for layer 7. New files created: {created}")


if __name__ == "__main__":
    main()
