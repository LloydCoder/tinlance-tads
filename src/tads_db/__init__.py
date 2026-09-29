"""PostgreSQL persistence primitives for TADS."""

from .connection import TenantConnection
from .integration_repositories import EnrichmentRunRepository, OpportunityHandoffRepository
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
    "AccountStateRepository",
    "AgentSpecRepository",
    "CorrelationRepository",
    "EnrichmentRunRepository",
    "EvidenceRepository",
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
