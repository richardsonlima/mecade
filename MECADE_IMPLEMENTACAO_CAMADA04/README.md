# MECADE Camada 4 - Implementação E2E

Camada 4: Execução Experimental Científica de Falhas.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `chaos/layer4/` | Artefatos obrigatórios da camada |
| `python/` | Scripts de geração, análise e validação |
| `scripts/` | Instalação, E2E e operação Docker |
| `docker/` | Configurações mínimas de Prometheus/Grafana/OTel |
| `notebooks/` | Espaço para estudos exploratórios |

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA04
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

| Serviço | Endpoint |
|---|---|
| Prometheus | `http://localhost:9390` |
| Grafana (admin/admin) | `http://localhost:3300` |
| OpenTelemetry Collector | `http://localhost:9388` |
| Jupyter Lab (token `mecade`) | `http://localhost:9098/lab?token=mecade` |
