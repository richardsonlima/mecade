#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Useful commands for Layer 1:

1) Install dependencies
   bash scripts/install.sh

2) Run full layer1 E2E
   bash scripts/run-e2e.sh
   # compatibility alias
   bash scripts/run_e2e.sh

3) Validate required artifacts and gate
   bash scripts/validate.sh

4) Start observability stack
   bash scripts/docker-up.sh

5) Stop observability stack
   bash scripts/docker-down.sh

6) Smoke-test stack endpoints
   bash scripts/smoke-test.sh

7) Recompute power analysis with custom params
   python python/power_analysis.py --baseline-mttr 150 --stddev 40 --effect-pct 0.12 --power 0.85 --alpha 0.05
EOF
