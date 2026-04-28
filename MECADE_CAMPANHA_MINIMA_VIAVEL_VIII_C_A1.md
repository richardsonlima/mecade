# HOWTO: Execucao da Campanha Minima Viavel (Secao VIII-C) para Tier A1

## Objetivo
Neste guia eu descrevo, de ponta a ponta, como executar a campanha minima viavel definida na Secao VIII-C com protocolo A/B pareado (Baseline Reativo vs MECADE), de forma reproduzivel e auditavel.

Quando concluida com evidencias consistentes, esta campanha posiciona o trabalho diretamente no tier A1.

## Ambiente alvo da campanha
A campanha minima viavel desta secao deve ser executada usando o Google Online Boutique (microservices-demo) em Kubernetes, conforme proposto no artigo.

## Escopo minimo obrigatorio
1. Dois bracos de avaliacao:
   - Braco A: Baseline Reativo
   - Braco B: MECADE
2. Tres cenarios de falha:
   - Latencia induzida
   - Timeout intermitente (gray failure)
   - Pod kill
3. Mesmas condicoes experimentais para A e B:
   - Mesmo workload
   - Mesma janela temporal
   - Mesma topologia e versoes
4. Repeticoes independentes com randomizacao da ordem A/B.
5. Coleta de metricas:
   - P95 e P99
   - TSR
   - MTTR
   - RTO
   - Taxa de falsos bloqueios
6. Registro temporal de ALERT/LIMIT/BLOCK + artefatos da Camada 6.

## Criterio de sucesso para tier A1
Considerar evidencia favoravel quando, com consistencia estatistica entre repeticoes:
1. MTTR e RTO do braco MECADE forem menores que no baseline.
2. Houver amortecimento da variabilidade de latencia (P95/P99) no braco MECADE.
3. A taxa de falsos bloqueios permanecer abaixo do limiar operacional definido no Safety Envelope.
4. Toda decisao ALERT/LIMIT/BLOCK estiver rastreavel (timestamp, contexto, resultado, hash/assinatura quando aplicavel).

## Pre-requisitos
1. Cluster Kubernetes funcional.
2. Online Boutique implantado e estavel.
3. Stack de observabilidade ativa (minimo: metricas e logs).
4. Definicao explicita de Safety Envelope e Chaos Budget (Camada 1).
5. Politicas de decisao ALERT/LIMIT/BLOCK versionadas.
6. Repositorio de evidencias criado (pasta local, bucket ou ambos).

## Instalacao do Google Online Boutique (Kubernetes)

### Passo 0: Preparar namespace
```bash
kubectl create namespace online-boutique
```

### Passo 1: Obter os manifests do projeto
```bash
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
```

### Passo 2: Implantar o Online Boutique
```bash
kubectl apply -n online-boutique -f microservices-demo/release/kubernetes-manifests.yaml
```

### Passo 3: Aguardar pods ficarem prontos
```bash
kubectl get pods -n online-boutique
kubectl wait --for=condition=Ready pods --all -n online-boutique --timeout=600s
```

### Passo 4: Validar servicos essenciais
```bash
kubectl get svc -n online-boutique
kubectl get deploy -n online-boutique
```

### Passo 5: Acessar a aplicacao localmente (validacao rapida)
```bash
kubectl port-forward -n online-boutique svc/frontend-external 8080:80
```

Abra no navegador:
```text
http://localhost:8080
```

### Passo 6: Gerar carga para baseline da campanha
Opcao A (usar loadgenerator do proprio Online Boutique):
```bash
kubectl get pod -n online-boutique -l app=loadgenerator
kubectl logs -n online-boutique -l app=loadgenerator --tail=100
```

Opcao B (gerador externo): usar k6/locust com perfil fixo e versionado em `workload.json`.

### Passo 7: Snapshot inicial para reprodutibilidade
```bash
kubectl get all -n online-boutique -o wide > baseline_cluster_snapshot.txt
kubectl get events -n online-boutique --sort-by=.lastTimestamp > baseline_events_snapshot.txt
```

## Reset rapido do ambiente (opcional)
Use quando precisar limpar o ambiente entre baterias de execucao:

```bash
kubectl delete namespace online-boutique
kubectl create namespace online-boutique
kubectl apply -n online-boutique -f microservices-demo/release/kubernetes-manifests.yaml
kubectl wait --for=condition=Ready pods --all -n online-boutique --timeout=600s
```

## Estrutura sugerida de evidencias
Crie a seguinte estrutura para garantir rastreabilidade:

```text
evidencias-campanha-viii-c/
  manifests/
    baseline/
    mecade/
    chaos/
  execucoes/
    run-001/
      metadata.json
      workload.json
      eventos-alert-limit-block.jsonl
      metricas-series.csv
      resumo.md
    run-002/
    ...
  analise/
    comparativo_ab.csv
    testes_estatisticos.md
    consolidado_final.md
```

## Protocolo operacional (passo a passo)

### Passo 1: Congelar baseline experimental
1. Fixe versoes de imagens, manifests e configuracoes.
2. Defina workload padrao (RPS/concurrency/duracao).
3. Defina janelas de observacao (ex.: warm-up, injecao, recuperacao).
4. Registre tudo em `metadata.json`.

Checklist:
- [ ] Mesma topologia para A e B
- [ ] Mesma carga para A e B
- [ ] Mesmos limites de observacao para A e B

### Passo 2: Definir desenho A/B pareado
1. Para cada cenario, execute pares A e B sob mesmas condicoes.
2. Randomize a ordem de execucao por repeticao (ex.: B-A, A-B, B-A...).
3. Use numero minimo de repeticoes predefinido (recomendado: >= 10 por cenario).

Exemplo de matriz:

```text
Cenario latencia:
  rep01 -> B-A
  rep02 -> A-B
  rep03 -> B-A
...
```

### Passo 3: Executar cenario 1 (latencia induzida)
1. Inicie coleta de metricas.
2. Injete latencia no servico alvo.
3. Registre ALERT/LIMIT/BLOCK com timestamp.
4. Encerre injecao e acompanhe recuperacao ate steady state.
5. Salve artefatos da repeticao.

Dados minimos por repeticao:
- P95/P99 ao longo do tempo
- TSR por janela
- MTTR observado
- RTO atingido/nao atingido
- Numero de bloqueios e falsos bloqueios

### Passo 4: Executar cenario 2 (timeout intermitente)
Repita o mesmo protocolo do Passo 3, alterando apenas o tipo de falha.

### Passo 5: Executar cenario 3 (pod kill)
Repita o mesmo protocolo do Passo 3, alterando apenas o tipo de falha.

### Passo 6: Coletar trilha de auditoria (Camada 6)
Para cada repeticao, registrar no minimo:
1. ID da execucao
2. Cenario e parametros de falha
3. Politica/versao ALERT/LIMIT/BLOCK
4. Sequencia de decisoes e timestamps
5. Resultado (aceitavel/degradado/critico)
6. Hash/assinatura do artefato final (quando aplicavel)

## Modelo de metadata.json (exemplo)

```json
{
  "run_id": "run-001",
  "cenario": "latencia_induzida",
  "ordem_bracos": "B-A",
  "workload": {
    "rps": 200,
    "duracao_seg": 900
  },
  "janelas": {
    "warmup_seg": 180,
    "injecao_seg": 300,
    "recuperacao_seg": 420
  },
  "politica_mecade": {
    "alert": "v1.2",
    "limit": "v1.2",
    "block": "v1.2"
  },
  "safety_envelope_ref": "SE-2026-04",
  "chaos_budget_ref": "CB-2026-04"
}
```

## Modelo de eventos-alert-limit-block.jsonl (exemplo)

```jsonl
{"ts":"2026-04-19T14:00:10Z","run_id":"run-001","evento":"ALERT","metrica":"p99","valor":420,"limiar":350}
{"ts":"2026-04-19T14:01:02Z","run_id":"run-001","evento":"LIMIT","integral_desvio":1.31,"budget":1.20}
{"ts":"2026-04-19T14:01:03Z","run_id":"run-001","evento":"BLOCK","acao":"abort_injection","resultado":"safe_state_transition"}
```

## Consolidacao e analise
1. Monte tabela comparativa A/B por cenario e repeticao.
2. Calcule diferencas relativas (MECADE vs baseline):
   - Delta MTTR
   - Delta RTO
   - Delta variabilidade P95/P99
   - Delta TSR
3. Reporte taxa de falsos bloqueios.
4. Aplique analise estatistica apropriada (intervalo de confianca + teste nao parametrico quando necessario).
5. Gere conclusao objetiva de aceitacao/reprovacao por criterio.

## Template de tabela final (resumo)

```text
| Cenario              | Repeticoes | MTTR Baseline | MTTR MECADE | RTO Baseline | RTO MECADE | Variabilidade P99 (A->B) | Falsos bloqueios (B) | Resultado |
|----------------------|------------|---------------|-------------|--------------|------------|---------------------------|----------------------|-----------|
| Latencia induzida    | 10         | ...           | ...         | ...          | ...        | ...                       | ...                  | ...       |
| Timeout intermitente | 10         | ...           | ...         | ...          | ...        | ...                       | ...                  | ...       |
| Pod kill             | 10         | ...           | ...         | ...          | ...        | ...                       | ...                  | ...       |
```

## Checklist final de submissao (tier A1)
- [ ] Protocolo A/B pareado executado nos 3 cenarios
- [ ] Randomizacao de ordem A/B documentada
- [ ] Repeticoes independentes concluidas
- [ ] Metricas P95/P99, TSR, MTTR, RTO coletadas
- [ ] Taxa de falsos bloqueios reportada
- [ ] Trilhas ALERT/LIMIT/BLOCK registradas com timestamp
- [ ] Artefatos de auditoria (Camada 6) consolidados
- [ ] Analise estatistica e conclusao objetiva publicadas
- [ ] Todos os artefatos versionados e reproduziveis
