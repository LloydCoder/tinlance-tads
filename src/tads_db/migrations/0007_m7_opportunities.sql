CREATE TABLE opportunities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    score numeric(7,6) NOT NULL CHECK (score BETWEEN 0 AND 1),
    confidence numeric(7,6) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    icp_fit numeric(7,6) NOT NULL CHECK (icp_fit BETWEEN 0 AND 1),
    evidence_strength numeric(7,6) NOT NULL CHECK (evidence_strength BETWEEN 0 AND 1),
    timing numeric(7,6) NOT NULL CHECK (timing BETWEEN 0 AND 1),
    negative_factor numeric(7,6) NOT NULL CHECK (negative_factor BETWEEN 0 AND 1),
    score_version text NOT NULL,
    hypothesis text NOT NULL,
    recommendation text NOT NULL CHECK (recommendation IN ('IGNORE','MONITOR','RESEARCH','ENRICH','QUEUE_FOR_FADEREACH','REQUEST_HUMAN_REVIEW','CREATE_OPPORTUNITY','EXPAND_RESEARCH')),
    reasons jsonb NOT NULL DEFAULT '[]'::jsonb,
    unknowns jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX opportunities_account_time_idx
    ON opportunities(tenant_id, account_id, created_at DESC);

ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;
CREATE POLICY opportunities_tenant_isolation ON opportunities
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER opportunities_account_tenant
BEFORE INSERT OR UPDATE ON opportunities FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON opportunities TO tads_app;
