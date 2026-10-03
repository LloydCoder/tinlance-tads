"""Independent data and evidence quality assessment primitives."""

from dataclasses import dataclass
from enum import StrEnum


class QualityBand(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    """Quality dimensions kept independent from intelligence or opportunity scores."""

    freshness: float
    completeness: float
    consistency: float
    source_reliability: float
    identity_confidence: float
    temporal_validity: float
    corroboration: float
    contradiction: float

    def validate(self) -> None:
        values = (
            self.freshness,
            self.completeness,
            self.consistency,
            self.source_reliability,
            self.identity_confidence,
            self.temporal_validity,
            self.corroboration,
            self.contradiction,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("quality dimensions must be within [0, 1]")

    @property
    def band(self) -> QualityBand:
        self.validate()
        usable = min(
            self.freshness,
            self.completeness,
            self.consistency,
            self.source_reliability,
            self.identity_confidence,
            self.temporal_validity,
        )
        if self.contradiction >= 0.75:
            return QualityBand.LOW
        if usable >= 0.8 and self.corroboration >= 0.5:
            return QualityBand.HIGH
        if usable >= 0.5:
            return QualityBand.MEDIUM
        return QualityBand.LOW


@dataclass(frozen=True, slots=True)
class QualityThresholds:
    minimum_dimension: float = 0.5
    maximum_contradiction: float = 0.75

    def validate(self) -> None:
        if not 0.0 <= self.minimum_dimension <= 1.0:
            raise ValueError("minimum_dimension must be within [0, 1]")
        if not 0.0 <= self.maximum_contradiction <= 1.0:
            raise ValueError("maximum_contradiction must be within [0, 1]")


def is_eligible(
    assessment: QualityAssessment,
    thresholds: QualityThresholds | None = None,
) -> bool:
    assessment.validate()
    thresholds = thresholds or QualityThresholds()
    thresholds.validate()
    dimensions = (
        assessment.freshness,
        assessment.completeness,
        assessment.consistency,
        assessment.source_reliability,
        assessment.identity_confidence,
        assessment.temporal_validity,
    )
    return (
        min(dimensions) >= thresholds.minimum_dimension
        and assessment.contradiction < thresholds.maximum_contradiction
    )
