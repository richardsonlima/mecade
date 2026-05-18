# HOWTO: Camada 7 (Aprendizado Causal Contínuo e Evolucao de Politicas) do MECADE

Eu escrevi este guia como passo a passo E2E para implementar, testar e validar tecnicamente a evolucao de politicas na Camada 7.

Stack open source recomendada:

- Argo Workflows (orquestracao periódica do loop)
- PostgreSQL + DuckDB (base historica e analise)
- MLflow (rastreio de versoes, parametros e resultados)
- DVC (versionamento de datasets e artefatos)
- Evidently + Great Expectations (drift e qualidade de dados)
- DoWhy/EconML (inferencia causal para efeito de politica)
- Grafana + Prometheus (acompanhamento de maturidade)

## 1. O que torna esta Camada 7 inovadora

A inovação não é apenas "medir e ajustar". É evoluir controle com evidência causal:

1. Loop fechado com hipótese de melhoria explicitada por ciclo.
2. Atualização de ALERT/LIMIT/BLOCK por otimização sob restrições de segurança.
3. Avaliação causal de intervenção (efeito real da nova política).
4. Guardrails contra regressão e overfitting operacional.
5. Promoção de política como release científico (com aprovação e rollback).

## 2. Entregas obrigatorias da Camada 7

```bash
mkdir -p improvement/layer7
mkdir -p improvement/layer7/contracts
mkdir -p improvement/layer7/workflows
mkdir -p improvement/layer7/models
mkdir -p improvement/layer7/evaluation
mkdir -p improvement/layer7/reports
```

Arquivos obrigatorios:

- improvement/layer7/contracts/learning-loop-contract.yaml
- improvement/layer7/models/policy-search-space.yaml
- improvement/layer7/models/causal-evaluation-plan.md
- improvement/layer7/workflows/continuous-policy-learning.yaml
- improvement/layer7/evaluation/upgrade-gate.yaml
- improvement/layer7/evaluation/regression-guardrails.yaml
- improvement/layer7/reports/cycle-review-template.md
- improvement/layer7/validation-protocol.md

Sem esses artefatos, a camada nao sustenta alegação de maturidade evolutiva.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Contrato formal do loop de aprendizado

Exemplo em improvement/layer7/contracts/learning-loop-contract.yaml:

```yaml
cadence: weekly
inputs:
  - layer3_detection_quality
  - layer4_experiment_results
  - layer5_release_decisions
  - layer6_audit_proofs
outputs:
  - candidate_policy_version
  - causal_effect_report
  - promote_or_rollback_decision
primary_objective:
  minimize: mttr_seconds
constraints:
  - false_block_rate_lte: 0.10
  - missed_gray_failure_rate_lte: 0.08
  - safety_limit_violations_eq: 0
```

Diferencial: deixa explícito objetivo, restrições e produtos do ciclo.

### Passo 3.2 - Definir espaço de busca da politica

Exemplo em improvement/layer7/models/policy-search-space.yaml:

```yaml
policy_parameters:
  alert_threshold:
    min: 0.10
    max: 0.35
  limit_threshold:
    min: 0.25
    max: 0.60
  accumulated_deviation_budget:
    min: 4
    max: 15
  block_risk_cutoff:
    min: 0.70
    max: 0.95
method:
  optimizer: bayesian_optimization
  max_trials_per_cycle: 25
  objective: "min_mttr_subject_to_safety_constraints"
```

Diferencial: tuning deixa de ser heurístico e vira otimização formal.

### Passo 3.3 - Planejar avaliação causal da mudança

Em improvement/layer7/models/causal-evaluation-plan.md:

```md
Pergunta:
- Qual o efeito causal da policy_version_k sobre MTTR e taxa de bloqueio falso?

Estratégia:
- Diferença-em-diferenças entre grupos comparáveis (antes/depois + controle).
- Ajuste por covariáveis de carga e sazonalidade.

Saídas:
- ATT estimado para MTTR.
- IC95% do efeito.
- Robustez em analises de sensibilidade.
```

Diferencial: separa ganho real de ruído operacional.

### Passo 3.4 - Orquestrar ciclo de aprendizado como workflow

Exemplo em improvement/layer7/workflows/continuous-policy-learning.yaml:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: mecade-policy-learning
  namespace: argo
spec:
  schedule: "0 3 * * 1"
  workflowSpec:
    entrypoint: loop
    templates:
      - name: loop
        steps:
          - - name: ingest-data
              template: run
              arguments:
                parameters:
                  - name: cmd
                    value: "python jobs/ingest_cycle_data.py"
          - - name: optimize-policy
              template: run
              arguments:
                parameters:
                  - name: cmd
                    value: "python jobs/optimize_policy.py"
          - - name: causal-eval
              template: run
              arguments:
                parameters:
                  - name: cmd
                    value: "python jobs/causal_eval.py"
          - - name: gate-upgrade
              template: run
              arguments:
                parameters:
                  - name: cmd
                    value: "python jobs/upgrade_gate.py"

      - name: run
        inputs:
          parameters:
            - name: cmd
        container:
          image: python:3.12-slim
          command: ["sh", "-c"]
          args: ["{{inputs.parameters.cmd}}"]
```

### Passo 3.5 - Definir gate de promoção de política

Exemplo em improvement/layer7/evaluation/upgrade-gate.yaml:

```yaml
promote_if:
  - att_mttr_reduction_percent_gte: 10
  - att_mttr_ci95_excludes_zero: true
  - false_block_rate_delta_lte: 0.02
  - missed_gray_failure_rate_not_worse: true
  - safety_violations_eq: 0
otherwise:
  action: rollback_to_previous_policy
```

Diferencial: política só promove com ganho causal + segurança.

### Passo 3.6 - Guardrails contra regressão e overfitting

Exemplo em improvement/layer7/evaluation/regression-guardrails.yaml:

```yaml
guardrails:
  - id: no_overfit_to_single_service
    rule: "policy_improvement_must_hold_in_at_least_2_services"
  - id: stability_under_load_shift
    rule: "improvement_must_hold_under_high_load_profile"
  - id: rollback_trigger
    rule: "if_false_block_rate_gt_0.12_then_rollback"
```

### Passo 3.7 - Relatório de ciclo científico

Template em improvement/layer7/reports/cycle-review-template.md deve conter:

1. Hipótese do ciclo.
2. Policy candidata e diff da policy anterior.
3. Efeito causal estimado (ATT + IC95%).
4. Métricas de segurança (falso bloqueio, missed gray failure).
5. Decisão (promover/reverter) e justificativa auditável.

## 4. Validacao de fato da Camada 7

A camada está validada quando melhoria é causalmente demonstrada, reproduzível e governada por critérios formais.

Checklist go/no-go:

1. Efeito causal demonstrado
- Mudança de política mostra efeito significativo em métrica primária.

2. Segurança preservada
- Não há piora relevante em limites de segurança e detecção crítica.

3. Robustez transversal
- Ganho não depende de um único serviço/cenário.

4. Governança auditável
- Toda promoção/reversão de política possui evidência e aprovação registrada.

5. Reprodutibilidade
- Reexecução do ciclo com mesmos insumos reproduz a decisão.

Se os 5 itens passarem, a Camada 7 está validada.

## 5. Protocolo de validacao experimental

Exemplo em improvement/layer7/validation-protocol.md:

```md
# Protocolo de Validacao - Camada 7

Cenario A - Upgrade com ganho real:
- gerar policy candidata por otimizacao
- medir ATT em MTTR com IC95%
- promover somente se gate aprovado

Cenario B - Upgrade regressivo:
- introduzir policy propositalmente agressiva
- validar aumento de falso bloqueio
- acionar rollback automatico

Cenario C - Drift de ambiente:
- alterar perfil de carga
- validar estabilidade da policy candidata

Cenario D - Reprodutibilidade:
- repetir ciclo com mesmos dados e seed
- validar mesma recomendacao de promoção/reversão
```

## 6. Comandos uteis

```bash
# disparar ciclo manualmente
argo -n argo submit --from cronwf/mecade-policy-learning

# versionar dataset e artefatos do ciclo
dvc add improvement/layer7/datasets/cycle_*.parquet

# registrar experimento de policy no mlflow
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

# consultar efeito causal (exemplo)
python improvement/layer7/jobs/causal_eval.py --policy-version vNext
```

## 7. Definicao de pronto (Definition of Done)

Camada 7 é considerada DONE quando:

- Loop contínuo executa com cadência definida.
- Política candidata é gerada por otimização sob restrições.
- Promoção depende de efeito causal estatisticamente robusto.
- Guardrails de regressão e rollback estão operacionais.
- Decisões de política são auditáveis e reproduzíveis.

## 8. Evitar erros comuns

- Chamar correlação de causalidade sem desenho apropriado.
- Ajustar thresholds por intuição sem espaço de busca formal.
- Promover política sem teste de robustez multi-cenário.
- Ignorar regressão de segurança ao otimizar MTTR.
- Não versionar dados, política e decisão do ciclo.

## 9. Fechamento tecnico

Nesta abordagem, a Camada 7 estrutura melhoria continua com criterio causal, guardrails de seguranca e decisao formal de promover ou reverter politica.
