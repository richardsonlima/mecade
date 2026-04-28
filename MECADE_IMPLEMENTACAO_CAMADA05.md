# HOWTO: Camada 5 (Governanca Cientifica de CI/CD e Resilience Gates) do MECADE

Eu escrevi este guia como referencia E2E para implementar, testar e validar tecnicamente a governanca de release na Camada 5.

Stack open source recomendada:

- GitHub Actions ou GitLab CI (orquestracao de pipeline)
- Argo CD (promocao GitOps deterministica)
- Open Policy Agent + Conftest (governanca declarativa)
- LitmusChaos/Chaos Mesh (fault tests no SDLC)
- Prometheus + Thanos (consulta historica de SLO/SLI)
- MLflow (rastreio de versao de policy e score de gate)

## 1. O que torna esta Camada 5 inovadora

A inovacao nao e apenas "rodar caos no pipeline". E fazer decisao de deploy orientada por evidencia:

1. Gate multiobjetivo (desempenho + risco + custo de recuperacao).
2. Politica de release com risco posterior explicito.
3. Simulacao contrafactual de policy antes de enforce.
4. Promocao baseada em criterio estatistico de nao regressao.
5. Trilha de decisao auditavel (quem aprovou, com quais evidencias).

## 2. Entregas obrigatorias da Camada 5

```bash
mkdir -p cicd/layer5
mkdir -p cicd/layer5/workflows
mkdir -p cicd/layer5/policies
mkdir -p cicd/layer5/models
mkdir -p cicd/layer5/evaluation
```

Arquivos obrigatorios:

- cicd/layer5/release-gate-contract.yaml
- cicd/layer5/workflows/resilience-scientific-gate.yml
- cicd/layer5/policies/release-governance.rego
- cicd/layer5/models/risk-score-model.md
- cicd/layer5/evaluation/non-regression-criteria.md
- cicd/layer5/evaluation/policy-dryrun-protocol.md
- cicd/layer5/validation-protocol.md

Sem esses artefatos, a camada nao sustenta decisao tecnicamente defensavel.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Definir contrato de gate cientifico

Exemplo em cicd/layer5/release-gate-contract.yaml:

```yaml
gate:
  id: mecade_release_gate_v1
  required_stages:
    - build
    - deploy_staging
    - chaos_test
    - slo_validation
    - risk_scoring
    - policy_gate
inputs:
  - slo_results
  - chaos_results
  - risk_score
  - rollback_cost_estimate
decision:
  mode: multiobjective
  approve_if:
    - slo_pass == true
    - non_regression_pass == true
    - risk_score <= 0.45
    - rollback_cost_estimate <= threshold
```

Diferencial: gate explicita variaveis de decisao e criterio composto.

### Passo 3.2 - Modelar score de risco de release

Em cicd/layer5/models/risk-score-model.md:

```md
RiskScore = w1*P(SLO_violation) + w2*P(recovery_delay) + w3*change_complexity + w4*dependency_instability

Faixas:
- <= 0.30: baixo risco (promocao automatica)
- 0.31 - 0.45: risco moderado (promocao com dupla aprovacao)
- > 0.45: bloquear release
```

Diferencial: risco tratado como variavel quantitativa e não opinativa.

### Passo 3.3 - Pipeline com evidencia estatistica de nao regressao

Exemplo em cicd/layer5/workflows/resilience-scientific-gate.yml:

```yaml
name: resilience-scientific-gate
on:
  push:
    branches: ["main"]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy staging
        run: kubectl apply -f k8s/staging/

      - name: Chaos campaign
        run: bash cicd/layer5/scripts/run_chaos_campaign.sh

      - name: SLO and non-regression test
        run: python cicd/layer5/evaluation/non_regression_test.py

      - name: Risk scoring
        run: python cicd/layer5/evaluation/compute_risk_score.py

      - name: Policy gate
        run: conftest test cicd/layer5/release-gate-contract.yaml -p cicd/layer5/policies/
```

### Passo 3.4 - Criterio de nao regressao

Exemplo em cicd/layer5/evaluation/non-regression-criteria.md:

```md
Metrica primaria: MTTR
Metricas secundarias: availability, p99, error_rate

Aprovacao:
- delta_MTTR <= 0 com IC95% nao cruzando degradacao relevante
- availability nao piora alem de epsilon
- p99 nao excede limite operacional em janela de observacao
```

Diferencial: deploy depende de evidência estatistica, nao apenas check binario.

### Passo 3.5 - Dry-run de politica (contrafactual)

Exemplo em cicd/layer5/evaluation/policy-dryrun-protocol.md:

```md
Antes de promover nova politica de gate:
1. Reexecutar historico de 30 releases em modo simulacao.
2. Medir quantos releases seriam bloqueados/aprovados.
3. Quantificar falsos bloqueios e bloqueios perdidos.
4. Aprovar somente se melhora o trade-off risco x throughput de entrega.
```

Diferencial: politica e validada offline antes de afetar pipeline real.

### Passo 3.6 - Politica declarativa de governanca

Exemplo em cicd/layer5/policies/release-governance.rego:

```rego
package mecade.release

deny[msg] {
  input.gate.decision.mode != "multiobjective"
  msg := "gate deve operar em modo multiobjetivo"
}

deny[msg] {
  not input.gate.decision.approve_if[_] == "risk_score <= 0.45"
  msg := "criterio de risco maximo ausente"
}
```

### Passo 3.7 - Promocao GitOps condicionada

Fluxo recomendado:

1. Gate cientifico aprova release com evidencias.
2. Pipeline gera artefato de decisao (score, testes, policy hash).
3. Apenas entao ocorre merge para branch de ambiente.
4. Argo CD sincroniza producao de forma deterministica.

## 4. Validacao de fato da Camada 5

A Camada 5 esta validada quando release e governado por evidencia reprodutivel, nao por aprovacao manual ad hoc.

Checklist go/no-go:

1. Validade de decisao
- Gate usa variaveis mensuraveis e regra formal de aprovacao.

2. Nao regressao comprovada
- Pipeline reprova releases com degradacao estatisticamente relevante.

3. Politica robusta
- Dry-run mostra melhora de risco sem colapsar throughput.

4. Rastreabilidade
- Cada decisao de release tem artefato de evidencia e hash de policy.

5. Reprodutibilidade
- Reexecucao dos mesmos insumos produz a mesma decisao.

Se os 5 itens passarem, a Camada 5 esta validada.

## 5. Protocolo de validacao experimental

Exemplo em cicd/layer5/validation-protocol.md:

```md
# Protocolo de Validacao - Camada 5

Cenario A - Regressao controlada:
- introduzir degradacao pequena de p99
- validar reprovação por nao regressao

Cenario B - Falso bloqueio:
- simular ruído sem regressao real
- validar taxa de falso bloqueio abaixo do limite

Cenario C - Dry-run de policy nova:
- executar politica candidata em historico de releases
- comparar com policy atual (abordagem A/B offline)

Cenario D - Caminho feliz:
- release sem violacao, risco baixo e custo de rollback aceitavel
- validar promocao automatica por GitOps
```

## 6. Comandos uteis

```bash
# validar contrato e policy
conftest test cicd/layer5/release-gate-contract.yaml -p cicd/layer5/policies/

# executar teste de nao regressao
python cicd/layer5/evaluation/non_regression_test.py

# calcular risco de release
python cicd/layer5/evaluation/compute_risk_score.py

# disparar workflow
gh workflow run resilience-scientific-gate.yml

# acompanhar promocao
argocd app get checkout-prod
```

## 7. Definicao de pronto (Definition of Done)

Camada 5 e considerada DONE quando:

- Contrato multiobjetivo de gate esta versionado.
- Politica de governanca e validada por dry-run historico.
- Nao regressao estatistica esta no caminho critico de release.
- Risco de release e calculado e usado na decisao.
- Promocao GitOps ocorre apenas apos gate cientifico aprovado.

## 8.  Evitar erros comuns

- Tratar gate como checklist binario sem modelo de risco.
- Aprovar release sem criterio de nao regressao estatistica.
- Alterar policy sem validacao contrafactual (dry-run).
- Nao registrar evidencia de decisao para auditoria.
- Confundir velocidade de entrega com qualidade de decisao.

## 9. Fechamento tecnico

Nesta abordagem, a Camada 5 torna a decisao de release objetiva, rastreavel e reproduzivel, conectando risco, nao regressao e politica declarativa.
