#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "planning" / "layer1" / "evidence" / "power-analysis.json"
OUTPUT_MD = ROOT / "planning" / "layer1" / "power-analysis.md"


def repetitions_per_group(effect_size_d: float, alpha: float, power: float) -> int:
    if effect_size_d <= 0:
        raise ValueError("effect_size_d must be > 0")

    z_alpha = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    z_beta = NormalDist().inv_cdf(power)
    n = 2.0 * ((z_alpha + z_beta) / effect_size_d) ** 2
    return math.ceil(n)


def render_md(args: argparse.Namespace, d: float, n: int) -> str:
    return f"""# Analise de poder amostral

Parametros:
- baseline_mttr_segundos: {args.baseline_mttr}
- stddev_segundos: {args.stddev}
- efeito_minimo_percentual: {args.effect_pct * 100:.2f}%
- alpha: {args.alpha}
- poder_alvo: {args.power}

Resultados:
- efeito_absoluto_segundos: {args.baseline_mttr * args.effect_pct:.4f}
- efeito_padronizado_d: {d:.6f}
- repeticoes_minimas_por_cenario: {n}

Metodo:
- aproximacao normal para teste bilateral de diferenca de medias
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Power analysis for Layer 1 experiments")
    parser.add_argument("--baseline-mttr", type=float, default=120.0)
    parser.add_argument("--stddev", type=float, default=30.0)
    parser.add_argument("--effect-pct", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--power", type=float, default=0.8)
    args = parser.parse_args()

    effect_abs = args.baseline_mttr * args.effect_pct
    d = effect_abs / args.stddev
    n = repetitions_per_group(d, alpha=args.alpha, power=args.power)

    payload = {
        "baseline_mttr": args.baseline_mttr,
        "stddev": args.stddev,
        "effect_pct": args.effect_pct,
        "alpha": args.alpha,
        "power": args.power,
        "effect_abs_seconds": effect_abs,
        "effect_size_d": d,
        "repetitions_per_group": n,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(render_md(args, d, n), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nUpdated: {OUTPUT_MD}")
    print(f"Saved: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
