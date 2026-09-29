"""PostgreSQL persistence primitives for TADS M1."""

from .connection import TenantConnection
from .migrate import apply_migrations
from .repositories import (
    AccountRepository,
    AccountStateRepository,
    AgentSpecRepository,
    CorrelationRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    OpportunityRepository,
    SignalDetectionRepository,
    SignalRepository,
    SourceRepository,
)

__all__ = [
    "AccountRepository",
    "AgentSpecRepository",
    "AccountStateRepository",
    "CorrelationRepository",
    "EvidenceRepository",
    "EventRepository",
    "ObservationRepository",
    "OpportunityRepository",
    "SignalRepository",
    "SignalDetectionRepository",
    "SourceRepository",
    "TenantConnection",
    "apply_migrations",
]
