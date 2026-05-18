# MECADE Camada 4 - Implementacao E2E

Camada 4: Execucao Experimental Cientifica de Falhas.

## Estrutura

- `chaos/layer4/`: artefatos obrigatorios da camada
- `python/`: scripts de geracao, analise e validacao
- `scripts/`: instalacao, E2E e operacao Docker
- `docker/`: configs minimas de Prometheus/Grafana/OTel
- `notebooks/`: espaco para estudos exploratorios

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA04
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

- Prometheus: http://localhost:9390
- Grafana: http://localhost:3300 (admin/admin)
- OpenTelemetry Collector: http://localhost:9388
- Jupyter Lab: http://localhost:9098/lab?token=mecade
