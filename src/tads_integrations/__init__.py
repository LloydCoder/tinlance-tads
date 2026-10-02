"""Versioned ReconOS and FadeReach integration contracts."""

from .errors import IntegrationAdapterError
from .fadereach_http import FadeReachHttpAdapter
from .models import EnrichmentRequest, EnrichmentResult, OpportunityHandoff
from .ports import FadeReachPort, ReconOSPort
from .reconos_http import ReconOSAdapterError, ReconOSHttpAdapter

__all__ = [
    "EnrichmentRequest",
    "FadeReachHttpAdapter",
    "EnrichmentResult",
    "FadeReachPort",
    "IntegrationAdapterError",
    "OpportunityHandoff",
    "ReconOSAdapterError",
    "ReconOSHttpAdapter",
    "ReconOSPort",
]
