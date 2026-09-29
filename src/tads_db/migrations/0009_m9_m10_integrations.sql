CREATE TABLE enrichment_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    provider text NOT NULL,
    provider_version text NOT NULL,
    purpose text NOT NULL,
    requested_fields jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    facts jsonb NOT NULL DEFAULT '[]'::jsonb,
    unknowns jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE opportunity_handoffs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    opportunity_id uuid NOT NULL REFERENCES opportunities(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    score numeric(7,6) NOT NULL CHECK (score BETWEEN 0 AND 1),
    confidence numeric(7,6) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    hypothesis text NOT NULL,
    evidence_ids jsonb NOT NULL DEFAULT '[]'::jsonb,
    recommended_persona text,
    recommended_angle text,
    timing text,
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE enrichment_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY enrichment_runs_tenant_isolation ON enrichment_runs
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());
ALTER TABLE opportunity_handoffs ENABLE ROW LEVEL SECURITY;
CREATE POLICY opportunity_handoffs_tenant_isolation ON opportunity_handoffs
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER enrichment_runs_account_tenant
BEFORE INSERT OR UPDATE ON enrichment_runs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER opportunity_handoffs_opportunity_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoffs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('opportunities','opportunity_id');
CREATE TRIGGER opportunity_handoffs_account_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoffs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON enrichment_runs, opportunity_handoffs TO tads_app;
