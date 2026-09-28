"""Transport models for source ingestion."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class FetchResult:
    url: str
    status_code: int
    content_type: str
    body: bytes
    captured_at: datetime
    headers: dict[str, str]


@dataclass(frozen=True, slots=True)
class NormalizedObservation:
    external_id: str
    source_kind: str
    locator: str
    observed_at: datetime
    payload: dict[str, Any]
    content_hash: str


@dataclass(frozen=True, slots=True)
class IngestionRecord:
    source_key: str
    source_url: str
    fetched_at: datetime
    content_hash: str
    observation_count: int
    created_observation_ids: tuple[str, ...]
