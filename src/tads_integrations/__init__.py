"""Versioned ReconOS and FadeReach integration contracts."""

from .models import EnrichmentRequest, EnrichmentResult, OpportunityHandoff
from .ports import FadeReachPort, ReconOSPort
from .fadereach_http import FadeReachHttpAdapter
from .reconos_http import ReconOSAdapterError, ReconOSHttpAdapter

__all__ = [
    "EnrichmentRequest",
    "FadeReachHttpAdapter",
    "EnrichmentResult",
    "FadeReachPort",
    "OpportunityHandoff",
    "ReconOSAdapterError",
    "ReconOSHttpAdapter",
    "ReconOSPort",
]
