"""Tenant-scoped persistence for M9/M10 integration contracts."""

from collections.abc import Sequence
from typing import Any

from psycopg import Connection
from psycopg.types.json import Jsonb


class EnrichmentRunRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        account_id: str,
        provider: str,
        provider_version: str,
        purpose: str,
        requested_fields: Sequence[str],
        evidence_ids: Sequence[str],
        facts: Sequence[dict[str, Any]],
        unknowns: Sequence[str],
    ) -> str:
        if not requested_fields:
            raise ValueError("enrichment request must contain fields")
        if not evidence_ids:
            raise ValueError("enrichment result requires evidence")
        row = self.conn.execute(
            """INSERT INTO enrichment_runs(
                   tenant_id,account_id,provider,provider_version,purpose,requested_fields,
                   evidence_ids,facts,unknowns
               ) VALUES (tads_tenant_id(),%s,%s,%s,%s,%s,%s,%s,%s)
               RETURNING id""",
            (
                account_id,
                provider,
                provider_version,
                purpose,
                Jsonb(list(requested_fields)),
                Jsonb(list(evidence_ids)),
                Jsonb(list(facts)),
                Jsonb(list(unknowns)),
            ),
        ).fetchone()
        assert row is not None
        run_id = str(row[0])
        for evidence_id in evidence_ids:
            self.conn.execute(
                """INSERT INTO enrichment_run_evidence(
                       tenant_id,enrichment_run_id,evidence_id
                   ) VALUES (tads_tenant_id(),%s,%s)""",
                (run_id, evidence_id),
            )
        return run_id


class OpportunityHandoffRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        opportunity_id: str,
        account_id: str,
        score: float,
        confidence: float,
        hypothesis: str,
        evidence_ids: Sequence[str],
        recommended_persona: str | None,
        recommended_angle: str | None,
        timing: str | None,
    ) -> str:
        if not evidence_ids:
            raise ValueError("opportunity handoff requires evidence")
        if not 0.0 <= score <= 1.0 or not 0.0 <= confidence <= 1.0:
            raise ValueError("score and confidence must be between 0 and 1")
        row = self.conn.execute(
            """INSERT INTO opportunity_handoffs(
                   tenant_id,opportunity_id,account_id,score,confidence,hypothesis,
                   evidence_ids,recommended_persona,recommended_angle,timing
               ) VALUES (tads_tenant_id(),%s,%s,%s,%s,%s,%s,%s,%s,%s)
               RETURNING id""",
            (
                opportunity_id,
                account_id,
                score,
                confidence,
                hypothesis,
                Jsonb(list(evidence_ids)),
                recommended_persona,
                recommended_angle,
                timing,
            ),
        ).fetchone()
        assert row is not None
        handoff_id = str(row[0])
        for evidence_id in evidence_ids:
            self.conn.execute(
                """INSERT INTO opportunity_handoff_evidence(
                       tenant_id,handoff_id,evidence_id
                   ) VALUES (tads_tenant_id(),%s,%s)""",
                (handoff_id, evidence_id),
            )
        return handoff_id
