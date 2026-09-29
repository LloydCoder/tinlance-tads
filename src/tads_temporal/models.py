"""Temporal intelligence models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class SignalPoint:
    signal_id: str
    account_id: str
    kind: str
    observed_at: datetime
    quality: float
    source_key: str
    direction: int = 1
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.signal_id or not self.account_id or not self.kind or not self.source_key:
            raise ValueError("signal points require identity and source context")
        if not self.evidence_ids or any(not item for item in self.evidence_ids):
            raise ValueError("signal points require evidence")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("signal point evidence identifiers must be unique")
        if not 0.0 <= self.quality <= 1.0:
            raise ValueError("signal point quality must be between 0 and 1")
        if self.direction not in (-1, 0, 1):
            raise ValueError("signal point direction must be -1, 0 or 1")


@dataclass(frozen=True, slots=True)
class TemporalFeatures:
    count: int
    density: float
    diversity: float
    independence: float
    momentum: float
    contradiction: float
    window_seconds: float
    rule_version: str
    evidence_ids: tuple[str, ...] = ()
