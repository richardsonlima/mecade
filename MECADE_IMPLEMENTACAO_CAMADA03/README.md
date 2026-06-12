# MECADE Camada 3 - Implementação E2E

Camada 3: Detecção Científica e Decisão em Tempo Real.

## Stack Docker Compose (open source)

| Componente | Função |
|---|---|
| Prometheus + PrometheusRule | Detecção em janela curta |
| Alertmanager | Roteamento determinístico e deduplicação |
| OpenTelemetry + Tempo + Loki | Evidência causal de suporte |
| Benthos CEP | Detecção de padrão temporal (*gray failure*) |
| Argo Events | Acionamento formal de LIMIT/BLOCK via CLI |
| Grafana + Jupyter | Observabilidade e análise |

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `planning/layer3/` | Artefatos obrigatórios da camada |
| `python/` | Scripts de geração, análise e validação |
| `scripts/` | Instalação, E2E e operação Docker |
| `docker/` | Configurações da stack de observabilidade |
| `observability/` | Regras, padrões e dashboards |
| `notebooks/` | Espaço para estudos exploratórios |

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA03
bash scripts/install.sh
bash scripts/docker-up.sh
bash scripts/smoke-test.sh
bash scripts/run-e2e.sh
```

## Validação em um comando

```bash
bash scripts/smoke-test.sh
```

O smoke test valida:

- *Health endpoints* da stack completa.
- Containers essenciais em execução.
- Comando do Argo Events em modo não interativo.

## Endpoints locais

| Serviço | Endpoint |
|---|---|
| Prometheus | `http://localhost:9290` |
| Alertmanager | `http://localhost:9293` |
| Grafana (admin/admin) | `http://localhost:3200` |
| OpenTelemetry Collector (metrics) | `http://localhost:9288/metrics` |
| Loki | `http://localhost:9300/ready` |
| Tempo | `http://localhost:9301/ready` |
| Benthos | `http://localhost:4295/ready` |
| Jupyter Lab (token `mecade`) | `http://localhost:8998/lab?token=mecade` |
