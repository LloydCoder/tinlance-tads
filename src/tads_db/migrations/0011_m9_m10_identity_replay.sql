-- M9/M10 integration identity and replay hardening.
ALTER TABLE enrichment_runs
    ADD COLUMN request_id text,
    ADD COLUMN response_id text;

CREATE UNIQUE INDEX enrichment_runs_request_id_idx
    ON enrichment_runs(tenant_id, request_id)
    WHERE request_id IS NOT NULL;

ALTER TABLE opportunity_handoffs
    ADD COLUMN expires_at timestamptz,
    ADD COLUMN idempotency_key text NOT NULL
        CHECK (length(trim(idempotency_key)) > 0);

CREATE UNIQUE INDEX opportunity_handoffs_idempotency_idx
    ON opportunity_handoffs(tenant_id, idempotency_key);

ALTER TABLE opportunity_handoffs
    ADD CONSTRAINT opportunity_handoffs_expiry_check
    CHECK (expires_at IS NULL OR expires_at >= created_at);

REVOKE UPDATE, DELETE ON enrichment_runs, enrichment_run_evidence,
    opportunity_handoffs, opportunity_handoff_evidence FROM tads_app;
