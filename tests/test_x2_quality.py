import pytest

from tads_quality import QualityAssessment, QualityBand, QualityThresholds, is_eligible


def assessment(**overrides: float) -> QualityAssessment:
    values = {
        "freshness": 0.9,
        "completeness": 0.9,
        "consistency": 0.9,
        "source_reliability": 0.8,
        "identity_confidence": 0.9,
        "temporal_validity": 0.9,
        "corroboration": 0.7,
        "contradiction": 0.1,
    }
    values.update(overrides)
    return QualityAssessment(**values)


def test_quality_dimensions_are_independent() -> None:
    item = assessment(source_reliability=0.4, identity_confidence=0.95)
    item.validate()
    assert item.source_reliability == 0.4
    assert item.identity_confidence == 0.95


def test_high_quality_requires_corroboration() -> None:
    assert assessment(corroboration=0.7).band is QualityBand.HIGH
    assert assessment(corroboration=0.1).band is QualityBand.MEDIUM


def test_contradiction_forces_low_band_and_blocks_eligibility() -> None:
    item = assessment(contradiction=0.75)
    assert item.band is QualityBand.LOW
    assert is_eligible(item) is False


def test_out_of_range_dimension_is_rejected() -> None:
    with pytest.raises(ValueError, match=r"[0, 1]"):
        assessment(freshness=1.1).validate()


def test_thresholds_are_validated() -> None:
    with pytest.raises(ValueError, match=r"[0, 1]"):
        QualityThresholds(minimum_dimension=-0.1).validate()
