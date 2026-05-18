# MECADE Camada 1 - Implementacao E2E

Este pacote implementa a Camada 1 (Planejamento Cientifico) do MECADE com artefatos obrigatorios, scripts de validacao e stack Docker para Linux/macOS.

## Estrutura

- `planning/layer1/`: artefatos obrigatorios da Camada 1
- `python/`: scripts Python para geracao, validacao e analise
- `scripts/`: scripts shell de instalacao e execucao E2E
- `docker/`: configuracao do Prometheus/Grafana
- `docker-compose.yml`: stack local para observabilidade e analise

## Requisitos

- Linux ou macOS
- Python 3.10+
- Docker + Compose (`docker compose` ou `docker-compose`)

## Quickstart

```bash
cd MECADE_IMPLEMENTACAO_CAMADA01
bash scripts/install.sh
bash scripts/run-e2e.sh
# alternativa equivalente:
# bash scripts/run_e2e.sh
```

## Subir stack Docker

```bash
bash scripts/docker-up.sh
```

## Smoke test da stack

Depois de subir os servicos, rode um unico comando para validar os endpoints principais:

```bash
bash scripts/smoke-test.sh
```

Endpoints locais:

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Jupyter Lab: http://localhost:8888/lab?token=mecade
- Pushgateway: http://localhost:9091

## Derrubar stack

```bash
bash scripts/docker-down.sh
```

## Fluxo E2E recomendado

1. Gerar/atualizar artefatos base:
   - `python python/generate_artifacts.py`
2. Calcular budget por risco:
   - `python python/compute_chaos_budget.py`
3. Rodar analise de poder:
   - `python python/power_analysis.py --baseline-mttr 120 --stddev 30 --effect-pct 0.15 --power 0.8 --alpha 0.05`
4. Validar gate cientifico:
   - `python python/validate_layer1.py`
5. (Opcional) Coletar evidencias:
   - `bash scripts/generate-evidence.sh`

## Observacoes

- Todos os arquivos obrigatorios da Camada 1 ja vem preenchidos para o cenario financeiro + microsservicos + Kubernetes.
- Ajuste nomes de servico, SLIs, limiares e hipoteses para seu contexto.
