# MECADE Camada 7 - Implementação E2E

Camada 7: Aprendizado Causal Contínuo e Evolução de Políticas.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `improvement/layer7/` | Artefatos obrigatórios da camada |
| `python/` | Scripts de geração, análise e validação |
| `scripts/` | Instalação, E2E e operação Docker |
| `docker/` | Configurações mínimas de Prometheus/Grafana/OTel |
| `notebooks/` | Espaço para estudos exploratórios |

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA07
bash scripts/install.sh
bash scripts/run-e2e.sh
```

## Endpoints locais

| Serviço | Endpoint |
|---|---|
| Prometheus | `http://localhost:9690` |
| Grafana (admin/admin) | `http://localhost:3600` |
| OpenTelemetry Collector | `http://localhost:9688` |
| Jupyter Lab (token `mecade`) | `http://localhost:9398/lab?token=mecade` |
