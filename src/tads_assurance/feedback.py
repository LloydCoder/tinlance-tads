"""M11 feedback contracts: outcomes are append-only and never rewrite history."""

from dataclasses import dataclass
from datetime import datetime


def _rate(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass(frozen=True, slots=True)
class OutcomeRecord:
    opportunity_id: str
    decision_at: str
    outcome: str
    source: str
    value: float | None = None

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.decision_at or not self.outcome or not self.source:
            raise ValueError("outcome identity, timestamp, outcome and source are required")


@dataclass(frozen=True, slots=True)
class PrecisionRecall:
    true_positive: int
    false_positive: int
    false_negative: int
    true_negative: int

    def __post_init__(self) -> None:
        if (
            min(self.true_positive, self.false_positive, self.false_negative, self.true_negative)
            < 0
        ):
            raise ValueError("confusion-matrix counts cannot be negative")

    @property
    def precision(self) -> float:
        denominator = self.true_positive + self.false_positive
        return self.true_positive / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        denominator = self.true_positive + self.false_negative
        return self.true_positive / denominator if denominator else 0.0


@dataclass(frozen=True, slots=True)
class CalibrationRecord:
    policy_version: str
    sample_count: int
    predicted_confidence: float
    observed_success_rate: float

    def __post_init__(self) -> None:
        if not self.policy_version or self.sample_count <= 0:
            raise ValueError("calibration requires a policy version and positive sample")
        _rate(self.predicted_confidence, "predicted_confidence")
        _rate(self.observed_success_rate, "observed_success_rate")

    @property
    def absolute_error(self) -> float:
        return abs(self.predicted_confidence - self.observed_success_rate)


@dataclass(frozen=True, slots=True)
class TemporalEvaluation:
    """A prediction/label pair whose evaluation cannot use future information."""

    prediction_at: str
    label_at: str
    predicted_confidence: float
    observed_success: bool

    def __post_init__(self) -> None:
        if not self.prediction_at or not self.label_at:
            raise ValueError("prediction_at and label_at are required")
        prediction = self._parse_timestamp(self.prediction_at)
        label = self._parse_timestamp(self.label_at)
        if label < prediction:
            raise ValueError("label_at cannot precede prediction_at")
        _rate(self.predicted_confidence, "predicted_confidence")

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            raise ValueError("evaluation timestamps must be timezone-aware")
        return parsed

    def available_at(self, as_of: str) -> bool:
        return self._parse_timestamp(self.label_at) <= self._parse_timestamp(as_of)

    @property
    def absolute_error(self) -> float:
        observed = 1.0 if self.observed_success else 0.0
        return abs(self.predicted_confidence - observed)
