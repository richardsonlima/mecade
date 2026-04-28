# HOWTO: Camada 3 (Deteccao Cientifica e Decisao em Tempo Real) do MECADE

Eu escrevi este guia como passo a passo E2E para implementar, testar e validar tecnicamente a Camada 3 em tempo real.

Stack open source recomendada:

- Prometheus + PrometheusRule (deteccao em janela curta)
- Alertmanager (roteamento deterministico e deduplicacao)
- OpenTelemetry + Tempo + Loki (evidencia causal de suporte)
- Flink CEP ou Benthos (deteccao de padrao temporal/gray failure)
- Argo Events (acionamento formal de LIMIT/BLOCK)

## 1. O que torna esta Camada 3 inovadora

A inovacao da Camada 3 nao e apenas "alertar mais rapido". E transformar deteccao em mecanismo de inferencia operacional:

1. Deteccao em comite (metrica + log + trace), nao sinal unico.
2. Limiar hibrido: limite duro de seguranca + sensibilidade adaptativa supervisionada.
3. Captura de gray failure como fenomeno temporal, nao apenas pico instantaneo.
4. Decisao baseada em risco posterior (likelihood x impacto), nao somente threshold.
5. BLOCK acionado por criterio formal e auditavel com latencia medida.

## 2. Entregas obrigatorias da Camada 3

```bash
mkdir -p planning/layer3
mkdir -p planning/layer3/models
mkdir -p observability/rules
mkdir -p observability/patterns
mkdir -p automation/block
```

Arquivos obrigatorios:

- planning/layer3/detection-contract.yaml
- planning/layer3/models/risk-posterior-model.md
- observability/rules/alert-limit-block.rules.yaml
- observability/patterns/gray-failure-cep.yaml
- planning/layer3/false-positive-negative-tracker.md
- automation/block/block-decision-policy.yaml
- planning/layer3/validation-protocol.md

Sem esses artefatos, a camada nao atende rigor de decisao critica.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Definir contrato de deteccao

Exemplo em planning/layer3/detection-contract.yaml:

```yaml
service: checkout
steady_state:
  p99_latency_seconds: 0.300
  error_rate: 0.010
hard_safety_limits:
  max_p99_latency_seconds: 0.600
  max_error_rate: 0.030
adaptive_zone:
  alert_relative_deviation: 0.20
  limit_relative_deviation: 0.40
windows:
  instant: 60s
  accumulated: 10m
required_evidence:
  - metric_signal
  - trace_or_log_corroboration
```

Diferencial: separa explicitamente limite duro (inviolavel) de zona adaptativa.

### Passo 3.2 - Regras de ALERT/LIMIT/BLOCK com desvio acumulado

Exemplo em observability/rules/alert-limit-block.rules.yaml:

```yaml
groups:
  - name: mecade-layer3-scientific
    interval: 15s
    rules:
      - record: mecade:checkout:p99
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="checkout"}[1m])) by (le))

      - record: mecade:checkout:error_rate
        expr: sum(rate(http_requests_total{service="checkout",status=~"5.."}[1m])) / sum(rate(http_requests_total{service="checkout"}[1m]))

      - record: mecade:checkout:relative_deviation
        expr: (mecade:checkout:p99 - 0.300) / 0.300

      - record: mecade:checkout:accum_dev_10m
        expr: sum_over_time(clamp_min(mecade:checkout:relative_deviation, 0)[10m:15s])

      - alert: MECADEAlert
        expr: mecade:checkout:relative_deviation > 0.20
        for: 1m
        labels:
          severity: warning
          mecade_axiom: ALERT

      - alert: MECADELimit
        expr: mecade:checkout:relative_deviation > 0.40 or mecade:checkout:accum_dev_10m > 8
        for: 30s
        labels:
          severity: critical
          mecade_axiom: LIMIT

      - alert: MECADEBlockHardSafety
        expr: mecade:checkout:p99 > 0.600 or mecade:checkout:error_rate > 0.030
        for: 15s
        labels:
          severity: critical
          mecade_axiom: BLOCK
```

### Passo 3.3 - Definir detector temporal de gray failure

Exemplo em observability/patterns/gray-failure-cep.yaml:

```yaml
pattern_id: gray_failure_latency_drift
window: 12m
conditions:
  - metric: p99_latency
    trend: increasing
    min_slope_per_minute: 0.01
  - metric: error_rate
    op: lte
    value: 0.01
  - metric: retry_rate
    op: gte
    value: 0.12
decision:
  emit_event: GRAY_FAILURE_SUSPECTED
  confidence_min: 0.8
```

Diferencial: modela degradacao progressiva com padrao temporal, nao limiar isolado.

### Passo 3.4 - Modelo de risco posterior para decisao

Em planning/layer3/models/risk-posterior-model.md documente:

```md
PosteriorRisk = P(falha_critica | sinais) * ImpactoDominio

Regra:
- ALERT quando PosteriorRisk >= 0.30
- LIMIT quando PosteriorRisk >= 0.55
- BLOCK quando PosteriorRisk >= 0.80 ou hard_safety_limits violados
```

Diferencial: decisao baseada em risco condicional e criticidade de dominio.

### Passo 3.5 - Politica formal de BLOCK

Exemplo em automation/block/block-decision-policy.yaml:

```yaml
block_policy:
  trigger_any:
    - alert_name: MECADEBlockHardSafety
    - posterior_risk_gte: 0.80
  require_evidence:
    - metric_signal
    - trace_or_log_corroboration
  actions:
    - stop_fault_injection: true
    - apply_safe_state_runbook: true
  max_decision_latency_ms: 1500
  audit_required: true
```

### Passo 3.6 - Medir qualidade da deteccao

Em planning/layer3/false-positive-negative-tracker.md registre por ciclo:

1. Precision e recall para eventos criticos.
2. Taxa de falso positivo ALERT/LIMIT.
3. Taxa de falso negativo em gray failure.
4. Lead-time-to-failure (tempo entre ALERT e violacao LIMIT/BLOCK).
5. Tempo de decisao (detectar -> acionar BLOCK).

Sem isso, nao ha evidencia de superioridade da camada.

## 4. Validacao de fato da Camada 3

A camada esta validada quando detecta cedo, decide corretamente e bloqueia com baixa latencia sem explodir falsos positivos.

Checklist go/no-go:

1. Sensibilidade temporal
- Gray failure detectado antes de violacao critica em >= 70% dos cenarios.

2. Especificidade operacional
- Falso positivo de LIMIT/BLOCK abaixo do limiar acordado (ex.: <= 10%).

3. Latencia de decisao
- BLOCK acionado dentro da meta (ex.: <= 1.5s) apos criterio formal.

4. Robustez de evidencia
- ALERT/LIMIT com corroboracao de ao menos dois sinais independentes.

5. Reprodutibilidade
- Mesmos cenarios produzem padroes de decisao equivalentes em repeticoes independentes.

Se os 5 itens passarem, a Camada 3 esta validada.

## 5. Protocolo de validacao experimental

Exemplo em planning/layer3/validation-protocol.md:

```md
# Protocolo de Validacao - Camada 3

Cenario A - Drift progressivo sem outage:
- aumentar latencia em degraus a cada 2 minutos
- validar deteccao de gray failure antes de 5xx massivo

Cenario B - Ruido sem falha real:
- injetar variabilidade controlada de curta duracao
- validar que LIMIT/BLOCK nao disparam indevidamente

Cenario C - Hard safety:
- violar limite duro de p99/error_rate
- validar BLOCK em tempo alvo e transicao para estado seguro

Cenario D - Ablacao de sinais:
- remover log/trace e repetir cenario
- medir degradacao da qualidade de decisao do comite
```

## 6. Comandos uteis

```bash
# aplicar regras cientificas
kubectl apply -f observability/rules/alert-limit-block.rules.yaml

# validar regras no Prometheus Operator
kubectl -n monitoring get prometheusrules

# acompanhar alertas
kubectl -n monitoring logs deploy/alertmanager-main --tail=200

# validar sensor de bloqueio
kubectl -n argo-events get sensors
kubectl -n argo get workflows
```

## 7. Definicao de pronto (Definition of Done)

Camada 3 e considerada DONE quando:

- Contrato de deteccao (limite duro + zona adaptativa) esta versionado.
- Detector de gray failure temporal esta ativo e validado.
- BLOCK possui politica formal com latencia alvo e auditoria.
- Qualidade da deteccao (precision/recall/falso positivo) esta medida.
- Resultados sao reproduziveis em multiplas repeticoes.

## 8. Fechamento tecnico

Nesta abordagem, a Camada 3 transforma deteccao em decisao operacional formal, com criterio de risco, latencia alvo e evidencia auditavel.
