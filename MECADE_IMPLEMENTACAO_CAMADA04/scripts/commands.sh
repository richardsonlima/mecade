#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Useful commands for Layer 4:

1) Install dependencies
   bash scripts/install.sh

2) Run full layer4 E2E
   bash scripts/run-e2e.sh
   bash scripts/run_e2e.sh

3) Validate required artifacts
   bash scripts/validate.sh

4) Start observability stack
   bash scripts/docker-up.sh

5) Stop observability stack
   bash scripts/docker-down.sh

6) Generate analysis evidence
   bash scripts/generate-evidence.sh

Ports:
- Prometheus: 9390
- Grafana: 3300
- OTel collector: 9388
- Jupyter: 9098
EOF
