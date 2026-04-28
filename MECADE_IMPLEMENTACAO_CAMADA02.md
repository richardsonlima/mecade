# HOWTO: Camada 2 (Metrologia Cientifica de Objetivos e Indicadores) do MECADE

Eu escrevi este guia como referencia E2E para implementar, testar e validar tecnicamente a Camada 2 com rigor metrologico e trilha de evidencia.

Stack open source recomendada:

- OpenTelemetry (instrumentacao semantica)
- Prometheus + Thanos (coleta, historico e consulta)
- Grafana (visualizacao e inspeção)
- OpenSLO/Sloth (SLO as Code)
- Great Expectations (qualidade de dados de telemetria)
- Jupyter + Python (inferencia estatistica e analise de incerteza)

## 1. O que torna esta Camada 2 inovadora

A inovacao nao e apenas medir P95/P99. E transformar telemetria em evidência científica:

1. Metricas com definicao operacional + incerteza associada.
2. SLI/SLO com rastreabilidade matematica e semantica.
3. Contrato de qualidade de dados observacionais antes de decidir.
4. RRIndex metrologico como indicador agregado de maturidade.
5. Decisao pass/fail baseada em efeito e confianca, nao so threshold fixo.

## 2. Entregas obrigatorias da Camada 2

```bash
mkdir -p planning/layer2
mkdir -p planning/layer2/data-quality
mkdir -p planning/layer2/stats
mkdir -p observability/dashboards
```

Arquivos obrigatorios:

- planning/layer2/metric-dictionary.yaml
- planning/layer2/sli-slo-contract.yaml
- planning/layer2/rrindex-definition.md
- planning/layer2/data-quality/gx-suite.yaml
- planning/layer2/stats/decision-rule.md
- planning/layer2/validation-rules.yaml
- observability/dashboards/layer2-scientific-overview.json

Sem esses artefatos, a camada nao atende rigor metrologico.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Definir dicionario metrologico de metricas

Exemplo em planning/layer2/metric-dictionary.yaml:

```yaml
service: checkout
metrics:
  - id: availability
    definition: "Proporcao de requisicoes bem-sucedidas"
    formula: "sum(rate(http_requests_total{service=\"checkout\",status!~\"5..\"}[5m])) / sum(rate(http_requests_total{service=\"checkout\"}[5m]))"
    unit: ratio
    expected_range: [0.0, 1.0]
    sampling_window: 5m
    uncertainty: "bootstrap_ci_95"

  - id: p99_latency_seconds
    definition: "Latencia no percentil 99"
    formula: "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service=\"checkout\"}[5m])) by (le))"
    unit: seconds
    expected_range: [0.0, 5.0]
    sampling_window: 5m
    uncertainty: "block_bootstrap_ci_95"
```

Diferencial: cada metrica tem unidade, faixa esperada e metodo de incerteza.

### Passo 3.2 - Formalizar contrato SLI/SLO

Exemplo em planning/layer2/sli-slo-contract.yaml:

```yaml
version: 1
service: checkout
objectives:
  - id: slo_availability_30d
    sli: availability
    target: 0.995
    window: 30d
    error_budget: 0.005

  - id: slo_p99_5m
    sli: p99_latency_seconds
    target_lte: 0.300
    window: 5m

traceability:
  business_goal:
    - continuidade_operacional
    - experiencia_usuario
```

Diferencial: conecta SLO tecnico a objetivo de negocio e budget de erro.

### Passo 3.3 - Definir RRIndex de forma reprodutivel

Exemplo em planning/layer2/rrindex-definition.md:

```md
RRIndex = w1 * (1 - norm_mttr) + w2 * norm_availability + w3 * (1 - norm_p99) + w4 * norm_tsr

Restricoes:
- w1 + w2 + w3 + w4 = 1
- pesos definidos por dominio de risco
- normalizacao por baseline pre-registrado

Saida:
- RRIndex em [0,1], maior e melhor
```

Diferencial: indice agregado com formula e restricoes explicitas.

### Passo 3.4 - Qualidade de dados como gate cientifico

Exemplo em planning/layer2/data-quality/gx-suite.yaml:

```yaml
expectations:
  - expect_column_values_to_not_be_null:
      column: timestamp
  - expect_column_values_to_be_between:
      column: availability
      min_value: 0
      max_value: 1
  - expect_column_values_to_be_between:
      column: p99_latency_seconds
      min_value: 0
      max_value: 5
  - expect_column_pair_values_A_to_be_greater_than_B:
      column_A: window_end
      column_B: window_start
```

Sem qualidade minima, a inferencia e invalidada.

### Passo 3.5 - Definir regra estatistica de decisao

Exemplo em planning/layer2/stats/decision-rule.md:

```md
Hipotese de melhoria operacional:
- H0: delta_MTTR >= 0
- H1: delta_MTTR < 0

Criterio de aprovacao:
- IC95% de delta_MTTR totalmente abaixo de 0
- tamanho de efeito absoluto >= 10%
- nenhuma violacao critica simultanea de availability e p99
```

Diferencial: decisao baseada em evidencia e efeito pratico.

### Passo 3.6 - Regras pass/fail por experimento

Exemplo em planning/layer2/validation-rules.yaml:

```yaml
experiment: net-latency-800ms
window: 10m
primary_decision:
  metric: mttr_seconds
  require_ci95_below_zero_delta: true
  minimum_effect_percent: 10
safety_constraints:
  - metric: availability
    op: gte
    value: 0.995
  - metric: p99_latency_seconds
    op: lte
    value: 0.450
```

### Passo 3.7 - Dashboard cientifico

O dashboard da Camada 2 deve ter:

1. Serie temporal de metrica com banda de confianca.
2. Valor pontual + intervalo de incerteza.
3. Error budget burn rate.
4. RRIndex por ciclo.
5. Estado do contrato de qualidade de dados.

## 4. Validacao de fato da Camada 2

A Camada 2 esta validada quando indicadores sao mediveis, confiaveis e inferencialmente utilizaveis.

Checklist go/no-go:

1. Validade de constructo
- Cada metrica possui definicao operacional e unidade.

2. Qualidade observacional
- Contrato de dados aprovado antes da analise.

3. Rigor inferencial
- Decisao usa intervalo de confianca e tamanho de efeito.

4. Reprodutibilidade
- Mesma consulta e janela reproduzem resultados equivalentes.

5. Acionabilidade
- Regras tecnicas conectam objetivo de negocio e risco.

Se os 5 itens passarem, a Camada 2 esta validada.

## 5. Comandos uteis

```bash
# validar contrato SLO
sloth validate -i planning/layer2/sli-slo-contract.yaml

# validar qualidade de dados (exemplo)
great_expectations checkpoint run layer2_metrics_checkpoint

# consultar metrica no Prometheus
curl -s http://localhost:9090/api/v1/query --data-urlencode 'query=sum(rate(http_requests_total{service="checkout"}[5m]))'

# gerar resumo estatistico (exemplo)
python planning/layer2/stats/run_inference.py
```

## 6. Definicao de pronto (Definition of Done)

Camada 2 e considerada DONE quando:

- Dicionario metrologico e contrato SLI/SLO estao versionados.
- RRIndex possui definicao formal e reproducivel.
- Qualidade de dados e validada antes de decidir.
- Regra de decisao estatistica esta predefinida.
- Dashboard cientifico exibe incerteza, budget e maturidade.

## 7.  Evitar erros comuns

- Tratar metrica como numero absoluto sem incerteza.
- Misturar unidade (ms/s) sem normalizacao documentada.
- Decidir por threshold sem efeito estatistico.
- Ignorar qualidade dos dados de telemetria.
- Criar indice agregado sem formula explicita.

## 8. Fechamento tecnico

Nesta abordagem, a Camada 2 conecta metrica, qualidade de dados e inferencia estatistica para sustentar decisao operacional com base objetiva.
