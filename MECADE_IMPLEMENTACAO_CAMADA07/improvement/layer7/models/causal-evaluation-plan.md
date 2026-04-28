# Causal evaluation plan

Pergunta:
- Qual o efeito causal da policy_version_k sobre MTTR e taxa de bloqueio falso?

Estrategia:
- Diferenca-em-diferencas com grupo de controle comparavel.
- Ajuste por carga e sazonalidade.

Saidas:
- ATT para MTTR.
- IC95% do efeito.
- Analise de sensibilidade.
