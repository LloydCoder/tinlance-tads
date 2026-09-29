from datetime import UTC, datetime, timedelta

import pytest

from tads_temporal import CorrelationEngine, SignalPoint


def test_empty_window_is_deterministic() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    result = CorrelationEngine().features([], start=start, end=start + timedelta(days=7))
    assert result.count == 0
    assert result.momentum == 0.0
    assert result.evidence_ids == ()


def test_temporal_features_measure_diversity_independence_and_contradiction() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    signals = [
        SignalPoint("s1", "a1", "hiring", start + timedelta(days=1), 0.8, "greenhouse", 1, ("ev-1",)),
        SignalPoint("s2", "a1", "security", start + timedelta(days=3), 0.9, "press", 1, ("ev-2",)),
        SignalPoint("s3", "a1", "security", start + timedelta(days=5), 0.7, "press", -1, ("ev-3",)),
    ]
    result = CorrelationEngine().features(signals, start=start, end=start + timedelta(days=7))
    assert result.count == 3
    assert result.diversity == pytest.approx(2 / 3)
    assert result.independence == pytest.approx(2 / 3)
    assert result.contradiction == pytest.approx(1 / 3)
    assert result.evidence_ids == ("ev-1", "ev-2", "ev-3")


def test_invalid_window_is_rejected() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValueError):
        CorrelationEngine().features([], start=now, end=now)


def test_signal_point_requires_evidence() -> None:
    with pytest.raises(ValueError, match="evidence"):
        SignalPoint("s1", "a1", "hiring", datetime.now(UTC), 0.8, "greenhouse")
