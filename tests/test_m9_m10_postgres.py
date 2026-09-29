"""PostgreSQL integration coverage for M9/M10 tenant and evidence boundaries."""

import os
from datetime import UTC, datetime

import psycopg
import pytest

from tads_db import (
    AccountRepository,
    EnrichmentRunRepository,
    EvidenceRepository,
    ObservationRepository,
    OpportunityHandoffRepository,
    OpportunityRepository,
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
            "INSERT INTO tenants(name) VALUES ('m9-m10-tenant') RETURNING id"
        ).fetchone()
        assert row is not None
        conn.commit()
        return str(row[0])


def _fixture_lineage(conn: psycopg.Connection[object]) -> tuple[str, str, str]:
    account_id = AccountRepository(conn).create("Integration Account")
    source_id = SourceRepository(conn).create(
        "test", "integration", "public_structured", "api", "terms"
    )
    snapshot_id = SourceRepository(conn).create_snapshot(
        source_id, datetime.now(UTC), "sha256:m9m10-snapshot"
    )
    observation_id = ObservationRepository(conn).create(
        source_id,
        snapshot_id,
        datetime.now(UTC),
        "sha256:m9m10-observation",
        {"title": "Security Engineer"},
    )
    evidence_id = EvidenceRepository(conn).create(
        source_id,
        snapshot_id,
        datetime.now(UTC),
        "sha256:m9m10-evidence",
        "test",
        "1",
        1.0,
        observation_id,
        "job:title",
        "Security Engineer",
    )
    return account_id, evidence_id, snapshot_id


def test_m9_m10_persist_evidence_and_tenant_lineage(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id, evidence_id, _ = _fixture_lineage(conn)
        enrichment_id = EnrichmentRunRepository(conn).create(
            account_id,
            "reconos-contract",
            "v1",
            "validate technology need",
            ("technology",),
            (evidence_id,),
            ({"technology": "postgres"},),
            ("ownership",),
            request_id="req-1",
            response_id="resp-1",
        )
        opportunity_id = OpportunityRepository(conn).create(
            account_id,
            0.8,
            0.7,
            0.9,
            0.8,
            0.8,
            0.0,
            "m7-v1",
            "Evidence-backed attention hypothesis.",
            "CREATE_OPPORTUNITY",
            ("ICP fit",),
            (),
            (evidence_id,),
        )
        handoff_id = OpportunityHandoffRepository(conn).create(
            opportunity_id,
            account_id,
            0.8,
            0.7,
            "Evidence-backed attention hypothesis.",
            (evidence_id,),
            "security leader",
            "security engineering evidence",
            "now",
            datetime(2026, 12, 31, tzinfo=UTC),
            "handoff-1",
        )
        assert enrichment_id and handoff_id

    with psycopg.connect(dsn) as conn:
        assert conn.execute(
            "SELECT count(*) FROM enrichment_run_evidence WHERE enrichment_run_id = %s",
            (enrichment_id,),
        ).fetchone() == (1,)
        assert conn.execute(
            "SELECT count(*) FROM opportunity_handoff_evidence WHERE handoff_id = %s",
            (handoff_id,),
        ).fetchone() == (1,)


def test_m9_m10_evidence_snapshot_must_match_normalized_links(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id, evidence_id, _ = _fixture_lineage(conn)
        row = conn.execute(
            """INSERT INTO enrichment_runs(
                   tenant_id, account_id, provider, provider_version, purpose,
                   requested_fields, evidence_ids, facts, unknowns
               ) VALUES (
                   tads_tenant_id(), %s, 'reconos-contract', 'v1', 'lineage check',
                   '[\"technology\"]'::jsonb, %s::jsonb, '[]'::jsonb, '[]'::jsonb
               )
               RETURNING id""",
            (account_id, str([evidence_id]).replace("'", '"')),
        ).fetchone()
        assert row is not None
        with pytest.raises(
            psycopg.errors.RaiseException, match="snapshot does not match"
        ):
            conn.execute(
                "SET CONSTRAINTS enrichment_evidence_snapshot_consistent IMMEDIATE"
            )


def test_m9_m10_historical_rows_are_append_only_for_application_role(
    dsn: str, tenant: str
) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        _, evidence_id, _ = _fixture_lineage(conn)
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("DELETE FROM evidence WHERE id = %s", (evidence_id,))
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute(
                "UPDATE opportunities SET score = 0.1 WHERE id = %s",
                ("00000000-0000-0000-0000-000000000000",),
            )


def test_all_m9_m10_tables_have_rls(dsn: str) -> None:
    apply_migrations(dsn)
    expected = {
        "enrichment_runs",
        "enrichment_run_evidence",
        "opportunity_handoffs",
        "opportunity_handoff_evidence",
    }
    with psycopg.connect(dsn) as conn:
        rows = conn.execute(
            """SELECT relname, relrowsecurity
               FROM pg_class
               WHERE relname = ANY(%s) AND relnamespace = 'public'::regnamespace""",
            (list(expected),),
        ).fetchall()
    assert dict(rows) == {name: True for name in expected}
