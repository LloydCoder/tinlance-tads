"""PostgreSQL integration coverage for immutable M11 evaluation outcomes."""

import os
from datetime import UTC, datetime

import psycopg
import pytest

from tads_db import (
    AccountRepository,
    EvaluationOutcomeRepository,
    EvidenceRepository,
    ObservationRepository,
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
            "INSERT INTO tenants(name) VALUES ('m11-tenant') RETURNING id"
        ).fetchone()
        assert row is not None
        conn.commit()
        return str(row[0])


def _opportunity(conn: psycopg.Connection[object]) -> str:
    account_id = AccountRepository(conn).create("M11 Evaluation Account")
    source_id = SourceRepository(conn).create("test", "m11", "public_structured", "api", "terms")
    snapshot_id = SourceRepository(conn).create_snapshot(
        source_id, datetime(2026, 1, 1, tzinfo=UTC), "sha256:m11-snapshot"
    )
    observation_id = ObservationRepository(conn).create(
        source_id,
        snapshot_id,
        datetime(2026, 1, 1, tzinfo=UTC),
        "sha256:m11-observation",
        {"title": "Security Engineer"},
    )
    evidence_id = EvidenceRepository(conn).create(
        source_id,
        snapshot_id,
        datetime(2026, 1, 1, tzinfo=UTC),
        "sha256:m11-evidence",
        "test",
        "1",
        1.0,
        observation_id,
        "job:title",
        "Security Engineer",
    )
    return OpportunityRepository(conn).create(
        account_id,
        0.8,
        0.7,
        0.9,
        0.8,
        0.8,
        0.0,
        "m7-v1",
        "Evidence-backed evaluation opportunity.",
        "CREATE_OPPORTUNITY",
        ("ICP fit",),
        (),
        (evidence_id,),
    )


def test_evaluation_outcome_is_idempotent_and_tenant_scoped(dsn: str, tenant: str) -> None:
    prediction_at = datetime(2026, 1, 1, tzinfo=UTC)
    label_at = datetime(2026, 2, 1, tzinfo=UTC)
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        opportunity_id = _opportunity(conn)
        repository = EvaluationOutcomeRepository(conn)
        first = repository.create(
            opportunity_id,
            prediction_at,
            label_at,
            "won",
            "crm",
            "m11-v1",
            0.8,
            True,
            "outcome-1",
        )
        second = repository.create(
            opportunity_id,
            prediction_at,
            label_at,
            "won",
            "crm",
            "m11-v1",
            0.8,
            True,
            "outcome-1",
        )
        assert first == second


def test_database_rejects_temporal_leakage(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        opportunity_id = _opportunity(conn)
        with pytest.raises(psycopg.errors.CheckViolation, match="evaluation_outcomes"):
            conn.execute(
                """INSERT INTO evaluation_outcomes(
                       tenant_id,opportunity_id,prediction_at,label_at,outcome,source,
                       policy_version,predicted_confidence,observed_success,idempotency_key
                   ) VALUES (
                       tads_tenant_id(),%s,%s,%s,'won','crm','m11-v1',0.8,true,'bad-order'
                   )""",
                (
                    opportunity_id,
                    datetime(2026, 2, 1, tzinfo=UTC),
                    datetime(2026, 1, 1, tzinfo=UTC),
                ),
            )


def test_evaluation_outcomes_are_append_only_for_application_role(dsn: str, tenant: str) -> None:
    with TenantConnection(dsn, tenant, "tads_app").transaction() as conn:
        opportunity_id = _opportunity(conn)
        outcome_id = EvaluationOutcomeRepository(conn).create(
            opportunity_id,
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 2, 1, tzinfo=UTC),
            "lost",
            "crm",
            "m11-v1",
            0.4,
            False,
            "outcome-immutable",
        )
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute(
                "DELETE FROM evaluation_outcomes WHERE id = %s",
                (outcome_id,),
            )


def test_evaluation_outcomes_have_rls(dsn: str) -> None:
    apply_migrations(dsn)
    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            """SELECT relrowsecurity
               FROM pg_class
               WHERE relname = 'evaluation_outcomes'
                 AND relnamespace = 'public'::regnamespace"""
        ).fetchone()
    assert row == (True,)
