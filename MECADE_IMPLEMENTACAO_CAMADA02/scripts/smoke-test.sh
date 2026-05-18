#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "Neither 'docker compose' nor 'docker-compose' was found."
  exit 1
fi

check_http() {
  local name="$1"
  local url="$2"
  local expected="$3"
  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 "$url" || true)"
  if [[ "$code" == "$expected" ]]; then
    echo "[OK] ${name}: HTTP ${code}"
  else
    echo "[FAIL] ${name}: expected HTTP ${expected}, got HTTP ${code}"
    return 1
  fi
}

check_running() {
  local service="$1"
  local state
  state="$("${COMPOSE_CMD[@]}" -f "$ROOT_DIR/docker-compose.yml" ps --format json "$service" 2>/dev/null | tr -d '\n')"
  if echo "$state" | grep -qi '"State":"running"'; then
    echo "[OK] ${service}: running"
  else
    echo "[FAIL] ${service}: not running"
    return 1
  fi
}

check_command() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "[OK] ${name}: command succeeded"
  else
    echo "[FAIL] ${name}: command failed"
    return 1
  fi
}

echo "Running smoke tests for Layer 2 Docker stack..."

check_http "Prometheus" "http://localhost:9190/-/healthy" "200"
check_http "Grafana" "http://localhost:3100/api/health" "200"
check_http "OTel Collector metrics" "http://localhost:9188/metrics" "200"
check_http "Thanos Sidecar" "http://localhost:10902/-/healthy" "200"
check_http "Thanos Query" "http://localhost:10903/-/healthy" "200"
check_http "Jupyter" "http://localhost:8898/api/status?token=mecade" "200"

check_running "great-expectations"
check_command "Sloth CLI" "${COMPOSE_CMD[@]}" -f "$ROOT_DIR/docker-compose.yml" run -T --rm sloth version

echo "All smoke tests passed."
