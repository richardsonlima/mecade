# MECADE Camada 5 - Implementação E2E

Camada 5: Governança Científica de CI/CD e Resilience Gates.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `cicd/layer5/` | Artefatos obrigatórios da camada |
| `python/` | Scripts de geração, análise e validação |
| `scripts/` | Instalação, E2E e operação Docker |
| `docker/` | Configurações mínimas de Prometheus/Grafana/OTel |
| `notebooks/` | Espaço para estudos exploratórios |

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA05
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

| Serviço | Endpoint |
|---|---|
| Prometheus | `http://localhost:9490` |
| Grafana (admin/admin) | `http://localhost:3400` |
| OpenTelemetry Collector | `http://localhost:9488` |
| Jupyter Lab (token `mecade`) | `http://localhost:9198/lab?token=mecade` |
