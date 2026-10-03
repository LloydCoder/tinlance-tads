"""Deterministic evaluation metrics and reproducibility controls."""

from dataclasses import dataclass
from datetime import datetime
from math import log2


@dataclass(frozen=True, slots=True)
class DetectionMetrics:
    true_positive: int
    false_positive: int
    false_negative: int

    def validate(self) -> None:
        if min(self.true_positive, self.false_positive, self.false_negative) < 0:
            raise ValueError("detection counts cannot be negative")

    @property
    def precision(self) -> float:
        self.validate()
        denominator = self.true_positive + self.false_positive
        return self.true_positive / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        self.validate()
        denominator = self.true_positive + self.false_negative
        return self.true_positive / denominator if denominator else 0.0

    @property
    def f1(self) -> float:
        precision = self.precision
        recall = self.recall
        return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


@dataclass(frozen=True, slots=True)
class RankingMetrics:
    relevant_ids: frozenset[str]
    ranked_ids: tuple[str, ...]

    def precision_at_k(self, k: int) -> float:
        if k <= 0:
            raise ValueError("k must be positive")
        selected = self.ranked_ids[:k]
        return (
            sum(item in self.relevant_ids for item in selected) / len(selected)
            if selected
            else 0.0
        )

    def recall_at_k(self, k: int) -> float:
        if k <= 0:
            raise ValueError("k must be positive")
        return (
            sum(item in self.relevant_ids for item in self.ranked_ids[:k]) / len(self.relevant_ids)
            if self.relevant_ids
            else 0.0
        )

    def ndcg_at_k(self, k: int) -> float:
        if k <= 0:
            raise ValueError("k must be positive")
        selected = self.ranked_ids[:k]
        dcg = sum(
            (1.0 if item in self.relevant_ids else 0.0) / log2(index + 2)
            for index, item in enumerate(selected)
        )
        ideal_hits = min(k, len(self.relevant_ids))
        idcg = sum(1.0 / log2(index + 2) for index in range(ideal_hits))
        return dcg / idcg if idcg else 0.0


@dataclass(frozen=True, slots=True)
class CalibrationMetrics:
    probabilities: tuple[float, ...]
    outcomes: tuple[int, ...]

    def validate(self) -> None:
        if len(self.probabilities) != len(self.outcomes) or not self.probabilities:
            raise ValueError("calibration inputs must be non-empty and aligned")
        if any(not 0.0 <= probability <= 1.0 for probability in self.probabilities):
            raise ValueError("probabilities must be within [0, 1]")
        if any(outcome not in (0, 1) for outcome in self.outcomes):
            raise ValueError("outcomes must be binary")

    @property
    def brier_score(self) -> float:
        self.validate()
        return sum(
            (probability - outcome) ** 2
            for probability, outcome in zip(self.probabilities, self.outcomes, strict=True)
        ) / len(self.probabilities)


@dataclass(frozen=True, slots=True)
class DriftReport:
    baseline_metric: float
    current_metric: float
    threshold: float

    def validate(self) -> None:
        if not 0.0 <= self.baseline_metric <= 1.0:
            raise ValueError("baseline_metric must be within [0, 1]")
        if not 0.0 <= self.current_metric <= 1.0:
            raise ValueError("current_metric must be within [0, 1]")
        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("threshold must be within [0, 1]")

    @property
    def detected(self) -> bool:
        self.validate()
        return abs(self.current_metric - self.baseline_metric) >= self.threshold


@dataclass(frozen=True, slots=True)
class EvaluationRun:
    run_id: str
    corpus_id: str
    as_of: datetime
    code_version: str
    taxonomy_version: str
    leakage_checked: bool
    representative_corpus: bool

    def validate(self) -> None:
        if (
            not self.run_id
            or not self.corpus_id
            or not self.code_version
            or not self.taxonomy_version
        ):
            raise ValueError("evaluation run identity/version fields are required")
        if self.as_of.tzinfo is None:
            raise ValueError("evaluation as_of must be timezone-aware")
        if not self.leakage_checked:
            raise ValueError("evaluation run must pass leakage checks")
        if not self.representative_corpus:
            raise ValueError("evaluation run must identify a representative corpus")
