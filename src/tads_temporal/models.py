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
