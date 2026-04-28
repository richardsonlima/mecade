#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Install Docker Desktop or Docker Engine first."
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

max_attempts=4
attempt=1
while true; do
  echo "Starting Docker stack (attempt ${attempt}/${max_attempts})..."
  if "${COMPOSE_CMD[@]}" -f "$ROOT_DIR/docker-compose.yml" up -d; then
    break
  fi

  if [[ "$attempt" -ge "$max_attempts" ]]; then
    echo "Failed to start stack after ${max_attempts} attempts."
    exit 1
  fi

  echo "Transient Docker error detected (common during large image pulls). Retrying in 5s..."
  attempt=$((attempt + 1))
  sleep 5
done

# Some Docker Desktop setups leave thanos-query in "Created" after the first wave.
"${COMPOSE_CMD[@]}" -f "$ROOT_DIR/docker-compose.yml" up -d thanos-query >/dev/null 2>&1 || true

echo "Stack started. Prometheus: http://localhost:9190 | Grafana: http://localhost:3100 | Jupyter: http://localhost:8898"
