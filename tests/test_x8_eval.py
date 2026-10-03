from datetime import UTC, datetime

import pytest

from tads_eval import (
    CalibrationMetrics,
    DetectionMetrics,
    DriftReport,
    EvaluationRun,
    RankingMetrics,
)


def test_detection_metrics_are_deterministic() -> None:
    metrics = DetectionMetrics(8, 2, 2)
    assert metrics.precision == pytest.approx(0.8)
    assert metrics.recall == pytest.approx(0.8)
    assert metrics.f1 == pytest.approx(0.8)


def test_ranking_metrics() -> None:
    metrics = RankingMetrics(frozenset({"a", "c"}), ("a", "b", "c"))
    assert metrics.precision_at_k(2) == pytest.approx(0.5)
    assert metrics.recall_at_k(2) == pytest.approx(0.5)
    assert metrics.ndcg_at_k(3) > 0.7


def test_calibration_uses_brier_score() -> None:
    metrics = CalibrationMetrics((0.9, 0.2), (1, 0))
    assert metrics.brier_score == pytest.approx(0.025)


def test_drift_report_is_fail_closed_at_threshold() -> None:
    assert DriftReport(0.8, 0.6, 0.2).detected is True
    assert DriftReport(0.8, 0.61, 0.2).detected is False


def test_evaluation_run_requires_representative_leakage_checked_corpus() -> None:
    run = EvaluationRun(
        "run-1",
        "corpus-1",
        datetime(2026, 10, 3, 11, 0, tzinfo=UTC),
        "git-sha",
        "taxonomy-v1",
        True,
        True,
    )
    run.validate()


def test_evaluation_run_rejects_future_leakage_not_checked() -> None:
    run = EvaluationRun(
        "run-1",
        "corpus-1",
        datetime(2026, 10, 3, 11, 0, tzinfo=UTC),
        "git-sha",
        "taxonomy-v1",
        False,
        True,
    )
    with pytest.raises(ValueError, match="leakage"):
        run.validate()
