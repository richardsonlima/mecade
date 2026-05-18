#!/usr/bin/env bash
set -euo pipefail

check_url() {
  local name="$1"
  local url="$2"
  local expected_code="$3"

  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 "$url" || true)"

  if [[ "$code" == "$expected_code" ]]; then
    echo "[OK] ${name}: HTTP ${code}"
  else
    echo "[FAIL] ${name}: expected HTTP ${expected_code}, got HTTP ${code}"
    return 1
  fi
}

main() {
  echo "Running smoke tests for Layer 1 Docker stack..."

  check_url "Prometheus" "http://localhost:9090/-/healthy" "200"
  check_url "Pushgateway" "http://localhost:9091/-/healthy" "200"
  check_url "Grafana" "http://localhost:3000/api/health" "200"
  check_url "Jupyter" "http://localhost:8888/api/status?token=mecade" "200"

  echo "All smoke tests passed."
}

main
