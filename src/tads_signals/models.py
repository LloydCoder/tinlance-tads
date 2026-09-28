"""Signal domain objects with explicit evidence and lifecycle state."""

from dataclasses import dataclass
from enum import StrEnum


class SignalKind(StrEnum):
    HIRING = "hiring"
    SECURITY = "security"
    TECHNOLOGY = "technology"
    PRODUCT = "product"
    REGULATORY = "regulatory"
    COMMERCIAL = "commercial"
    COMPANY = "company"


class SignalState(StrEnum):
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    EXPIRED = "expired"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class DetectedSignal:
    kind: SignalKind
    subtype: str
    state: SignalState
    strength: float
    freshness: float
    reliability: float
    evidence_observation_id: str
    rationale: tuple[str, ...]

    @property
    def quality(self) -> float:
        return round(self.strength * self.freshness * self.reliability, 6)
