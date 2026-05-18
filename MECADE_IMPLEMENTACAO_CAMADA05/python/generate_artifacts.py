#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = {
    ROOT / 'cicd/layer5/release-gate-contract.yaml': 'gate:\n  id: mecade_release_gate_v1\n  required_stages:\n    - build\n    - deploy_staging\n    - chaos_test\n    - slo_validation\n    - risk_scoring\n    - policy_gate\ndecision:\n  mode: multiobjective\n  approve_if:\n    - slo_pass == true\n    - non_regression_pass == true\n    - risk_score <= 0.45\n',
    ROOT / 'cicd/layer5/workflows/resilience-scientific-gate.yml': 'name: resilience-scientific-gate\non:\n  push:\n    branches: ["main"]\njobs:\n  gate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Compute risk score\n        run: python cicd/layer5/evaluation/compute_risk_score.py\n      - name: Policy gate\n        run: conftest test cicd/layer5/policies/input.json --policy cicd/layer5/policies\n',
    ROOT / 'cicd/layer5/policies/release-governance.rego': 'package mecade.layer5\n\ndefault allow = false\n\nallow {\n  input.slo_pass == true\n  input.non_regression_pass == true\n  input.risk_score <= 0.45\n}\n',
    ROOT / 'cicd/layer5/models/risk-score-model.md': '# Risk score model\n\nRiskScore = w1*P(SLO_violation) + w2*P(recovery_delay) + w3*change_complexity + w4*dependency_instability\n\nFaixas:\n- <= 0.30: baixo risco\n- 0.31 a 0.45: risco moderado\n- > 0.45: bloquear release\n',
    ROOT / 'cicd/layer5/evaluation/non-regression-criteria.md': '# Non regression criteria\n\n- p95 latencia nao pode piorar > 5%.\n- erro 5xx nao pode aumentar > 0.3 p.p.\n- MTTR deve manter tendencia nao regressiva.\n',
    ROOT / 'cicd/layer5/evaluation/policy-dryrun-protocol.md': '# Policy dry-run protocol\n\n1. Executar politica em modo observacao por 2 semanas.\n2. Registrar divergencias entre decisao automatica e humana.\n3. Ajustar pesos e limiares antes de enforce.\n',
    ROOT / 'cicd/layer5/validation-protocol.md': '# Validation protocol - Layer 5\n\n1. Validar contrato de gate e workflow.\n2. Validar politica Rego compilavel.\n3. Confirmar criterios de nao regressao e dry-run.\n4. Garantir rastreabilidade de decisao de release.\n',
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured for layer 5. New files created: {created}")


if __name__ == "__main__":
    main()
