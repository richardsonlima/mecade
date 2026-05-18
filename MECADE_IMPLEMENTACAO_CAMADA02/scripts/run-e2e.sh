#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$ROOT_DIR/.venv" ]]; then
  echo "Virtual env not found. Run: bash scripts/install.sh"
  exit 1
fi

# shellcheck source=/dev/null
source "$ROOT_DIR/.venv/bin/activate"

echo "[1/4] Ensuring required artifacts..."
python "$ROOT_DIR/python/generate_artifacts.py"

echo "[2/4] Computing RRIndex..."
python "$ROOT_DIR/python/compute_rrindex.py"

echo "[3/4] Running non-regression inference..."
python "$ROOT_DIR/python/run_inference.py"

echo "[4/4] Validating scientific acceptance gate..."
python "$ROOT_DIR/python/validate_layer2.py"

echo
echo "E2E Camada 2 completed successfully."
