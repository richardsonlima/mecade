# MECADE Campanha Minima Viavel VIII-C (Tier A1)

Implementacao executavel da campanha A/B pareada descrita no guia `MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1.md`.

## Estrutura

- `campaign/config/`: configuracao da campanha e randomizacao A/B
- `evidencias-campanha-viii-c/`: artefatos de execucao e analise
- `python/`: automacao de geracao, analise e validacao
- `scripts/`: instalacao, bootstrap Kubernetes e fluxo E2E

## Quickstart

```bash
cd MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Fluxo em cluster Kubernetes

```bash
bash scripts/bootstrap-online-boutique.sh
bash scripts/docker-up.sh
bash scripts/run-e2e.sh
bash scripts/validate.sh
bash scripts/docker-down.sh
```

## Endpoints locais (Docker Compose)

- Online Boutique Frontend: http://localhost:8088
- Prometheus: http://localhost:9790
- Grafana: http://localhost:3700 (admin/admin)
- OpenTelemetry Collector: http://localhost:9788
- Jupyter Lab: http://localhost:9498/lab?token=mecade

## Resultado esperado

Ao final do E2E, os arquivos abaixo devem existir:

- `evidencias-campanha-viii-c/analise/comparativo_ab.csv`
- `evidencias-campanha-viii-c/analise/consolidado_final.md`
- `evidencias-campanha-viii-c/analise/analysis-summary.json`
