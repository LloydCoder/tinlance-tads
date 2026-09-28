"""Controlled source-ingestion primitives for TADS M2."""

from .adapters import GreenhouseAdapter, LeverAdapter
from .fetcher import FetchPolicy, SafeFetcher
from .models import FetchResult, IngestionRecord, NormalizedObservation
from .service import IngestionService
from .storage import PostgresObservationSink, PostgresSnapshotSink

__all__ = [
    "FetchPolicy",
    "FetchResult",
    "GreenhouseAdapter",
    "IngestionRecord",
    "IngestionService",
    "LeverAdapter",
    "NormalizedObservation",
    "PostgresObservationSink",
    "PostgresSnapshotSink",
    "SafeFetcher",
]
