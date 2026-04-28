# Tracker de falsos positivos/negativos e latencia de decisao

Registre por ciclo experimental:

1. Precision e recall para eventos criticos.
2. Taxa de falso positivo ALERT/LIMIT.
3. Taxa de falso negativo em gray failure.
4. Lead-time-to-failure (tempo entre ALERT e violacao LIMIT/BLOCK).
5. Tempo de decisao (detectar -> acionar BLOCK).

| ciclo | precision | recall | fp_alert_limit | fn_gray_failure | lead_time_s | decision_latency_ms |
|------:|----------:|-------:|---------------:|----------------:|------------:|--------------------:|
| 1     | 0.90      | 0.83   | 0.09           | 0.17            | 75          | 980                 |
