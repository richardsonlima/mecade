#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/3] Checking Python..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.10+ and rerun."
  exit 1
fi

echo "[2/3] Creating virtual environment..."
python3 -m venv "$ROOT_DIR/.venv"
# shellcheck source=/dev/null
source "$ROOT_DIR/.venv/bin/activate"

echo "[3/3] Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r "$ROOT_DIR/requirements.txt"

echo "Install completed. Activate with: source .venv/bin/activate"
