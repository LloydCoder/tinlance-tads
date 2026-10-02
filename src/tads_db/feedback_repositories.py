"""Tenant-scoped append-only feedback persistence."""

from datetime import datetime
from typing import Any

from psycopg import Connection


class EvaluationOutcomeRepository:
    def __init__(self, conn: Connection[Any]):
        self.conn = conn

    def create(
        self,
        opportunity_id: str,
        prediction_at: datetime,
        label_at: datetime,
        outcome: str,
        source: str,
        policy_version: str,
        predicted_confidence: float,
        observed_success: bool,
        idempotency_key: str,
        value: float | None = None,
    ) -> str:
        if label_at < prediction_at:
            raise ValueError("label_at cannot precede prediction_at")
        if not 0.0 <= predicted_confidence <= 1.0:
            raise ValueError("predicted_confidence must be between 0 and 1")
        if not idempotency_key.strip():
            raise ValueError("idempotency_key is required")
        row = self.conn.execute(
            """INSERT INTO evaluation_outcomes(
                   tenant_id,opportunity_id,prediction_at,label_at,outcome,source,
                   policy_version,predicted_confidence,observed_success,idempotency_key,value
               ) VALUES (
                   tads_tenant_id(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
               )
               ON CONFLICT (tenant_id,idempotency_key) DO NOTHING
               RETURNING id""",
            (
                opportunity_id,
                prediction_at,
                label_at,
                outcome,
                source,
                policy_version,
                predicted_confidence,
                observed_success,
                idempotency_key,
                value,
            ),
        ).fetchone()
        if row is None:
            existing = self.conn.execute(
                """SELECT id FROM evaluation_outcomes
                   WHERE tenant_id = tads_tenant_id() AND idempotency_key = %s""",
                (idempotency_key,),
            ).fetchone()
            if existing is None:
                raise RuntimeError("evaluation outcome insert was not persisted")
            return str(existing[0])
        return str(row[0])
