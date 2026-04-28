#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LAYER1 = ROOT / "planning" / "layer1"
RISK_FILE = LAYER1 / "risk-prior.yaml"
BUDGET_FILE = LAYER1 / "chaos-budget-model.yaml"
OUTPUT = LAYER1 / "evidence" / "chaos-budget-computed.json"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    risk_prior = load_yaml(RISK_FILE).get("risk_prior", {})
    budget = load_yaml(BUDGET_FILE)

    selected_domain = budget["risk_aware_budget"]["selected_domain"]
    b0 = float(budget["risk_aware_budget"]["B0"])

    domain = risk_prior.get(selected_domain)
    if not domain:
        raise SystemExit(f"Domain '{selected_domain}' not found in risk prior.")

    impact_weight = float(domain["impact_weight"])
    p_critical = float(domain["p_critical_failure"])
    computed_budget = b0 * (1.0 - impact_weight * p_critical)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "service": budget.get("service"),
        "window": budget.get("window"),
        "formula": budget["risk_aware_budget"]["formula"],
        "B0": b0,
        "selected_domain": selected_domain,
        "impact_weight": impact_weight,
        "p_critical_failure": p_critical,
        "computed_budget": round(computed_budget, 4),
        "constraints": budget.get("constraints", {}),
        "integral_limit": budget.get("integral_limit", {}),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()
