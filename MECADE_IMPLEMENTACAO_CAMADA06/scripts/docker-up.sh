#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found."
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "Neither 'docker compose' nor 'docker-compose' was found."
  exit 1
fi

"${COMPOSE_CMD[@]}" -f "$ROOT_DIR/docker-compose.yml" up -d

echo "Stack started. Prometheus: http://localhost:9590 | Grafana: http://localhost:3500 | Jupyter: http://localhost:9298"
