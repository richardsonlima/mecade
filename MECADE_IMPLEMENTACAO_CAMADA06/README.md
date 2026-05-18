# MECADE Camada 6 - Implementacao E2E

Camada 6: Auditoria Cientifica, Prova Criptografica e Governanca Deterministica.

## Estrutura

- `audit/layer6/`: artefatos obrigatorios da camada
- `python/`: scripts de geracao, analise e validacao
- `scripts/`: instalacao, E2E e operacao Docker
- `docker/`: configs minimas de Prometheus/Grafana/OTel
- `notebooks/`: espaco para estudos exploratorios

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA06
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

- Prometheus: http://localhost:9590
- Grafana: http://localhost:3500 (admin/admin)
- OpenTelemetry Collector: http://localhost:9588
- Jupyter Lab: http://localhost:9298/lab?token=mecade
