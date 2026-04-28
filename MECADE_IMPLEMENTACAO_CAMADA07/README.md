# MECADE Camada 7 - Implementacao E2E

Camada 7: Aprendizado Causal Continuo e Evolucao de Politicas.

## Estrutura

- `improvement/layer7/`: artefatos obrigatorios da camada
- `python/`: scripts de geracao, analise e validacao
- `scripts/`: instalacao, E2E e operacao Docker
- `docker/`: configs minimas de Prometheus/Grafana/OTel
- `notebooks/`: espaco para estudos exploratorios

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA07
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

- Prometheus: http://localhost:9690
- Grafana: http://localhost:3600 (admin/admin)
- OpenTelemetry Collector: http://localhost:9688
- Jupyter Lab: http://localhost:9398/lab?token=mecade
