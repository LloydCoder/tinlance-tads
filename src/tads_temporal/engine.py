"""Evidence-preserving temporal correlation rules."""

from collections.abc import Sequence
from datetime import datetime

from .models import SignalPoint, TemporalFeatures


class CorrelationEngine:
    """Computes deterministic, replayable features without inferring intent."""

    def __init__(self, rule_version: str = "m5-v1"):
        self.rule_version = rule_version

    def features(
        self,
        signals: Sequence[SignalPoint],
        *,
        start: datetime,
        end: datetime,
    ) -> TemporalFeatures:
        if end <= start:
            raise ValueError("correlation window must have positive duration")
        window = (end - start).total_seconds()
        points = sorted(
            (item for item in signals if start <= item.observed_at <= end),
            key=lambda item: item.observed_at,
        )
        if not points:
            return TemporalFeatures(0, 0.0, 0.0, 0.0, 0.0, 0.0, window, self.rule_version)

        kinds = {item.kind for item in points}
        sources = {item.source_key for item in points}
        positives = sum(1 for item in points if item.direction > 0)
        negatives = sum(1 for item in points if item.direction < 0)
        midpoint = start + (end - start) / 2
        early = sum(item.quality for item in points if item.observed_at < midpoint)
        late = sum(item.quality for item in points if item.observed_at >= midpoint)
        density = min(1.0, len(points) / max(1.0, window / 86400.0))
        diversity = len(kinds) / len(points)
        independence = len(sources) / len(points)
        momentum = min(1.0, max(0.0, late - early + 0.5))
        contradiction = negatives / max(1, positives + negatives)
        evidence_ids = tuple(
            sorted({evidence_id for point in points for evidence_id in point.evidence_ids})
        )
        return TemporalFeatures(
            len(points),
            round(density, 6),
            round(diversity, 6),
            round(independence, 6),
            round(momentum, 6),
            round(contradiction, 6),
            window,
            self.rule_version,
            evidence_ids,
        )
