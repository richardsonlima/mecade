#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
else
  echo "Python not found."
  exit 1
fi

"$PYTHON_BIN" "$ROOT_DIR/python/run_layer4_analysis.py"
"$PYTHON_BIN" "$ROOT_DIR/python/validate_layer4.py"

if command -v dvc >/dev/null 2>&1; then
  dvc add "$ROOT_DIR/chaos/layer4"
  echo "DVC tracking updated for chaos/layer4."
else
  echo "DVC not found. Evidence generated but not tracked by DVC."
fi
