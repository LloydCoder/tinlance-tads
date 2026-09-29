"""PostgreSQL persistence primitives for TADS M1."""

from .connection import TenantConnection
from .migrate import apply_migrations
from .repositories import (
    AccountRepository,
    AccountStateRepository,
    CorrelationRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    SignalDetectionRepository,
    SignalRepository,
    SourceRepository,
)

__all__ = [
    "AccountRepository",
    "AccountStateRepository",
    "CorrelationRepository",
    "EvidenceRepository",
    "EventRepository",
    "ObservationRepository",
    "SignalRepository",
    "SignalDetectionRepository",
    "SourceRepository",
    "TenantConnection",
    "apply_migrations",
]
