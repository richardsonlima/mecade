# MECADE Camada 3 - Implementacao E2E

Camada 3: Deteccao Cientifica e Decisao em Tempo Real.

## Stack Docker Compose (open source)

- Prometheus + PrometheusRule (deteccao em janela curta)
- Alertmanager (roteamento deterministico e deduplicacao)
- OpenTelemetry + Tempo + Loki (evidencia causal de suporte)
- Benthos CEP (deteccao de padrao temporal/gray failure)
- Argo Events (acionamento formal de LIMIT/BLOCK via CLI)
- Grafana + Jupyter para observabilidade e analise

## Estrutura

- `planning/layer3/`: artefatos obrigatorios da camada
- `python/`: scripts de geracao, analise e validacao
- `scripts/`: instalacao, E2E e operacao Docker
- `docker/`: configs da stack de observabilidade
- `observability/`: regras, padroes e dashboards
- `notebooks/`: espaco para estudos exploratorios

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA03
bash scripts/install.sh
bash scripts/docker-up.sh
bash scripts/smoke-test.sh
bash scripts/run-e2e.sh
```

## Validacao em um comando

```bash
bash scripts/smoke-test.sh
```

O smoke test valida:
- Health endpoints da stack completa
- Containers essenciais em execucao
- Comando do Argo Events em modo nao interativo

## Endpoints locais

- Prometheus: http://localhost:9290
- Alertmanager: http://localhost:9293
- Grafana: http://localhost:3200 (admin/admin)
- OpenTelemetry Collector metrics: http://localhost:9288/metrics
- Loki: http://localhost:9300/ready
- Tempo: http://localhost:9301/ready
- Benthos: http://localhost:4295/ready
- Jupyter Lab: http://localhost:8998/lab?token=mecade
