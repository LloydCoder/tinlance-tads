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
    PEOPLE = "people"
    DIGITAL = "digital"


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
    evidence_ids: tuple[str, ...]
    rationale: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.evidence_observation_id or not self.evidence_ids:
            raise ValueError("detected signals require evidence lineage")
        if any(not item for item in self.evidence_ids):
            raise ValueError("signal evidence identifiers must be non-empty")
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("signal strength must be between 0 and 1")
        if not 0.0 <= self.freshness <= 1.0:
            raise ValueError("signal freshness must be between 0 and 1")
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("signal reliability must be between 0 and 1")

    @property
    def quality(self) -> float:
        return round(self.strength * self.freshness * self.reliability, 6)
