#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / 'audit/layer6/schemas/audit-event.schema.json',
    ROOT / 'audit/layer6/provenance/evidence-graph-model.yaml',
    ROOT / 'audit/layer6/pipeline/offchain-onchain-contract.yaml',
    ROOT / 'audit/layer6/ledger/proof-contract.md',
    ROOT / 'audit/layer6/evaluation/audit-slo.yaml',
    ROOT / 'audit/layer6/evaluation/overhead-study.md',
    ROOT / 'audit/layer6/validation-protocol.md',
]


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

    token_checks(ROOT / 'audit/layer6/ledger/proof-contract.md', ['hash', 'assinatura'])
    token_checks(ROOT / 'audit/layer6/validation-protocol.md', ['proveniencia', 'adulteracao'])

    print("[OK] Camada 6 valida e pronta.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[FAIL] Unexpected error: {exc}")
        sys.exit(1)
