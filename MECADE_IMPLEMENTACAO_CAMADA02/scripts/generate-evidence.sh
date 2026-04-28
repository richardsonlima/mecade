#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Python not found. Install Python 3.10+ or run bash scripts/install.sh first."
  exit 1
fi

"$PYTHON_BIN" "$ROOT_DIR/python/compute_rrindex.py"
"$PYTHON_BIN" "$ROOT_DIR/python/run_inference.py"
"$PYTHON_BIN" "$ROOT_DIR/python/validate_layer2.py"

if command -v dvc >/dev/null 2>&1; then
  dvc add "$ROOT_DIR/planning/layer2/evidence/"
  echo "DVC tracking updated for evidence directory."
else
  echo "DVC not found. Evidence generated but not tracked by DVC."
fi
