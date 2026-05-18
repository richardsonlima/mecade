#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$ROOT_DIR/.venv" ]]; then
  echo "Virtual env not found. Run: bash scripts/install.sh"
  exit 1
fi

# shellcheck source=/dev/null
source "$ROOT_DIR/.venv/bin/activate"

echo "[1/3] Ensuring required artifacts..."
python "$ROOT_DIR/python/generate_artifacts.py"

echo "[2/3] Running layer 5 analysis..."
python "$ROOT_DIR/python/run_layer5_analysis.py"

echo "[3/3] Validating required artifacts..."
python "$ROOT_DIR/python/validate_layer5.py"

echo "E2E Camada 5 completed successfully."
