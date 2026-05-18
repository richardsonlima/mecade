#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="$ROOT_DIR/workspace"
REPO_DIR="$WORK_DIR/microservices-demo"

mkdir -p "$WORK_DIR"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl not found. Install kubectl and rerun."
  exit 1
fi

echo "[1/6] Preparing namespace online-boutique..."
kubectl get namespace online-boutique >/dev/null 2>&1 || kubectl create namespace online-boutique

echo "[2/6] Fetching Online Boutique manifests..."
if [[ ! -d "$REPO_DIR" ]]; then
  git clone https://github.com/GoogleCloudPlatform/microservices-demo.git "$REPO_DIR"
else
  git -C "$REPO_DIR" pull --ff-only
fi

echo "[3/6] Applying manifests..."
kubectl apply -n online-boutique -f "$REPO_DIR/release/kubernetes-manifests.yaml"

echo "[4/6] Waiting for pods readiness..."
kubectl wait --for=condition=Ready pods --all -n online-boutique --timeout=600s

echo "[5/6] Capturing reproducibility snapshot..."
kubectl get all -n online-boutique -o wide > "$ROOT_DIR/evidencias-campanha-viii-c/manifests/baseline/baseline_cluster_snapshot.txt"
kubectl get events -n online-boutique --sort-by=.lastTimestamp > "$ROOT_DIR/evidencias-campanha-viii-c/manifests/baseline/baseline_events_snapshot.txt"

echo "[6/6] Verifying essential services..."
kubectl get svc -n online-boutique
kubectl get deploy -n online-boutique

echo "Bootstrap completed."
