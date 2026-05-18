# Modelo de risco posterior (Camada 3)

PosteriorRisk = P(falha_critica | sinais) * ImpactoDominio

Regra:
- ALERT quando PosteriorRisk >= 0.30
- LIMIT quando PosteriorRisk >= 0.55
- BLOCK quando PosteriorRisk >= 0.80 ou hard_safety_limits violados
