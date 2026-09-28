"""PostgreSQL sinks for M2 snapshots and observations."""

from typing import Any
from psycopg import Connection
from tads_db import ObservationRepository, SourceRepository
from .models import FetchResult, NormalizedObservation

class PostgresSnapshotSink:
    def __init__(self, conn: Connection[Any]):
        self.sources = SourceRepository(conn)

    def store_snapshot(self, source_id: str, result: FetchResult, content_hash: str) -> str:
        return self.sources.create_snapshot(
            source_id, result.captured_at, content_hash, result.content_type, len(result.body)
        )

class PostgresObservationSink:
    def __init__(self, conn: Connection[Any]):
        self.observations = ObservationRepository(conn)

    def create_observation(
        self, source_id: str, snapshot_id: str, observation: NormalizedObservation
    ) -> str:
        return self.observations.create(
            source_id, snapshot_id, observation.observed_at,
            observation.content_hash, observation.payload, observation.locator
        )
