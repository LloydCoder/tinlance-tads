from datetime import UTC, datetime

import pytest

from tads_signalops import SignalDrift, SignalEvent, SignalLifecycle, SignalRegistry


def event(kind: SignalLifecycle, minute: int) -> SignalEvent:
    return SignalEvent(
        signal_id="sig-1",
        lifecycle=kind,
        occurred_at=datetime(2026, 10, 3, 11, minute, tzinfo=UTC),
        evidence_ids=("ev-1",),
    )


def test_signal_history_is_append_only_and_chronological() -> None:
    registry = SignalRegistry()
    registry.append(event(SignalLifecycle.DETECTED, 0))
    registry.append(event(SignalLifecycle.CORROBORATED, 1))
    assert [item.lifecycle for item in registry.history("sig-1")] == [
        SignalLifecycle.DETECTED,
        SignalLifecycle.CORROBORATED,
    ]


def test_out_of_order_signal_event_is_rejected() -> None:
    registry = SignalRegistry()
    registry.append(event(SignalLifecycle.DETECTED, 2))
    with pytest.raises(ValueError, match="chronological"):
        registry.append(event(SignalLifecycle.WEAKENED, 1))


def test_signal_events_require_evidence_and_aware_time() -> None:
    with pytest.raises(ValueError, match="evidence"):
        SignalEvent("sig-1", SignalLifecycle.DETECTED, datetime(2026, 10, 3, tzinfo=UTC), ()).validate()
    with pytest.raises(ValueError, match="timezone-aware"):
        SignalEvent("sig-1", SignalLifecycle.DETECTED, datetime(2026, 10, 3), ("ev-1",)).validate()


def test_drift_is_detected_when_any_material_metric_crosses_threshold() -> None:
    metrics = SignalDrift(0.1, 0.21, 0.0, 0.0)
    assert metrics.detected is True
    assert SignalDrift(0.1, 0.19, 0.0, 0.0).detected is False
