#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / 'planning/layer3/detection-contract.yaml',
    ROOT / 'planning/layer3/models/risk-posterior-model.md',
    ROOT / 'observability/rules/alert-limit-block.rules.yaml',
    ROOT / 'observability/patterns/gray-failure-cep.yaml',
    ROOT / 'planning/layer3/false-positive-negative-tracker.md',
    ROOT / 'automation/block/block-decision-policy.yaml',
    ROOT / 'planning/layer3/validation-protocol.md',
]

REQUIRED_SERVICES = {
    'prometheus',
    'alertmanager',
    'grafana',
    'otel-collector',
    'loki',
    'tempo',
    'benthos',
    'argo-events',
    'jupyter',
}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def validate_yaml(path: Path) -> None:
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid YAML: {path} ({exc})")


def validate_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid JSON: {path} ({exc})")


def token_checks(path: Path, tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for token in tokens:
        if token.lower() not in text:
            fail(f"Missing token '{token}' in {path}")


def main() -> None:
    for f in REQUIRED_FILES:
        if not f.exists():
            fail(f"Missing required file: {f}")

    for f in REQUIRED_FILES:
        if f.suffix in {".yaml", ".yml"}:
            validate_yaml(f)
        elif f.suffix == ".json":
            validate_json(f)

    token_checks(ROOT / 'planning/layer3/models/risk-posterior-model.md', ['posterior', 'block'])
    token_checks(ROOT / 'planning/layer3/validation-protocol.md', ['cenario a', 'hard safety', 'gray failure'])

    compose_data = yaml.safe_load((ROOT / 'docker-compose.yml').read_text(encoding='utf-8'))
    compose_services = set((compose_data or {}).get('services', {}).keys())
    missing_services = sorted(REQUIRED_SERVICES - compose_services)
    if missing_services:
        fail(f"docker-compose missing required services: {', '.join(missing_services)}")

    print("[OK] Camada 3 valida e pronta.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[FAIL] Unexpected error: {exc}")
        sys.exit(1)
