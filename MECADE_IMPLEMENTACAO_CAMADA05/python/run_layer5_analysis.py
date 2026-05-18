#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / 'cicd/layer5'
EVIDENCE_DIR = ARTIFACT_ROOT / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

summary = {
    "layer": "L5",
    "generated_at_utc": datetime.now(UTC).isoformat(),
    "artifact_root": str(ARTIFACT_ROOT.relative_to(ROOT)),
    "required_files_detected": sum(1 for _ in ARTIFACT_ROOT.rglob('*') if _.is_file()),
    "status": "baseline-analysis-generated"
}

out = EVIDENCE_DIR / "analysis-summary.json"
out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"Layer 5 analysis summary written to {out}")
