"""Provider-neutral M0 contracts for Tinlance TADS."""

from .domain import CanonicalEventRef, ObservationRef, SignalRef
from .integration import FadeReachHandoff, ReconOSRequest
from .provenance import EvidenceRef, ProvenanceRef
from .scoring import ScoreComponent, ScoreContract
from .source import SourceContract
from .taxonomy import SignalType, SourceClass

__all__ = [
    "CanonicalEventRef",
    "EvidenceRef",
    "FadeReachHandoff",
    "ObservationRef",
    "ProvenanceRef",
    "ReconOSRequest",
    "ScoreComponent",
    "ScoreContract",
    "SignalRef",
    "SignalType",
    "SourceClass",
    "SourceContract",
]
