#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LAYER1 = ROOT / "planning" / "layer1"


REQUIRED_FILES = [
    LAYER1 / "steady-state.openslo.yaml",
    LAYER1 / "fmea-causal.csv",
    LAYER1 / "risk-prior.yaml",
    LAYER1 / "chaos-budget-model.yaml",
    LAYER1 / "hypotheses-causal.md",
    LAYER1 / "power-analysis.md",
    LAYER1 / "prereg" / "experiment-protocol.md",
    LAYER1 / "acceptance-gate.yaml",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def validate_yaml(path: Path) -> None:
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid YAML: {path} ({exc})")


def validate_fmea(path: Path) -> None:
    required_cols = {
        "failure_mode",
        "cause",
        "pathway",
        "observable_effect",
        "severity",
        "occurrence",
        "detection",
        "rpn",
        "owner",
    }
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            fail("FMEA CSV is empty")
        missing = required_cols - set(reader.fieldnames)
        if missing:
            fail(f"FMEA CSV missing columns: {sorted(missing)}")
        rows = list(reader)
        if not rows:
            fail("FMEA CSV has no data rows")


def validate_markdown_content(path: Path, required_tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for token in required_tokens:
        if token.lower() not in text:
            fail(f"Missing token '{token}' in {path}")


def main() -> None:
    for file in REQUIRED_FILES:
        if not file.exists():
            fail(f"Missing required file: {file}")

    validate_yaml(LAYER1 / "steady-state.openslo.yaml")
    validate_yaml(LAYER1 / "risk-prior.yaml")
    validate_yaml(LAYER1 / "chaos-budget-model.yaml")
    validate_yaml(LAYER1 / "acceptance-gate.yaml")
    validate_fmea(LAYER1 / "fmea-causal.csv")

    validate_markdown_content(
        LAYER1 / "hypotheses-causal.md",
        ["hipotese causal", "metrica primaria", "criterio de sucesso"],
    )
    validate_markdown_content(
        LAYER1 / "prereg" / "experiment-protocol.md",
        ["hipoteses", "metrica", "metodo estatistico", "rollback"],
    )
    validate_markdown_content(
        LAYER1 / "power-analysis.md",
        ["alpha", "poder", "repeticoes"],
    )

    print("[OK] Camada 1 valida e pronta para gate cientifico.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] Unexpected error: {exc}")
        sys.exit(1)
