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

echo "[2/4] Computing risk-aware chaos budget..."
python "$ROOT_DIR/python/compute_chaos_budget.py"

echo "[3/4] Running sample power analysis..."
python "$ROOT_DIR/python/power_analysis.py" \
  --baseline-mttr 120 \
  --stddev 30 \
  --effect-pct 0.15 \
  --power 0.8 \
  --alpha 0.05

echo "[4/4] Validating scientific acceptance gate..."
python "$ROOT_DIR/python/validate_layer1.py"

echo
echo "E2E Camada 1 completed successfully."
