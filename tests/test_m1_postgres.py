"""Integration tests for the M1 PostgreSQL kernel."""

import os
from datetime import UTC, datetime

import psycopg
import pytest

from tads_db import (
    AccountRepository,
    AccountStateRepository,
    AgentSpecRepository,
    CorrelationRepository,
    EventRepository,
    EvidenceRepository,
    ObservationRepository,
    OpportunityRepository,
    SignalDetectionRepository,
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
        with (
            pytest.raises(psycopg.errors.InsufficientPrivilege),
            conn.transaction(),
        ):
            conn.execute(
                "UPDATE evidence SET excerpt='tampered' WHERE id=%s",
                (evidence_id,),
            )
        with (
            pytest.raises(psycopg.errors.InsufficientPrivilege),
            conn.transaction(),
        ):
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
               WHERE relname = ANY(%s) AND relnamespace = 'public'::regnamespace""",
            (list(expected),),
        ).fetchall()
    states = dict(rows)
    assert set(states) == expected
    assert states == {name: True for name in expected}


def test_signal_detection_is_idempotent_and_tenant_scoped(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        source_id = SourceRepository(conn).create(
            "test", "signal-source", "public_structured", "api", "terms"
        )
        snapshot_id = SourceRepository(conn).create_snapshot(
            source_id, datetime.now(UTC), "sha256:m4-snapshot"
        )
        observation_id = ObservationRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:m4-observation",
            {"provider": "greenhouse", "title": "Security Engineer"},
        )
        evidence_id = EvidenceRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:m4-evidence",
            "m4",
            "1",
            0.95,
            observation_id,
        )
        repo = SignalDetectionRepository(conn)
        first = repo.create(
            observation_id,
            "hiring",
            "job_posting",
            "m4-v1",
            "validated",
            0.8,
            1.0,
            0.9,
            ("structured hiring source",),
            (evidence_id,),
        )
        second = repo.create(
            observation_id,
            "hiring",
            "job_posting",
            "m4-v1",
            "validated",
            0.8,
            1.0,
            0.9,
            ("structured hiring source",),
            (evidence_id,),
        )
        assert first is not None
        assert second is None
        row = conn.execute(
            """SELECT sd.quality, sde.evidence_id
               FROM signal_detections sd
               JOIN signal_detection_evidence sde ON sde.detection_id=sd.id
               WHERE sd.id=%s""",
            (first,),
        ).fetchone()
        assert row is not None
        assert float(row[0]) == pytest.approx(0.72)
        assert str(row[1]) == evidence_id


def test_m4_signal_detection_has_rls(dsn: str) -> None:
    apply_migrations(dsn)
    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            """SELECT relrowsecurity FROM pg_class
               WHERE relname='signal_detections'
                 AND relnamespace='public'::regnamespace"""
        ).fetchone()
    assert row == (True,)


def test_m5_correlation_persistence_is_tenant_scoped(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("Correlation Account")
        source_id = SourceRepository(conn).create("test", "m5", "public_structured", "api", "terms")
        snapshot_id = SourceRepository(conn).create_snapshot(
            source_id, datetime.now(UTC), "sha256:m5"
        )
        evidence_id = EvidenceRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:m5e",
            "m5",
            "1",
            1.0,
        )
        correlation_id = CorrelationRepository(conn).create(
            account_id,
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 1, 8, tzinfo=UTC),
            3,
            0.4,
            0.66,
            0.66,
            0.8,
            0.33,
            "m5-v1",
            (evidence_id,),
        )
        row = conn.execute(
            "SELECT count, rule_version FROM signal_correlations WHERE id=%s",
            (correlation_id,),
        ).fetchone()
        assert row == (3, "m5-v1")
        assert conn.execute(
            "SELECT count(*) FROM signal_correlation_evidence WHERE correlation_id=%s",
            (correlation_id,),
        ).fetchone() == (1,)


def test_m6_account_state_persistence(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("State Account")
        source_id = SourceRepository(conn).create("test", "m6", "public_structured", "api", "terms")
        snapshot_id = SourceRepository(conn).create_snapshot(
            source_id, datetime.now(UTC), "sha256:m6"
        )
        evidence_id = EvidenceRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:m6e",
            "m6",
            "1",
            1.0,
        )
        state_id = AccountStateRepository(conn).create(
            account_id,
            0.7,
            0.6,
            0.8,
            0.1,
            0.9,
            4,
            "m6-v1",
            ("hiring:quality=0.90",),
            (evidence_id,),
        )
        row = conn.execute(
            "SELECT active_signal_count, state_version FROM account_states WHERE id=%s",
            (state_id,),
        ).fetchone()
        assert row == (4, "m6-v1")
        assert conn.execute(
            "SELECT count(*) FROM account_state_evidence WHERE account_state_id=%s",
            (state_id,),
        ).fetchone() == (1,)


def test_m7_opportunity_persistence(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("Opportunity Account")
        source_id = SourceRepository(conn).create("test", "m7", "public_structured", "api", "terms")
        snapshot_id = SourceRepository(conn).create_snapshot(
            source_id, datetime.now(UTC), "sha256:m7"
        )
        evidence_id = EvidenceRepository(conn).create(
            source_id,
            snapshot_id,
            datetime.now(UTC),
            "sha256:m7e",
            "m7",
            "1",
            1.0,
        )
        opportunity_id = OpportunityRepository(conn).create(
            account_id,
            0.8,
            0.75,
            1.0,
            0.9,
            0.8,
            0.0,
            "m7-v1",
            "Evidence-backed attention hypothesis.",
            "CREATE_OPPORTUNITY",
            ("ICP industry match",),
            ("employee count",),
            (evidence_id,),
        )
        row = conn.execute(
            "SELECT recommendation, score_version FROM opportunities WHERE id=%s",
            (opportunity_id,),
        ).fetchone()
        assert row == ("CREATE_OPPORTUNITY", "m7-v1")
        assert conn.execute(
            "SELECT count(*) FROM opportunity_evidence WHERE opportunity_id=%s",
            (opportunity_id,),
        ).fetchone() == (1,)


def test_m8_agent_spec_persistence(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        spec_id = AgentSpecRepository(conn).create(
            "signal_researcher",
            "Verify evidence.",
            "medium",
            True,
            12,
            True,
            [{"name": "source_reader", "read_only": True}],
            ["send_outreach", "expose_secrets"],
            ["prompt injection"],
            ["evidence precision"],
        )
        row = conn.execute(
            "SELECT required_evidence, max_steps FROM agent_specs WHERE id=%s",
            (spec_id,),
        ).fetchone()
        assert row == (True, 12)
