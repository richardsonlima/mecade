#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Useful commands for Layer 3:

1) Install dependencies
   bash scripts/install.sh

2) Run full layer3 E2E
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

7) One-command stack smoke test
   bash scripts/smoke-test.sh

Ports:
- Prometheus: 9290
- Alertmanager: 9293
- Grafana: 3200
- OTel collector: 9288
- Loki: 9300
- Tempo: 9301
- Benthos: 4295
- Jupyter: 8998
EOF
