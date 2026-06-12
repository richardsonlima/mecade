# MECADE Camada 6 - Implementação E2E

Camada 6: Auditoria Científica, Prova Criptográfica e Governança Determinística.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `audit/layer6/` | Artefatos obrigatórios da camada |
| `python/` | Scripts de geração, análise e validação |
| `scripts/` | Instalação, E2E e operação Docker |
| `docker/` | Configurações mínimas de Prometheus/Grafana/OTel |
| `notebooks/` | Espaço para estudos exploratórios |

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA06
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

| Serviço | Endpoint |
|---|---|
| Prometheus | `http://localhost:9590` |
| Grafana (admin/admin) | `http://localhost:3500` |
| OpenTelemetry Collector | `http://localhost:9588` |
| Jupyter Lab (token `mecade`) | `http://localhost:9298/lab?token=mecade` |
