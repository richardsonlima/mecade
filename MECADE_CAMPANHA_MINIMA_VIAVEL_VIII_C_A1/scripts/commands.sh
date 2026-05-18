#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Useful commands for Campanha VIII-C Tier A1:

1) Install dependencies
   bash scripts/install.sh

2) Bootstrap Online Boutique in Kubernetes
   bash scripts/bootstrap-online-boutique.sh

3) Run full campaign E2E checks
   bash scripts/run-e2e.sh
   bash scripts/run_e2e.sh

4) Validate campaign compliance
   bash scripts/validate.sh

5) Start Docker stack (Online Boutique + observability)
   bash scripts/docker-up.sh

6) Stop observability stack
   bash scripts/docker-down.sh

7) Reset Online Boutique namespace
   bash scripts/reset-online-boutique.sh
EOF
