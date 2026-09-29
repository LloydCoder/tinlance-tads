"""Explicit integration ports; adapters remain external-system specific."""

from typing import Protocol

from .models import EnrichmentRequest, EnrichmentResult, OpportunityHandoff


class ReconOSPort(Protocol):
    def enrich(self, request: EnrichmentRequest) -> EnrichmentResult: ...


class FadeReachPort(Protocol):
    def publish(self, handoff: OpportunityHandoff) -> str: ...
