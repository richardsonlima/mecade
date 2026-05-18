package mecade.layer5

default allow = false

allow {
  input.slo_pass == true
  input.non_regression_pass == true
  input.risk_score <= 0.45
}
