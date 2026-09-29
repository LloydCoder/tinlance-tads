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
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.signal_id or not self.kind or not self.evidence_ids:
            raise ValueError("account signals require identity, kind and evidence")
        if any(not item for item in self.evidence_ids):
            raise ValueError("account signal evidence identifiers must be non-empty")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("account signal evidence identifiers must be unique")
        if not 0.0 <= self.quality <= 1.0 or not 0.0 <= self.freshness <= 1.0:
            raise ValueError("account signal quality and freshness must be between 0 and 1")
        if self.direction not in (-1, 0, 1):
            raise ValueError("account signal direction must be -1, 0 or 1")


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
    evidence_ids: tuple[str, ...] = ()
