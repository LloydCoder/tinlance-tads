"""Small tenant-scoped SQL repositories; intelligence logic remains above persistence."""

from collections.abc import Sequence
from datetime import datetime
from typing import Any

from psycopg import Connection


class AccountRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(self, name: str) -> str:
        row = self.conn.execute(
            "INSERT INTO accounts(canonical_name) VALUES (%s) RETURNING id", (name,)
        ).fetchone()
        assert row is not None
        return str(row[0])

    def get(self, account_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT id, canonical_name, status FROM accounts WHERE id = %s", (account_id,)
        ).fetchone()
        return (
            None
            if row is None
            else {"id": str(row[0]), "canonical_name": row[1], "status": row[2]}
        )


class SourceRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        provider: str,
        name: str,
        source_class: str,
        access_mechanism: str,
        terms_reference: str,
    ) -> str:
        row = self.conn.execute(
            """INSERT INTO sources(provider,name,source_class,access_mechanism,terms_reference)
               VALUES (%s,%s,%s,%s,%s) RETURNING id""",
            (provider, name, source_class, access_mechanism, terms_reference),
        ).fetchone()
        assert row is not None
        return str(row[0])

    def create_snapshot(
        self,
        source_id: str,
        captured_at: datetime,
        content_hash: str,
        content_type: str | None = None,
        byte_size: int | None = None,
    ) -> str:
        row = self.conn.execute(
            """INSERT INTO source_snapshots(
                   source_id,captured_at,content_hash,content_type,byte_size
               ) VALUES (%s,%s,%s,%s,%s) RETURNING id""",
            (source_id, captured_at, content_hash, content_type, byte_size),
        ).fetchone()
        assert row is not None
        return str(row[0])


class ObservationRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        source_id: str,
        snapshot_id: str,
        observed_at: datetime,
        content_hash: str,
        payload: dict[str, Any],
        locator: str | None = None,
    ) -> str:
        row = self.conn.execute(
            """INSERT INTO observations(
                   source_id,snapshot_id,observed_at,content_hash,payload,locator
               ) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id""",
            (source_id, snapshot_id, observed_at, content_hash, payload, locator),
        ).fetchone()
        assert row is not None
        return str(row[0])


class EventRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        event_type: str,
        observation_ids: Sequence[str],
        occurred_at: datetime | None,
        event_time_confidence: float,
        payload: dict[str, Any] | None = None,
    ) -> str:
        if not observation_ids:
            raise ValueError("canonical event requires observations")
        row = self.conn.execute(
            """INSERT INTO canonical_events(
                   event_type,occurred_at,event_time_confidence,normalized_payload
               ) VALUES (%s,%s,%s,%s) RETURNING id""",
            (event_type, occurred_at, event_time_confidence, payload or {}),
        ).fetchone()
        assert row is not None
        event_id = str(row[0])
        for observation_id in observation_ids:
            self.conn.execute(
                "INSERT INTO event_observations(event_id,observation_id) VALUES (%s,%s)",
                (event_id, observation_id),
            )
        return event_id


class EvidenceRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        source_id: str,
        snapshot_id: str,
        observed_at: datetime,
        content_hash: str,
        extractor: str,
        extractor_version: str,
        confidence: float,
        observation_id: str | None = None,
        locator: str | None = None,
        excerpt: str | None = None,
    ) -> str:
        row = self.conn.execute(
            """INSERT INTO evidence(
                   source_id,snapshot_id,observation_id,locator,excerpt,content_hash,
                   confidence,observed_at,extractor,extractor_version
               ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
            (
                source_id,
                snapshot_id,
                observation_id,
                locator,
                excerpt,
                content_hash,
                confidence,
                observed_at,
                extractor,
                extractor_version,
            ),
        ).fetchone()
        assert row is not None
        return str(row[0])


class SignalRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        account_id: str,
        event_id: str,
        signal_type: str,
        confidence: float,
        relevance: float,
        freshness: float,
        reliability: float,
        business_impact: float,
        direction: int,
        first_seen_at: datetime,
        last_seen_at: datetime,
        evidence_ids: Sequence[str],
        signal_subtype: str | None = None,
        expires_at: datetime | None = None,
    ) -> str:
        if not evidence_ids:
            raise ValueError("signal requires evidence")
        row = self.conn.execute(
            """INSERT INTO signals(
                   account_id,event_id,signal_type,signal_subtype,confidence,relevance,
                   freshness,reliability,business_impact,direction,first_seen_at,last_seen_at,expires_at
               ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
            (
                account_id,
                event_id,
                signal_type,
                signal_subtype,
                confidence,
                relevance,
                freshness,
                reliability,
                business_impact,
                direction,
                first_seen_at,
                last_seen_at,
                expires_at,
            ),
        ).fetchone()
        assert row is not None
        signal_id = str(row[0])
        for evidence_id in evidence_ids:
            self.conn.execute(
                "INSERT INTO signal_evidence(signal_id,evidence_id) VALUES (%s,%s)",
                (signal_id, evidence_id),
            )
        return signal_id
