# MECADE Camada 5 - Implementacao E2E

Camada 5: Governanca Cientifica de CI/CD e Resilience Gates.

## Estrutura

- `cicd/layer5/`: artefatos obrigatorios da camada
- `python/`: scripts de geracao, analise e validacao
- `scripts/`: instalacao, E2E e operacao Docker
- `docker/`: configs minimas de Prometheus/Grafana/OTel
- `notebooks/`: espaco para estudos exploratorios

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA05
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

- Prometheus: http://localhost:9490
- Grafana: http://localhost:3400 (admin/admin)
- OpenTelemetry Collector: http://localhost:9488
- Jupyter Lab: http://localhost:9198/lab?token=mecade
