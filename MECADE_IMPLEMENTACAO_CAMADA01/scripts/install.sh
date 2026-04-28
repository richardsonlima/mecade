#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/4] Checking Python..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.10+ and rerun."
  exit 1
fi

echo "[2/4] Creating virtual environment..."
python3 -m venv "$ROOT_DIR/.venv"
# shellcheck source=/dev/null
source "$ROOT_DIR/.venv/bin/activate"

echo "[3/4] Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r "$ROOT_DIR/requirements.txt"

echo "[4/4] Checking Docker (optional for local-only mode)..."
if command -v docker >/dev/null 2>&1; then
  echo "Docker found: $(docker --version)"
  if docker compose version >/dev/null 2>&1; then
    echo "Compose found: $(docker compose version | head -n 1)"
  elif command -v docker-compose >/dev/null 2>&1; then
    echo "Compose found: $(docker-compose --version)"
  else
    echo "Warning: Compose not found. Docker stack scripts will not run until compose is installed/enabled."
  fi
else
  echo "Docker not found. You can still run local planning scripts without Docker."
fi

echo
echo "Install completed. Activate env with:"
echo "source .venv/bin/activate"
