#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="$ROOT_DIR/workspace/microservices-demo"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl not found. Install kubectl and rerun."
  exit 1
fi

if [[ ! -d "$REPO_DIR" ]]; then
  echo "microservices-demo not found. Run bootstrap script first."
  exit 1
fi

kubectl delete namespace online-boutique --ignore-not-found=true
kubectl create namespace online-boutique
kubectl apply -n online-boutique -f "$REPO_DIR/release/kubernetes-manifests.yaml"
kubectl wait --for=condition=Ready pods --all -n online-boutique --timeout=600s

echo "Reset completed."
