# HOWTO: Camada 6 (Auditoria Cientifica, Prova Criptografica e Governanca Deterministica) do MECADE

Eu escrevi este guia como roteiro E2E para implementar, testar e validar tecnicamente a auditoria da Camada 6 com prova verificavel.

Stack open source recomendada:

- Apache Kafka (buffer assíncrono e desacoplamento do caminho crítico)
- OpenTelemetry Collector (normalização e assinatura de eventos)
- MinIO ou S3-compatible (payload completo off-chain)
- Hyperledger Fabric ou immudb (âncora imutável de prova)
- Vault + Sigstore/Cosign (gestão criptográfica e assinatura)
- Prometheus + Grafana (SLO da auditoria)

## 1. O que torna esta Camada 6 inovadora

A inovação não é apenas "registrar no blockchain". É criar prova auditável com hipótese testável:

1. Modelo de evidência em duas camadas: conteúdo completo off-chain + prova compacta on-chain.
2. Grafo de proveniência (evento -> decisão -> ação -> efeito) com verificabilidade automatizada.
3. SLO da auditoria como sistema crítico independente (latência, completude, integridade).
4. Mensuração de overhead da auditoria no caminho crítico operacional.
5. Protocolo experimental para detectar adulteração, perda e reordenação de eventos.

## 2. Entregas obrigatórias da Camada 6

```bash
mkdir -p audit/layer6
mkdir -p audit/layer6/schemas
mkdir -p audit/layer6/provenance
mkdir -p audit/layer6/pipeline
mkdir -p audit/layer6/ledger
mkdir -p audit/layer6/evaluation
```

Arquivos obrigatorios:

- audit/layer6/schemas/audit-event.schema.json
- audit/layer6/provenance/evidence-graph-model.yaml
- audit/layer6/pipeline/offchain-onchain-contract.yaml
- audit/layer6/ledger/proof-contract.md
- audit/layer6/evaluation/audit-slo.yaml
- audit/layer6/evaluation/overhead-study.md
- audit/layer6/validation-protocol.md

Sem esses artefatos, a camada nao sustenta alegacao de imutabilidade e conformidade forte.

## 3. Implementacao passo a passo (formato banca)

### Passo 3.1 - Padronizar evento auditavel com identidade criptográfica

Exemplo em audit/layer6/schemas/audit-event.schema.json:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MECADEAuditEvent",
  "type": "object",
  "required": [
    "event_id",
    "parent_event_id",
    "experiment_id",
    "timestamp",
    "layer",
    "event_type",
    "payload_hash",
    "signature",
    "trace_id"
  ],
  "properties": {
    "event_id": { "type": "string" },
    "parent_event_id": { "type": "string" },
    "experiment_id": { "type": "string" },
    "timestamp": { "type": "string" },
    "layer": { "type": "string", "enum": ["L3", "L4", "L5", "L6", "L7"] },
    "event_type": { "type": "string" },
    "payload_uri": { "type": "string" },
    "payload_hash": { "type": "string" },
    "signature": { "type": "string" },
    "trace_id": { "type": "string" },
    "actor": { "type": "string" },
    "policy_version": { "type": "string" }
  }
}
```

Diferencial: permite reconstruir cadeia causal e autoria de decisão.

### Passo 3.2 - Definir modelo de grafo de evidência

Exemplo em audit/layer6/provenance/evidence-graph-model.yaml:

```yaml
nodes:
  - ExperimentStarted
  - AlertRaised
  - LimitTriggered
  - BlockExecuted
  - RecoveryVerified
  - ReleaseDecision
edges:
  - from: ExperimentStarted
    to: AlertRaised
  - from: AlertRaised
    to: LimitTriggered
  - from: LimitTriggered
    to: BlockExecuted
  - from: BlockExecuted
    to: RecoveryVerified
constraints:
  - every_node_must_have_event_id
  - every_edge_must_reference_parent_event_id
  - graph_must_be_acyclic_per_experiment
```

Diferencial: trilha forense consultável, não apenas sequência textual de logs.

### Passo 3.3 - Contrato off-chain/on-chain

Exemplo em audit/layer6/pipeline/offchain-onchain-contract.yaml:

```yaml
offchain:
  storage: minio
  object_key_pattern: "YYYY/MM/DD/{experiment_id}/{event_id}.json"
  required_metadata:
    - payload_hash
    - signature
    - trace_id
onchain:
  anchor:
    - event_id
    - payload_hash
    - timestamp
    - actor
rules:
  - reject_if_signature_invalid
  - reject_if_hash_missing
  - reconcile_if_ledger_unavailable
```

### Passo 3.4 - Definir contrato de prova imutável

Exemplo em audit/layer6/ledger/proof-contract.md:

```md
Operacoes:
- PutProof(event_id, payload_hash, parent_event_id, actor, timestamp)
- GetProof(event_id)
- VerifyProof(event_id, payload_hash)

Propriedades:
- event_id unico por experimento
- payload_hash imutavel apos commit
- parent_event_id obrigatorio para manter encadeamento causal
```

### Passo 3.5 - SLO da auditoria

Exemplo em audit/layer6/evaluation/audit-slo.yaml:

```yaml
audit_slo:
  ingest_latency_p95_ms_lte: 300
  chain_write_latency_p95_ms_lte: 500
  event_loss_rate_eq: 0
  proof_mismatch_rate_eq: 0
  max_reconciliation_lag_seconds: 120
```

Diferencial: auditoria passa a ter qualidade de serviço explicitamente monitorada.

### Passo 3.6 - Estudo de overhead no caminho crítico

Em audit/layer6/evaluation/overhead-study.md documente:

1. Tempo de decisão sem auditoria.
2. Tempo de decisão com auditoria assíncrona ativa.
3. Delta de latência e IC95%.
4. Critério de aceitabilidade (ex.: overhead <= 5%).

Sem isso, a alegação "não impacta caminho crítico" não é cientificamente sustentada.

## 4. Validacao de fato da Camada 6

A camada está validada quando prova integridade, completude e baixo impacto operacional com evidência quantitativa.

Checklist go/no-go:

1. Integridade ponta a ponta
- VerifyProof confirma hash off-chain para eventos amostrados e críticos.

2. Completude de proveniência
- Grafo de evidência sem lacunas para experimentos auditados.

3. Robustez a falha
- Ledger indisponível não gera perda de evento (apenas atraso de ancoragem).

4. Segurança criptográfica
- Evento sem assinatura válida é rejeitado e contabilizado.

5. Overhead controlado
- Impacto de latência no caminho crítico dentro do limite definido.

Se os 5 itens passarem, a Camada 6 está validada.

## 5. Protocolo de validacao experimental

Exemplo em audit/layer6/validation-protocol.md:

```md
# Protocolo de Validacao - Camada 6

Cenario A - Integridade nominal:
- publicar evento assinado
- persistir payload off-chain
- ancorar hash on-chain
- validar VerifyProof == true

Cenario B - Adulteracao de payload:
- alterar payload após persistencia
- recalcular hash
- validar mismatch detectado automaticamente

Cenario C - Ledger indisponivel:
- derrubar peer/orderer temporariamente
- validar backlog em Kafka
- validar reconciliacao total apos retorno

Cenario D - Reordenacao de eventos:
- publicar eventos fora de ordem
- validar reconstrução correta via parent_event_id

Cenario E - Medicao de overhead:
- comparar latencia de decisao com/sem auditoria
- avaliar delta e IC95%
```

## 6. Comandos uteis

```bash
# validar schema de evento (exemplo)
python audit/layer6/tools/validate_event_schema.py

# listar topicos kafka
kafka-topics.sh --bootstrap-server kafka:9092 --list

# consultar prova on-chain (exemplo)
peer chaincode query -C mecade-audit -n auditcc -c '{"Args":["GetProof","evt-001"]}'

# verificar objeto no minio
mc ls local/mecade-audit/

# observar SLO da auditoria
kubectl -n monitoring port-forward svc/prometheus-server 9090:80
```

## 7. Definicao de pronto (Definition of Done)

Camada 6 e considerada DONE quando:

- Contratos de evento, proveniência e prova estão versionados.
- Trilhas críticas possuem verificabilidade automatizada de integridade.
- Reconciliação após falha de ledger foi testada e aprovada.
- SLO da auditoria está em operação contínua.
- Estudo de overhead comprova impacto controlado no caminho crítico.

## 8. Evitar erros comuns

- Confundir imutabilidade com retenção de log comum.
- Não medir impacto da auditoria na latência operacional.
- Não provar completude da cadeia de evidência.
- Usar blockchain sem definir propriedade verificável de prova.
- Ignorar cenários de indisponibilidade e reordenação de eventos.

## 9. Fechamento tecnico

Nesta abordagem, a Camada 6 entrega auditoria com integridade verificavel, proveniencia completa e controle mensuravel de overhead no caminho critico.
