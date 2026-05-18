#!/usr/bin/env bash
set -euo pipefail

# Compatibility wrapper for users typing underscore instead of hyphen.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash "$ROOT_DIR/scripts/run-e2e.sh"
