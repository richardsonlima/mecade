# Risk score model

RiskScore = w1*P(SLO_violation) + w2*P(recovery_delay) + w3*change_complexity + w4*dependency_instability

Faixas:
- <= 0.30: baixo risco
- 0.31 a 0.45: risco moderado
- > 0.45: bloquear release
