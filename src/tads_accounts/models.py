"""Account intelligence models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AccountSignal:
    signal_id: str
    kind: str
    quality: float
    freshness: float
    direction: int
    observed_at: datetime


@dataclass(frozen=True, slots=True)
class AccountState:
    account_id: str
    signal_strength: float
    signal_diversity: float
    momentum: float
    negative_evidence: float
    data_confidence: float
    active_signal_count: int
    state_version: str
    drivers: tuple[str, ...]
