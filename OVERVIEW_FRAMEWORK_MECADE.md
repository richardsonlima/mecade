# OVERVIEW DO FRAMEWORK MECADE (MEDADE)

Este documento apresenta uma visao integrada do framework proposto, conectando as 7 camadas em um fluxo unico, com diagramas em varios niveis para facilitar entendimento tecnico, academico e de banca.

## 1. Visao geral em uma frase

O MECADE e um ciclo cibernetico de dependabilidade que transforma: planejamento cientifico -> medicao robusta -> deteccao inteligente -> execucao controlada -> governanca de release -> auditoria verificavel -> aprendizado causal continuo.

## 2. Mapa rapido das camadas

| Camada | Nome | Pergunta central | Saida principal |
|---|---|---|---|
| 1 | Planejamento Cientifico | O que testar e com qual rigor? | Hipoteses causais + Chaos Budget por risco |
| 2 | Metrologia Cientifica | Como medir com validade e incerteza? | SLI/SLO formal + RRIndex + regras de decisao |
| 3 | Deteccao Cientifica | Quando agir e com qual evidencia? | ALERT/LIMIT/BLOCK com risco posterior |
| 4 | Execucao Experimental | Como injetar falha com seguranca e causalidade? | Campanhas progressivas + ablation + efeito |
| 5 | Governanca de CI/CD | Quando promover release com evidencia? | Release gate multiobjetivo e auditavel |
| 6 | Auditoria Cientifica | Como provar integridade e proveniencia? | Prova criptografica off-chain/on-chain |
| 7 | Aprendizado Causal | Como evoluir politica sem regressao? | Upgrade/rollback de politica com efeito causal |

## 3. Diagrama de contexto (nivel executivo)

```mermaid
flowchart LR
  A[Ambiente Distribuido Critico] --> B[MECADE]
  B --> C[Resiliencia Operacional]
  B --> D[Conformidade e Auditoria]
  B --> E[Evolucao Continua de Politicas]
```

## 4. Diagrama macro das 7 camadas (nivel arquitetural)

```mermaid
flowchart TB
  L1[Camada 1<br/>Planejamento Cientifico]
  L2[Camada 2<br/>Metrologia Cientifica]
  L3[Camada 3<br/>Deteccao Cientifica]
  L4[Camada 4<br/>Execucao Experimental]
  L5[Camada 5<br/>Governanca CI/CD]
  L6[Camada 6<br/>Auditoria Cientifica]
  L7[Camada 7<br/>Aprendizado Causal]

  L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7
  L7 -. Feedback de politica e risco .-> L1
```

## 5. Fluxo ponta a ponta de artefatos (nivel operacional)

```mermaid
flowchart LR
  A1[Hipoteses + Budget + Pre-registro<br/>Camada 1]
  A2[SLI/SLO + RRIndex + Qualidade de dados<br/>Camada 2]
  A3[Alertas e risco posterior<br/>Camada 3]
  A4[Falhas controladas + ablation<br/>Camada 4]
  A5[Gate de release multiobjetivo<br/>Camada 5]
  A6[Prova criptografica e grafo de evidencias<br/>Camada 6]
  A7[Tuning de politica com causalidade<br/>Camada 7]

  A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7 --> A1
```

## 6. Fluxo de dados e controle (nivel engenharia)

```mermaid
flowchart TB
  subgraph Observabilidade
    M[Metricas]
    T[Traces]
    G[Logs]
  end

  subgraph Decisao
    D1[Detector ALERT/LIMIT]
    D2[Risco Posterior]
    D3[Politica BLOCK]
  end

  subgraph Execucao
    X1[Fault Runner]
    X2[Rollback Safe State]
  end

  subgraph Auditoria
    O1[Store Off-chain]
    O2[Prova On-chain]
  end

  subgraph Aprendizado
    P1[Dataset Historico]
    P2[Otimizacao de Politica]
    P3[Promover ou Reverter]
  end

  M --> D1
  T --> D1
  G --> D1
  D1 --> D2 --> D3 --> X1
  X1 --> X2
  X1 --> O1 --> O2
  O2 --> P1
  M --> P1
  P1 --> P2 --> P3
  P3 -. Atualiza thresholds .-> D1
```

## 7. Sequencia temporal de uma campanha (nivel processo)

```mermaid
sequenceDiagram
  participant C1 as Camada 1
  participant C2 as Camada 2
  participant C3 as Camada 3
  participant C4 as Camada 4
  participant C5 as Camada 5
  participant C6 as Camada 6
  participant C7 as Camada 7

  C1->>C2: Entrega baseline, hipoteses e budget
  C2->>C3: Entrega metricas, SLO e regra estatistica
  C3->>C4: Entrega ALERT/LIMIT/BLOCK com risco
  C4->>C5: Entrega resultados de experimento
  C5->>C6: Entrega decisao de release e evidencias
  C6->>C7: Entrega prova de integridade e proveniencia
  C7->>C1: Entrega policy refinada e novo plano
```

## 8. Maquina de estados do ciclo de decisao

```mermaid
stateDiagram-v2
  [*] --> Planejar
  Planejar --> Medir
  Medir --> Detectar
  Detectar --> Executar
  Executar --> Gate
  Gate --> Auditar
  Auditar --> Aprender
  Aprender --> Planejar

  Detectar --> Bloquear: risco alto ou limite duro
  Bloquear --> Auditar
```

## 9. Arvore de decisao para release

```mermaid
flowchart TD
  Q1{SLO passou?}
  Q2{Nao regressao estatistica?}
  Q3{Risk score <= limite?}
  Q4{Seguranca preservada?}
  OK[Promover release]
  NO[Bloquear e abrir rollback]

  Q1 -- Nao --> NO
  Q1 -- Sim --> Q2
  Q2 -- Nao --> NO
  Q2 -- Sim --> Q3
  Q3 -- Nao --> NO
  Q3 -- Sim --> Q4
  Q4 -- Nao --> NO
  Q4 -- Sim --> OK
```

## 10. Diagrama de niveis de evidencia

```mermaid
flowchart LR
  E1[Nivel 1<br/>Observacao]
  E2[Nivel 2<br/>Reproducao]
  E3[Nivel 3<br/>Efeito Estatistico]
  E4[Nivel 4<br/>Efeito Causal]
  E5[Nivel 5<br/>Governanca Auditavel]

  E1 --> E2 --> E3 --> E4 --> E5
```

## 11. Como as camadas se interligam na pratica

1. A Camada 1 define o contrato cientifico do experimento.
2. A Camada 2 transforma contrato em medicao valida.
3. A Camada 3 converte medicao em decisao em tempo real.
4. A Camada 4 executa falha controlada para gerar evidencia.
5. A Camada 5 decide promocao de release por gate multiobjetivo.
6. A Camada 6 ancora e prova integridade de toda decisao.
7. A Camada 7 aprende causalmente e atualiza politica.

## 12. Diferencial do modelo proposto

O diferencial do framework nao e ferramenta isolada. E a integracao formal entre:

- controle deterministico de seguranca,
- inferencia estatistica e causal,
- experimentacao reproduzivel,
- e governanca criptograficamente verificavel.

Isso permite defender em banca que o modelo evolui de PoC para um sistema de engenharia cientifica de dependabilidade.

## 13. Checklist

Roteiro de implementacao, teste e validacao de cada camada:

1. Mostrar o diagrama macro das 7 camadas.
2. Mostrar um fluxo ponta a ponta de artefatos.
3. Mostrar a sequencia temporal de uma campanha real.
4. Mostrar a arvore de decisao de release.
5. Mostrar o nivel de evidencia alcancado (1 a 5).
