#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LAYER2 = ROOT / "planning" / "layer2"


REQUIRED_FILES = [
    LAYER2 / "metric-dictionary.yaml",
    LAYER2 / "sli-slo-contract.yaml",
    LAYER2 / "rrindex-definition.md",
    LAYER2 / "data-quality" / "gx-suite.yaml",
    LAYER2 / "stats" / "decision-rule.md",
    LAYER2 / "validation-rules.yaml",
    ROOT / "observability" / "dashboards" / "layer2-scientific-overview.json",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def validate_yaml(path: Path) -> None:
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid YAML: {path} ({exc})")


def validate_dashboard_json(path: Path) -> None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid dashboard JSON: {path} ({exc})")

    if "title" not in payload:
        fail("Dashboard JSON missing required field: title")


def validate_metric_dictionary(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("metric-dictionary.yaml must be a mapping")

    metrics = data.get("metrics", [])
    if not isinstance(metrics, list) or not metrics:
        fail("metric-dictionary.yaml must have non-empty metrics list")

    required_keys = {"id", "definition", "formula", "unit", "uncertainty"}
    for metric in metrics:
        missing = required_keys - set(metric.keys())
        if missing:
            fail(f"Metric entry missing fields: {sorted(missing)}")


def validate_markdown_content(path: Path, required_tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for token in required_tokens:
        if token.lower() not in text:
            fail(f"Missing token '{token}' in {path}")


def main() -> None:
    for file in REQUIRED_FILES:
        if not file.exists():
            fail(f"Missing required file: {file}")

    validate_yaml(LAYER2 / "metric-dictionary.yaml")
    validate_yaml(LAYER2 / "sli-slo-contract.yaml")
    validate_yaml(LAYER2 / "data-quality" / "gx-suite.yaml")
    validate_yaml(LAYER2 / "validation-rules.yaml")

    validate_metric_dictionary(LAYER2 / "metric-dictionary.yaml")
    validate_dashboard_json(ROOT / "observability" / "dashboards" / "layer2-scientific-overview.json")

    validate_markdown_content(
        LAYER2 / "rrindex-definition.md",
        ["rrindex", "w1", "w2", "w3", "w4"],
    )
    validate_markdown_content(
        LAYER2 / "stats" / "decision-rule.md",
        ["h0", "h1", "ic95", "efeito"],
    )

    print("[OK] Camada 2 valida e pronta para gate cientifico.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] Unexpected error: {exc}")
        sys.exit(1)
