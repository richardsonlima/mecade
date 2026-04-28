# RRIndex - Definicao Metrologica

Formula:

RRIndex = w1 * (1 - norm_mttr) + w2 * norm_availability + w3 * (1 - norm_p99) + w4 * norm_tsr

Restricoes:

- w1 + w2 + w3 + w4 = 1
- Pesos definidos por dominio de risco
- Normalizacao por baseline pre-registrado

Saida:

- RRIndex em [0, 1]
- Quanto maior, melhor a maturidade operacional
