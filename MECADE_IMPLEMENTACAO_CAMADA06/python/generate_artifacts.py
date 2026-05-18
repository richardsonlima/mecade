#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = {
    ROOT / 'audit/layer6/schemas/audit-event.schema.json': '{\n  "$schema": "http://json-schema.org/draft-07/schema#",\n  "title": "MECADEAuditEvent",\n  "type": "object",\n  "required": [\n    "event_id",\n    "parent_event_id",\n    "experiment_id",\n    "timestamp",\n    "layer",\n    "event_type",\n    "payload_hash",\n    "signature",\n    "trace_id"\n  ],\n  "properties": {\n    "event_id": {"type": "string"},\n    "parent_event_id": {"type": "string"},\n    "experiment_id": {"type": "string"},\n    "timestamp": {"type": "string"},\n    "layer": {"type": "string", "enum": ["L3", "L4", "L5", "L6", "L7"]},\n    "event_type": {"type": "string"},\n    "payload_hash": {"type": "string"},\n    "signature": {"type": "string"},\n    "trace_id": {"type": "string"}\n  }\n}\n',
    ROOT / 'audit/layer6/provenance/evidence-graph-model.yaml': 'nodes:\n  - ExperimentStarted\n  - AlertRaised\n  - LimitTriggered\n  - BlockExecuted\n  - RecoveryVerified\nedges:\n  - from: ExperimentStarted\n    to: AlertRaised\n  - from: AlertRaised\n    to: LimitTriggered\n  - from: LimitTriggered\n    to: BlockExecuted\nconstraints:\n  - every_node_must_have_event_id\n  - graph_must_be_acyclic_per_experiment\n',
    ROOT / 'audit/layer6/pipeline/offchain-onchain-contract.yaml': 'offchain:\n  storage: s3\n  payload_uri_pattern: s3://mecade-audit/{experiment_id}/{event_id}.json\n  hash_algorithm: sha256\nonchain:\n  anchor:\n    ledger: immudb\n    fields:\n      - event_id\n      - payload_hash\n      - signature\nconsistency_rule:\n  onchain_payload_hash_must_match_offchain\n',
    ROOT / 'audit/layer6/ledger/proof-contract.md': '# Proof contract\n\nCada evento auditavel deve possuir:\n- hash SHA-256 do payload completo\n- assinatura digital do emissor\n- ancoragem imutavel no ledger\n\nA verificacao deve reconstruir a cadeia causal end-to-end.\n',
    ROOT / 'audit/layer6/evaluation/audit-slo.yaml': 'slo:\n  ingestion_latency_p95_seconds: 2\n  completeness_ratio: 0.999\n  integrity_verification_success_ratio: 1.0\nalerts:\n  - id: audit_pipeline_delay\n    expr: audit_ingestion_latency_p95_seconds > 2\n',
    ROOT / 'audit/layer6/evaluation/overhead-study.md': '# Overhead study\n\n- Medir overhead de CPU e latencia com auditoria ligada/desligada.\n- Meta: overhead < 7% no caminho critico.\n- Reportar IC95% para diferencas observadas.\n',
    ROOT / 'audit/layer6/validation-protocol.md': '# Validation protocol - Layer 6\n\n1. Validar schema JSON e contrato offchain/onchain.\n2. Verificar trilha de proveniencia aciclica.\n3. Confirmar SLO de auditoria e estudo de overhead.\n4. Executar teste de adulteracao e detectar divergencia.\n',
}


def main() -> None:
    created = 0
    for path, content in TEMPLATES.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            created += 1

    print(f"Artifacts ensured for layer 6. New files created: {created}")


if __name__ == "__main__":
    main()
