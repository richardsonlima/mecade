# MECADE Camada 2 - Implementacao E2E

Este pacote implementa a Camada 2 (Metrologia Cientifica de Objetivos e Indicadores) do MECADE com artefatos obrigatorios, scripts de validacao e stack Docker para Linux/macOS.

## Estrutura

- `planning/layer2/`: artefatos obrigatorios da Camada 2
- `python/`: scripts Python para geracao, analise e validacao
- `scripts/`: scripts shell de instalacao e execucao E2E
- `observability/dashboards/`: dashboard cientifico da Camada 2
- `docker/`: configuracao do Prometheus/Grafana/OpenTelemetry
- `docker-compose.yml`: stack local para observabilidade e analise

## Requisitos

- Linux ou macOS
- Python 3.10+
- Docker + Compose (`docker compose` ou `docker-compose`)

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA02
bash scripts/install.sh
bash scripts/run-e2e.sh
# alternativa equivalente:
# bash scripts/run_e2e.sh
```

## Subir stack Docker

```bash
bash scripts/docker-up.sh
```

Endpoints locais:

- Prometheus: http://localhost:9190
- Grafana: http://localhost:3100 (admin/admin)
- OpenTelemetry Collector: http://localhost:9188
- Thanos Sidecar: http://localhost:10902
- Thanos Query: http://localhost:10903
- Jupyter Lab: http://localhost:8898/lab?token=mecade

## Smoke test da stack

Depois de subir os servicos, rode um unico comando para validar endpoints e servicos auxiliares:

```bash
bash scripts/smoke-test.sh
```

Observacao: o Sloth e disponibilizado como CLI no compose (execucao one-shot para validacao SLO as Code), e o smoke test valida sua execucao.

## Derrubar stack

```bash
bash scripts/docker-down.sh
```

## Fluxo E2E recomendado

1. Gerar/atualizar artefatos base:
   - `python python/generate_artifacts.py`
2. Calcular RRIndex metrologico:
   - `python python/compute_rrindex.py`
3. Rodar inferencia estatistica de nao regressao:
   - `python python/run_inference.py`
4. Validar gate cientifico da camada:
   - `python python/validate_layer2.py`
5. (Opcional) Coletar evidencias:
   - `bash scripts/generate-evidence.sh`

## Observacoes

- Todos os arquivos obrigatorios da Camada 2 ja vem preenchidos para o cenario financeiro + microsservicos + Kubernetes.
- Ajuste formulas de SLI/SLO, limiares e regras estatisticas para o contexto real da sua campanha.
