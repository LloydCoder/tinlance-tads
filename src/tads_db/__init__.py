"""PostgreSQL persistence primitives for TADS M1."""

from .connection import TenantConnection
from .migrate import apply_migrations
from .repositories import (
    AccountRepository,
    AccountStateRepository,
    AgentSpecRepository,
    CorrelationRepository,
    EnrichmentRunRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    OpportunityHandoffRepository,
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
    "EnrichmentRunRepository",
    "EventRepository",
    "ObservationRepository",
    "OpportunityHandoffRepository",
    "OpportunityRepository",
    "SignalRepository",
    "SignalDetectionRepository",
    "SourceRepository",
    "TenantConnection",
    "apply_migrations",
]
