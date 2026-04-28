# Protocolo de Validacao - Camada 3

Cenario A - Drift progressivo sem outage:
- aumentar latencia em degraus a cada 2 minutos
- validar deteccao de gray failure antes de 5xx massivo

Cenario B - Ruido sem falha real:
- injetar variabilidade controlada de curta duracao
- validar que LIMIT/BLOCK nao disparam indevidamente

Cenario C - Hard safety:
- violar limite duro de p99/error_rate
- validar BLOCK em tempo alvo e transicao para estado seguro

Cenario D - Ablacao de sinais:
- remover log/trace e repetir cenario
- medir degradacao da qualidade de decisao do comite
