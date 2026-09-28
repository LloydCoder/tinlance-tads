"""Integration tests for the M1 PostgreSQL kernel."""

import os
from datetime import UTC, datetime

import psycopg
import pytest

from tads_db import (
    AccountRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    SignalRepository,
    SourceRepository,
    TenantConnection,
    apply_migrations,
)

pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def dsn() -> str:
    value = os.getenv("DATABASE_URL")
    if not value:
        pytest.skip("DATABASE_URL is not configured")
    return value


@pytest.fixture()
def tenant(dsn: str) -> str:
    apply_migrations(dsn)
    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            "INSERT INTO tenants(name) VALUES ('test-tenant') RETURNING id"
        ).fetchone()
        assert row is not None
        conn.commit()
        return str(row[0])


def test_migration_and_rls_isolation(dsn: str, tenant: str) -> None:
    apply_migrations(dsn)
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("Acme Test")
        account = AccountRepository(conn).get(account_id)
        assert account is not None and account["canonical_name"] == "Acme Test"

    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            "INSERT INTO tenants(name) VALUES ('other-tenant') RETURNING id"
        ).fetchone()
        assert row is not None
        other = str(row[0])
        conn.commit()

    with TenantConnection(dsn, other, "tads_app").transaction() as conn:
        assert AccountRepository(conn).get(account_id) is None


def test_evidence_chain_and_immutability(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        source_id = SourceRepository(conn).create(
            "test", "jobs", "public_structured", "api", "terms"
        )
        snapshot_id = SourceRepository(conn).create_snapshot(
            source_id, datetime.now(UTC), "sha256:snapshot"
        )
        observation_id = ObservationRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:obs",
            {"title": "Engineer"},
        )
        event_id = EventRepository(conn).create(
            "job_posted", [observation_id], datetime.now(UTC), 0.9
        )
        evidence_id = EvidenceRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:evidence",
            "test",
            "1",
            0.95,
            observation_id,
        )
        account_id = AccountRepository(conn).create("Acme")
        signal_id = SignalRepository(conn).create(
            account_id,
            event_id,
            "hiring",
            0.9,
            0.9,
            1.0,
            0.95,
            0.7,
            1,
            datetime.now(UTC),
            datetime.now(UTC),
            [evidence_id],
        )
        assert signal_id
        with conn.transaction():
            with pytest.raises(psycopg.errors.RaiseException, match="evidence is immutable"):
                conn.execute(
                    "UPDATE evidence SET excerpt='tampered' WHERE id=%s",
                    (evidence_id,),
                )
        with conn.transaction():
            with pytest.raises(psycopg.errors.RaiseException, match="evidence is immutable"):
                conn.execute("DELETE FROM evidence WHERE id=%s", (evidence_id,))
        lineage = conn.execute(
            """SELECT s.id, ss.id, o.id, e.id, sig.id
               FROM sources s
               JOIN source_snapshots ss ON ss.source_id=s.id
               JOIN observations o ON o.snapshot_id=ss.id
               JOIN evidence e ON e.observation_id=o.id
               JOIN signal_evidence se ON se.evidence_id=e.id
               JOIN signals sig ON sig.id=se.signal_id
               WHERE s.id=%s""",
            (source_id,),
        ).fetchone()
        assert lineage is not None


def test_migration_is_idempotent(dsn: str) -> None:
    apply_migrations(dsn)
    assert apply_migrations(dsn) == []


def test_cross_tenant_reference_is_rejected(dsn: str, tenant: str) -> None:
    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            "INSERT INTO tenants(name) VALUES ('foreign-tenant') RETURNING id"
        ).fetchone()
        assert row is not None
        foreign_tenant = str(row[0])
        conn.commit()

    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("Local Account")

    with (
        TenantConnection(dsn, foreign_tenant, "tads_app").transaction() as conn,
        pytest.raises(psycopg.errors.RaiseException, match="cross-tenant"),
    ):
        conn.execute(
            "INSERT INTO organizations(tenant_id, account_id) VALUES (tads_tenant_id(), %s)",
            (account_id,),
        )


def test_all_tenant_tables_have_rls(dsn: str) -> None:
    apply_migrations(dsn)
    expected = {
        "accounts",
        "organizations",
        "domains",
        "sources",
        "source_snapshots",
        "observations",
        "canonical_events",
        "event_observations",
        "evidence",
        "relationships",
        "signals",
        "signal_evidence",
    }
    with psycopg.connect(dsn) as conn:
        rows = conn.execute(
            """SELECT relname, relrowsecurity
               FROM pg_class
               WHERE relname = ANY(%s)""",
            (list(expected),),
        ).fetchall()
    states = dict(rows)
    assert set(states) == expected
    assert states == {name: True for name in expected}
