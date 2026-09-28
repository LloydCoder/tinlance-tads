"""Evidence-first domain distinctions frozen by M0."""

from dataclasses import dataclass
from datetime import datetime

from .provenance import EvidenceRef


@dataclass(frozen=True, slots=True)
class ObservationRef:
    """A source observation. It is not a signal or an interpretation."""

    observation_id: str
    source_id: str
    snapshot_id: str
    observed_at: datetime
    content_hash: str

    def validate(self) -> None:
        if not all((self.observation_id, self.source_id, self.snapshot_id, self.content_hash)):
            raise ValueError("observation requires stable identity and source lineage")


@dataclass(frozen=True, slots=True)
class CanonicalEventRef:
    """A normalized real-world event derived from one or more observations."""

    event_id: str
    event_type: str
    observation_ids: tuple[str, ...]
    occurred_at: datetime | None

    def validate(self) -> None:
        if not self.event_id or not self.event_type:
            raise ValueError("canonical event requires identity and type")
        if not self.observation_ids:
            raise ValueError("canonical event requires observations")


@dataclass(frozen=True, slots=True)
class SignalRef:
    """A derived signal that must remain traceable to evidence."""

    signal_id: str
    account_id: str
    signal_type: str
    event_id: str
    evidence: tuple[EvidenceRef, ...]
    confidence: float

    def validate(self) -> None:
        if not self.signal_id or not self.account_id or not self.signal_type:
            raise ValueError("signal requires identity, account and type")
        if not self.event_id:
            raise ValueError("signal requires a canonical event")
        if not self.evidence:
            raise ValueError("signal requires evidence")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("signal confidence must be between 0 and 1")
        for item in self.evidence:
            item.validate()
