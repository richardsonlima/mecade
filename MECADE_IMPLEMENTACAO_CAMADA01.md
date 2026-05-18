# HOWTO: Camada 1 (Planejamento Cientifico) do MECADE

Eu escrevi este guia como um roteiro E2E de implementacao, testes e validacao tecnica da Camada 1, com foco em reprodutibilidade e auditabilidade.

Stack open source recomendada para a Camada 1:

- OpenSLO (especificacao formal de objetivos)
- Prometheus (medicao operacional)
- Jupyter + Python (analise estatistica e poder amostral)
- LitmusChaos (execucao posterior, somente apos gate da Camada 1)
- Git + DVC (versionamento de protocolo e evidencias)

## 1. O que torna esta Camada 1 inovadora

A inovacao aqui nao e "usar ferramenta X". E transformar planejamento em artefato cientifico:

1. Hipoteses causais explicitas com tamanho de efeito esperado.
2. Chaos Budget derivado de risco e nao de numero arbitrario.
3. Calibracao inicial por digital twin/simulacao antes de producao.
4. Protocolo pre-registrado de experimento (antes de executar).
5. Critério de decisao com confianca estatistica e risco residual.

## 2. Entregas obrigatorias da Camada 1

Crie os artefatos abaixo:

```bash
mkdir -p planning/layer1
mkdir -p planning/layer1/prereg
mkdir -p planning/layer1/evidence
```

Arquivos obrigatorios:

- planning/layer1/steady-state.openslo.yaml
- planning/layer1/fmea-causal.csv
- planning/layer1/risk-prior.yaml
- planning/layer1/chaos-budget-model.yaml
- planning/layer1/hypotheses-causal.md
- planning/layer1/power-analysis.md
- planning/layer1/prereg/experiment-protocol.md
- planning/layer1/acceptance-gate.yaml

Sem esses arquivos, o experimento nao avanca.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Definir estado estacionario formal (OpenSLO)

Exemplo minimo:

```yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: checkout-steady-state
spec:
  service: checkout
  indicators:
    - name: availability
      ratioMetric:
        counter: http_requests_total{service="checkout",status!~"5.."}
        total: http_requests_total{service="checkout"}
    - name: p99_latency
      thresholdMetric: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="checkout"}[5m])) by (le))
  objectives:
    - displayName: availability_target
      target: 0.995
      timeWindow: 30d
    - displayName: p99_latency_target
      target: 0.300
      operator: lte
      unit: seconds
      timeWindow: 5m
```

Resultado esperado: baseline formal, mensuravel e reproduzivel.

### Passo 3.2 - FMEA causal (nao apenas listagem)

Exemplo em planning/layer1/fmea-causal.csv:

```csv
failure_mode,cause,pathway,observable_effect,severity,occurrence,detection,rpn,owner
network_latency_800ms,mesh_delay_fault,checkout->payment->timeout,p99_up_and_tsr_down,9,6,4,216,platform
retry_storm,retry_policy_misconfig,checkout->retry_loop,error_rate_up_without_outage,8,5,6,240,sre
pod_kill_payment,node_pressure,payment->failover->recovery,short_unavailability,7,4,3,84,platform
```

Diferencial: inclua pathway causal (causa -> propagacao -> efeito observado).

### Passo 3.3 - Definir prior de risco (Bayes simples)

Exemplo em planning/layer1/risk-prior.yaml:

```yaml
risk_prior:
  financial:
    p_critical_failure: 0.12
    impact_weight: 0.9
  aerospace:
    p_critical_failure: 0.08
    impact_weight: 1.0
  infrastructure:
    p_critical_failure: 0.15
    impact_weight: 0.85
```

Uso: o budget e os limiares de aceitacao devem ser mais conservadores para maior impacto ponderado.

### Passo 3.4 - Modelar Chaos Budget por risco

Exemplo em planning/layer1/chaos-budget-model.yaml:

```yaml
service: checkout
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
```

Diferencial: budget justificado por modelo de risco explicito.

### Passo 3.5 - Escrever hipoteses causais com tamanho de efeito

Exemplo em planning/layer1/hypotheses-causal.md:

```md
# H1 - Efeito esperado do mecanismo de bloqueio

Intervencao: ativar controle ALERT/LIMIT/BLOCK durante falha de latencia progressiva.

Hipotese causal:
- O controle reduz MTTR em pelo menos 15% versus baseline reativo.

Metrica primaria:
- MTTR (s)

Metricas secundarias:
- p99 latency, error_rate, TSR

Criterio de sucesso:
- delta_MTTR <= -15% com IC95% excluindo 0.
```

### Passo 3.6 - Fazer analise de poder amostral

Em planning/layer1/power-analysis.md documente:

1. Efeito minimo detectavel (ex.: 15% em MTTR).
2. Poder estatistico alvo (>= 0.8).
3. Nivel de significancia (alpha = 0.05).
4. Numero minimo de repeticoes por cenario.

Sem poder amostral, resultado vira demonstracao, nao evidencia.

### Passo 3.7 - Pre-registrar protocolo

Exemplo em planning/layer1/prereg/experiment-protocol.md:

```md
# Pre-registro do experimento

- Pergunta de pesquisa
- Hipoteses H1..Hn
- Metricas primaria/secundarias
- Cenarios de falha
- Numero de repeticoes
- Regras de exclusao de execucao invalida
- Metodo estatistico
- Criterio de aceite/rejeicao
```

Pre-registro reduz viés de confirmacao e fortalece defesa academica.

### Passo 3.8 - Definir gate de aceite tecnico-cientifico

Exemplo em planning/layer1/acceptance-gate.yaml:

```yaml
must_have:
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
```

## 4. Validacao de fato da Camada 1

A Camada 1 esta validada quando o planejamento permite inferencia causal minima, nao apenas checklist operacional.

Checklist go/no-go:

1. Constructo valido
- Cada hipotese possui intervencao, mecanismo esperado e metrica primaria.

2. Rigor estatistico
- Existe poder amostral e regra de decisao pre-definida.

3. Risco explicitado
- Chaos Budget foi derivado por prior de risco e dominio.

4. Reprodutibilidade
- Protocolo pre-registrado e versionado.

5. Auditabilidade
- Decisoes de planejamento deixam trilha de evidencia.

Se os 5 itens passarem, a Camada 1 esta validada para execucao.

## 5. Comandos uteis

```bash
# validar sintaxe dos artefatos yaml
yq e '.' planning/layer1/*.yaml > /dev/null

# registrar evidencias de planejamento no dvc
dvc add planning/layer1/evidence/

# versionar protocolo pre-registrado
git add planning/layer1/prereg/experiment-protocol.md
```

## 6. Definicao de pronto (Definition of Done)

Considere Camada 1 DONE quando:

- Hipoteses causais com efeito minimo detectavel estao definidas.
- Budget e limiares tem justificativa de risco.
- Plano estatistico esta documentado antes dos testes.
- Gate cientifico foi executado e aprovado.
- Ha aprovacao conjunta de SRE + orientacao metodologica.

## 7.  Evitar erros comuns

- Definir hipotese sem tamanho de efeito.
- Usar threshold por conveniencia sem racional de risco.
- Rodar experimento sem pre-registro.
- Reportar so media sem intervalo de confianca.
- Chamar PoC de validacao robusta sem analise de poder.

## 8. Fechamento tecnico

Nesta abordagem, a Camada 1 deixa de ser checklist e vira base tecnica para execucao experimental com criterio, evidencia e decisao reproduzivel.
