"""PostgreSQL persistence primitives for TADS M1."""

from .connection import TenantConnection
from .migrate import apply_migrations
from .repositories import (
    AccountRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    SignalRepository,
    SignalDetectionRepository,
    SourceRepository,
)

__all__ = [
    "AccountRepository",
    "EvidenceRepository",
    "EventRepository",
    "ObservationRepository",
    "SignalRepository",
    "SignalDetectionRepository",
    "SourceRepository",
    "TenantConnection",
    "apply_migrations",
]
