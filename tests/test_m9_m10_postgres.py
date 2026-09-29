"""PostgreSQL integration coverage for M9/M10 tenant and evidence boundaries."""

import os
from datetime import UTC, datetime

import psycopg
import pytest

from tads_db import (
    AccountRepository,
    EnrichmentRunRepository,
    EvidenceRepository,
    OpportunityHandoffRepository,
    OpportunityRepository,
    ObservationRepository,
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
        row = conn.execute("INSERT INTO tenants(name) VALUES ('m9-m10-tenant') RETURNING id").fetchone()
        assert row is not None
        conn.commit()
        return str(row[0])


def test_m9_m10_persist_evidence_and_tenant_lineage(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        account_id = AccountRepository(conn).create("Integration Account")
        source_id = SourceRepository(conn).create("test", "integration", "public", "api", "terms")
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
        enrichment_id = EnrichmentRunRepository(conn).create(
            account_id,
            "reconos-contract",
            "v1",
            "validate technology need",
            ("technology",),
            (evidence_id,),
            ({"technology": "postgres"},),
            ("ownership",),
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
        )
        assert enrichment_id and handoff_id

    with psycopg.connect(dsn) as conn:
        enrichment_count = conn.execute(
            "SELECT count(*) FROM enrichment_run_evidence WHERE enrichment_run_id = %s",
            (enrichment_id,),
        ).fetchone()
        handoff_count = conn.execute(
            "SELECT count(*) FROM opportunity_handoff_evidence WHERE handoff_id = %s",
            (handoff_id,),
        ).fetchone()
        assert enrichment_count == (1,)
        assert handoff_count == (1,)
