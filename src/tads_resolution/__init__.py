"""Deterministic canonical entity resolution for TADS M3."""

from .models import Candidate, ResolutionResult
from .normalization import normalize_domain, normalize_name
from .resolver import EntityResolver

__all__ = ["Candidate", "EntityResolver", "ResolutionResult", "normalize_domain", "normalize_name"]
