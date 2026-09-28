"""Ingestion orchestration above the M1 persistence layer."""

from datetime import UTC
from hashlib import sha256
from typing import Protocol

from .models import FetchResult, IngestionRecord, NormalizedObservation

class SnapshotSink(Protocol):
    def store_snapshot(self, source_id: str, result: FetchResult, content_hash: str) -> str: ...

class ObservationSink(Protocol):
    def create_observation(
        self, source_id: str, snapshot_id: str, observation: NormalizedObservation
    ) -> str: ...

class IngestionService:
    def __init__(self, snapshot_sink: SnapshotSink, observation_sink: ObservationSink):
        self.snapshots = snapshot_sink
        self.observations = observation_sink

    def ingest(
        self, source_id: str, source_url: str, result: FetchResult,
        observations: tuple[NormalizedObservation, ...],
    ) -> IngestionRecord:
        if result.url != source_url:
            raise ValueError("source URL mismatch")
        content_hash = "sha256:" + sha256(result.body).hexdigest()
        snapshot_id = self.snapshots.store_snapshot(source_id, result, content_hash)
        created = [
            self.observations.create_observation(
                source_id, snapshot_id,
                NormalizedObservation(
                    item.external_id, item.source_kind, item.locator,
                    item.observed_at.astimezone(UTC), item.payload, item.content_hash,
                ),
            )
            for item in observations
        ]
        return IngestionRecord(
            source_id, source_url, result.captured_at, content_hash,
            len(observations), tuple(created)
        )
