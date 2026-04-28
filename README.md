# MECADE

Modelo de Engenharia do Caos para Avaliacao da Garantia de Dependabilidade em Sistemas Criticos Distribuidos.

## Visao Geral

O MECADE e um framework de engenharia do caos orientado a dependabilidade, projetado para ambientes distribuidos de alta criticidade (como financeiro, aeroespacial, energia e infraestrutura essencial).

A proposta central e transformar a experimentacao de falhas de uma pratica ad hoc em um ciclo cibernetico estruturado, com:

- controle deterministico de risco operacional
- validacao empirica de resiliencia sob estresse controlado
- trilha de auditoria verificavel para conformidade e forense

## Problema que o MECADE endereca

Abordagens tradicionais costumam tratar, de forma separada:

- observabilidade
- execucao de caos
- governanca e auditoria

Em sistemas criticos, essa fragmentacao dificulta:

- reduzir MTTR e RTO de forma previsivel
- detectar falhas cinzentas (gray failures) com antecedencia
- sustentar rastreabilidade imutavel de decisoes e recuperacoes

## Proposta do Modelo

O MECADE organiza a operacao em 7 camadas funcionais, formando um loop fechado de melhoria continua:

1. Planejamento cientifico (hipoteses, FMEA, chaos budget)
2. Objetivos e metricas (SLOs, latencia, erro, MTTR, RTO, RRIndex)
3. Deteccao automatica (ALERT e LIMIT)
4. Execucao tecnica de falhas e mitigacao (incluindo BLOCK)
5. Integracao com pipelines (Resilience as Code)
6. Auditoria continua (proveniencia e integridade)
7. Feedback e evolucao (ajuste de limiares, politicas e conhecimento)

Esse desenho combina rigor metodologico com operacao pratica em cloud-native/microsservicos.

## Diferenciais tecnicos

- Governanca axiomatica com ALERT, LIMIT e BLOCK
- Safety Envelope formal para conter blast radius
- Integracao nativa com experimentacao e observabilidade
- Arquitetura de auditoria com foco em rastreabilidade
- Evolucao continua orientada por evidencia

## Evidencias e escopo cientifico

No estado atual, o MECADE apresenta prova de conceito em ambiente controlado. Os resultados devem ser interpretados como evidencias preliminares, com consolidacao prevista via campanhas adicionais em ambientes representativos.

## Estrutura deste repositorio

### Mapeamento de guias e implementacao/validacao E2E (Camadas 01 a 07)

| Camada | Guia (MD) | Pasta de implementacao/validacao E2E | Status atual |
|---|---|---|---|
| 01 | [MECADE_IMPLEMENTACAO_CAMADA01.md](MECADE_IMPLEMENTACAO_CAMADA01.md) | [MECADE_IMPLEMENTACAO_CAMADA01](MECADE_IMPLEMENTACAO_CAMADA01) | Implementada e validada E2E |
| 02 | [MECADE_IMPLEMENTACAO_CAMADA02.md](MECADE_IMPLEMENTACAO_CAMADA02.md) | [MECADE_IMPLEMENTACAO_CAMADA02](MECADE_IMPLEMENTACAO_CAMADA02) | Implementada e validada E2E |
| 03 | [MECADE_IMPLEMENTACAO_CAMADA03.md](MECADE_IMPLEMENTACAO_CAMADA03.md) | [MECADE_IMPLEMENTACAO_CAMADA03](MECADE_IMPLEMENTACAO_CAMADA03) | Implementada e validada E2E |
| 04 | [MECADE_IMPLEMENTACAO_CAMADA04.md](MECADE_IMPLEMENTACAO_CAMADA04.md) | [MECADE_IMPLEMENTACAO_CAMADA04](MECADE_IMPLEMENTACAO_CAMADA04) | Implementada e validada E2E |
| 05 | [MECADE_IMPLEMENTACAO_CAMADA05.md](MECADE_IMPLEMENTACAO_CAMADA05.md) | [MECADE_IMPLEMENTACAO_CAMADA05](MECADE_IMPLEMENTACAO_CAMADA05) | Implementada e validada E2E |
| 06 | [MECADE_IMPLEMENTACAO_CAMADA06.md](MECADE_IMPLEMENTACAO_CAMADA06.md) | [MECADE_IMPLEMENTACAO_CAMADA06](MECADE_IMPLEMENTACAO_CAMADA06) | Implementada e validada E2E |
| 07 | [MECADE_IMPLEMENTACAO_CAMADA07.md](MECADE_IMPLEMENTACAO_CAMADA07.md) | [MECADE_IMPLEMENTACAO_CAMADA07](MECADE_IMPLEMENTACAO_CAMADA07) | Implementada e validada E2E |

### Mapeamento de campanha experimental (Secao VIII-C)

| Campanha | Guia (MD) | Pasta de implementacao/validacao | Status atual |
|---|---|---|---|
| Campanha minima viavel Tier A1 | [MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1.md](MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1.md) | [MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1](MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1) | Implementacao executavel criada |

### Arquivos principais de navegacao

- [OVERVIEW_FRAMEWORK_MECADE.md](OVERVIEW_FRAMEWORK_MECADE.md): visao integrada do framework e conexao entre as 7 camadas
- [MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1.md](MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1.md): protocolo minimo para campanha A/B pareada em Kubernetes (tier A1)
- [MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1/README.md](MECADE_CAMPANHA_MINIMA_VIAVEL_VIII_C_A1/README.md): implementacao executavel da campanha minima viavel (scripts + validacao + evidencias)


## Objetivo pratico

Permitir que equipes de engenharia validem resiliencia de forma reproduzivel, auditavel e governada por risco, sem sacrificar requisitos de operacao de sistemas criticos distribuidos.
