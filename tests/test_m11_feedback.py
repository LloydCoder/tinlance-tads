import pytest

from tads_assurance import TemporalEvaluation


def test_temporal_evaluation_rejects_future_label_leakage() -> None:
    evaluation = TemporalEvaluation(
        "2026-01-01T00:00:00Z",
        "2026-01-02T00:00:00Z",
        0.8,
        True,
    )
    assert evaluation.available_at("2026-01-01T12:00:00Z") is False
    assert evaluation.available_at("2026-01-02T00:00:00Z") is True
    assert evaluation.absolute_error == pytest.approx(0.2)


def test_temporal_evaluation_rejects_naive_or_reversed_timestamps() -> None:
    try:
        TemporalEvaluation(
            "2026-01-02T00:00:00Z",
            "2026-01-01T00:00:00Z",
            0.5,
            False,
        )
    except ValueError as exc:
        assert "label_at" in str(exc)
    else:
        raise AssertionError("reversed evaluation timestamps must fail")

    try:
        TemporalEvaluation(
            "2026-01-01T00:00:00",
            "2026-01-02T00:00:00Z",
            0.5,
            False,
        )
    except ValueError as exc:
        assert "timezone" in str(exc)
    else:
        raise AssertionError("naive evaluation timestamps must fail")
