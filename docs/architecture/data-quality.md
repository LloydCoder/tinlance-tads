# Data Quality & Evidence Trust

TADS keeps evidence quality separate from intelligence and opportunity scores.

## Dimensions

The X2 assessment models freshness, completeness, consistency, source reliability, identity confidence, temporal validity, corroboration and contradiction independently. Every dimension is bounded to [0, 1].

## Eligibility

Eligibility is a deterministic control decision, not a prediction score. The default threshold requires every core validity dimension to meet 0.5 and contradiction to remain below 0.75.

A quality band is a compact presentation of the dimensions; it must never replace the underlying values or evidence lineage.

## Boundary

X2 does not mutate observations, signals or opportunities. It evaluates the quality of the evidence supporting them. Production quality monitoring and source-specific calibration remain operational evaluation work.
