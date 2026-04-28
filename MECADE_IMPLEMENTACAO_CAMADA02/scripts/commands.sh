#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Useful commands for Layer 2:

1) Install dependencies
   bash scripts/install.sh

2) Run full layer2 E2E
   bash scripts/run-e2e.sh
   # compatibility alias
   bash scripts/run_e2e.sh

3) Validate required artifacts and gate
   bash scripts/validate.sh

4) Start observability stack
   bash scripts/docker-up.sh

5) Stop observability stack
   bash scripts/docker-down.sh

6) Smoke-test stack endpoints and services
   bash scripts/smoke-test.sh

7) Recompute RRIndex and inference evidence
   bash scripts/generate-evidence.sh
EOF
