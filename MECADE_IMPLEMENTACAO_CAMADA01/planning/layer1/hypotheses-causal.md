# H1 - Efeito esperado do mecanismo de bloqueio

Intervencao: ativar controle ALERT/LIMIT/BLOCK durante falha de latencia progressiva.

Hipotese causal:
- O controle reduz MTTR em pelo menos 15% versus baseline reativo.

Metrica primaria:
- MTTR (s)

Metricas secundarias:
- p99 latency, error_rate, TSR

Criterio de sucesso:
- delta_MTTR <= -15% com IC95% excluindo 0.
