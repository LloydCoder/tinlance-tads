# Evaluation & Experimentation

X8 elevates TADS evaluation into a reproducible measurement surface.

## Metrics

The platform provides deterministic primitives for:

- detection precision, recall and F1;
- ranking precision@k, recall@k and NDCG@k;
- calibration via Brier score;
- metric drift against an explicit baseline and threshold.

## Reproducibility

Every evaluation run identifies:

- corpus;
- as-of timestamp;
- code version;
- taxonomy version;
- leakage-check status;
- representative-corpus status.

An evaluation run cannot validate until temporal leakage checks have passed and the corpus is identified as representative.

## Boundary

Evaluation never mutates historical evidence or retroactively changes a score. Results inform monitoring and future improvements; they do not grant authorization or create outreach.

The production gate remains stronger than unit metrics: TADS still requires a representative operational corpus, monitored calibration, drift/error telemetry and the M18 evidence gates.
