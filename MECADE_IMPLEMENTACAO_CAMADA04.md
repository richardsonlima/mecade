# HOWTO: Camada 4 (Execucao Experimental Cientifica de Falhas) do MECADE

Eu escrevi este guia como roteiro E2E para executar, testar e validar tecnicamente experimentos de falha na Camada 4.

Stack open source recomendada:

- LitmusChaos + Chaos Mesh (injeção de falhas em diferentes niveis)
- Kubernetes + Istio (controle de escopo e rede)
- Argo Workflows (orquestracao reproduzivel)
- Keptn ou custom evaluator em Python (avaliacao automatizada de experimento)
- Prometheus + Tempo + Loki (evidencias operacionais e causais)

## 1. O que torna esta Camada 4 inovadora

A inovacao nao e apenas "rodar chaos". E executar falhas como experimento controlado com validade interna:

1. DSL de cenario para padronizar injecao, escopo, duracao e rollback.
2. Execucao progressiva canario com expansao condicionada a gates.
3. Preflight formal de seguranca antes de cada rodada.
4. Desenho de ablação (com/sem mecanismo) para identificar causalidade de mitigacao.
5. Medida de efeito operacional com criterio estatistico, nao so observacao visual.

## 2. Entregas obrigatorias da Camada 4

```bash
mkdir -p chaos/layer4
mkdir -p chaos/layer4/dsl
mkdir -p chaos/layer4/experiments
mkdir -p chaos/layer4/workflows
mkdir -p chaos/layer4/safety
mkdir -p chaos/layer4/evaluation
```

Arquivos obrigatorios:

- chaos/layer4/dsl/scenario-spec.yaml
- chaos/layer4/safety/preflight-checklist.yaml
- chaos/layer4/experiments/fault-library.yaml
- chaos/layer4/workflows/progressive-chaos.yaml
- chaos/layer4/evaluation/effect-size-criteria.md
- chaos/layer4/evaluation/ablation-plan.md
- chaos/layer4/validation-protocol.md

Sem esses artefatos, a camada nao comprova efetividade com rigor.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Definir DSL de cenario experimental

Exemplo em chaos/layer4/dsl/scenario-spec.yaml:

```yaml
scenario_id: S4_NET_LATENCY_PROGRESSIVE
service_under_test: checkout
hypothesis_ref: H1
fault_model:
  type: network_latency
  target: checkout->payment
  profile:
    - step: 1
      delay_ms: 150
      duration_s: 120
    - step: 2
      delay_ms: 400
      duration_s: 120
    - step: 3
      delay_ms: 800
      duration_s: 120
blast_radius:
  namespace: shop
  max_replicas_affected: 1
safety:
  hard_abort:
    p99_latency_seconds_gt: 0.600
    error_rate_gt: 0.030
rollback:
  remove_fault_object: true
  restore_replicas: true
```

Diferencial: a DSL permite reexecucao identica e comparacao entre rodadas.

### Passo 3.2 - Preflight de seguranca automatizado

Exemplo em chaos/layer4/safety/preflight-checklist.yaml:

```yaml
checks:
  - id: min_replicas_ready
    query: "k8s_deployment_ready_replicas{deployment='checkout'} >= 3"
  - id: budget_available
    query: "mecade:remaining_error_budget_ratio > 0.20"
  - id: no_active_incident
    query: "incident_open_critical == 0"
  - id: rollback_path_valid
    query: "runbook_block_safe_state_available == 1"
on_fail: block_experiment
```

Sem preflight aprovado, experimento nao inicia.

### Passo 3.3 - Biblioteca de falhas com mapeamento causal

Exemplo em chaos/layer4/experiments/fault-library.yaml:

```yaml
faults:
  - id: pod_delete
    tool: litmus
    layer: compute
    expected_effect: short_availability_drop
    causal_path: pod_eviction->reschedule->recovery

  - id: network_latency
    tool: istio
    layer: network
    expected_effect: p99_drift_and_timeout
    causal_path: queueing->retry->tail_latency

  - id: cpu_hog
    tool: litmus
    layer: resource
    expected_effect: service_degradation
    causal_path: throttling->slow_response->error_spike
```

### Passo 3.4 - Orquestrar caos progressivo canario

Exemplo em chaos/layer4/workflows/progressive-chaos.yaml:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: mecade-progressive-chaos-
  namespace: argo
spec:
  entrypoint: progressive
  templates:
    - name: progressive
      steps:
        - - name: preflight
            template: run
            arguments:
              parameters:
                - name: cmd
                  value: "python chaos/layer4/safety/run_preflight.py"
        - - name: inject-step-1
            template: run
            arguments:
              parameters:
                - name: cmd
                  value: "python chaos/layer4/runner.py --step 1"
        - - name: gate-step-1
            template: run
            arguments:
              parameters:
                - name: cmd
                  value: "python chaos/layer4/evaluation/gate.py --step 1"
        - - name: inject-step-2
            template: run
            arguments:
              parameters:
                - name: cmd
                  value: "python chaos/layer4/runner.py --step 2"

    - name: run
      inputs:
        parameters:
          - name: cmd
      container:
        image: python:3.12-slim
        command: ["sh", "-c"]
        args: ["{{inputs.parameters.cmd}}"]
```

Diferencial: cada etapa so avanca com gate aprovado.

### Passo 3.5 - Plano de ablação para causalidade

Em chaos/layer4/evaluation/ablation-plan.md documente:

1. Baseline reativo sem ALERT/LIMIT/BLOCK.
2. Execucao com ALERT apenas.
3. Execucao com ALERT+LIMIT.
4. Execucao completa com ALERT+LIMIT+BLOCK.

Objetivo: isolar contribuicao causal de cada mecanismo.

### Passo 3.6 - Definir criterio de efeito operacional

Exemplo em chaos/layer4/evaluation/effect-size-criteria.md:

```md
Metrica primaria:
- MTTR

Criterio de sucesso:
- Reducao >= 15% vs baseline reativo
- IC95% de delta_MTTR abaixo de 0

Restricoes de seguranca:
- availability >= 99.5%
- p99 <= 450ms apos recovery
```

## 4. Validacao de fato da Camada 4

A camada esta validada quando a injecao e controlada, causalmente interpretavel e reproduzivel.

Checklist go/no-go:

1. Controle de escopo
- Blast radius respeitado em todas as rodadas.

2. Seguranca experimental
- Preflight aprovado e hard-abort funcional.

3. Reprodutibilidade
- Cenario DSL reproduz comportamento equivalente em repeticoes.

4. Causalidade operacional
- Ablacao mostra ganho incremental dos mecanismos de controle.

5. Efetividade estatistica
- Ganho de MTTR/RTO com criterio de efeito + confianca.

Se os 5 itens passarem, a Camada 4 esta validada.

## 5. Protocolo de validacao experimental

Exemplo em chaos/layer4/validation-protocol.md:

```md
# Protocolo de Validacao - Camada 4

Cenario A - Canary progression:
- executar step 1 (150ms), step 2 (400ms), step 3 (800ms)
- validar gates por etapa antes de escalar fault

Cenario B - Ablacao de controles:
- repetir o mesmo fault profile em quatro condicoes (baseline, ALERT, ALERT+LIMIT, completo)
- medir delta de MTTR e taxa de violacao

Cenario C - Hard abort:
- forcar violacao de limite duro
- validar interrupcao em tempo alvo e rollback para estado seguro

Cenario D - Repetibilidade:
- executar no minimo N repeticoes por cenario
- comparar variabilidade entre lotes
```

## 6. Comandos uteis

```bash
# aplicar experimentos/faults
kubectl apply -f chaos/layer4/experiments/

# iniciar workflow progressivo
argo -n argo submit chaos/layer4/workflows/progressive-chaos.yaml

# acompanhar resultados litmus/mesh
kubectl -n litmus get chaosresults
kubectl -n shop get virtualservice

# rollback emergencial
python chaos/layer4/safety/force_safe_state.py
```

## 7. Definicao de pronto (Definition of Done)

Camada 4 e considerada DONE quando:

- DSL de cenario esta versionada e em uso.
- Preflight de seguranca bloqueia execucao insegura.
- Workflow progressivo canario funciona com gates.
- Plano de ablacao foi executado e analisado.
- Efeito operacional foi demonstrado com criterio estatistico.

## 8. Evitar erros comuns

- Injetar falha sem desenho experimental causal.
- Escalar intensidade sem gate intermediario.
- Nao medir efeito incremental dos mecanismos de controle.
- Confundir observacao pontual com evidência estatistica.
- Nao documentar rollback e hard-abort em tempo alvo.

## 9. Fechamento tecnico

Nesta abordagem, a Camada 4 organiza o caos de forma controlada, progressiva e mensuravel, com gates claros de seguranca e criterio de efeito.
