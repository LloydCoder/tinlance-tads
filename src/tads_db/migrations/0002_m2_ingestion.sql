CREATE TABLE source_ingestion_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    source_id uuid NOT NULL REFERENCES sources(id),
    requested_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    status text NOT NULL CHECK (status IN ('running','succeeded','failed','partial')),
    request_key text NOT NULL,
    content_hash text,
    observation_count integer NOT NULL DEFAULT 0 CHECK (observation_count >= 0),
    error_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, source_id, request_key)
);
CREATE TABLE source_fetch_attempts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    ingestion_run_id uuid NOT NULL REFERENCES source_ingestion_runs(id),
    attempt_number integer NOT NULL CHECK (attempt_number > 0),
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    status text NOT NULL CHECK (status IN ('started','succeeded','failed')),
    http_status integer,
    content_type text,
    byte_size bigint CHECK (byte_size IS NULL OR byte_size >= 0),
    error_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, ingestion_run_id, attempt_number)
);
CREATE INDEX source_ingestion_runs_source_time_idx
    ON source_ingestion_runs(tenant_id, source_id, requested_at DESC);
CREATE INDEX source_fetch_attempts_run_idx
    ON source_fetch_attempts(tenant_id, ingestion_run_id, attempt_number);
ALTER TABLE source_ingestion_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY source_ingestion_runs_tenant_isolation
    ON source_ingestion_runs USING (tenant_id = tads_tenant_id())
    WITH CHECK (tenant_id = tads_tenant_id());
ALTER TABLE source_fetch_attempts ENABLE ROW LEVEL SECURITY;
CREATE POLICY source_fetch_attempts_tenant_isolation
    ON source_fetch_attempts USING (tenant_id = tads_tenant_id())
    WITH CHECK (tenant_id = tads_tenant_id());
CREATE TRIGGER source_ingestion_runs_source_tenant
BEFORE INSERT OR UPDATE ON source_ingestion_runs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('sources','source_id');
CREATE TRIGGER source_fetch_attempts_run_tenant
BEFORE INSERT OR UPDATE ON source_fetch_attempts FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('source_ingestion_runs','ingestion_run_id');
GRANT SELECT, INSERT, UPDATE, DELETE ON source_ingestion_runs, source_fetch_attempts TO tads_app;
