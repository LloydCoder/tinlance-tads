CREATE TABLE enrichment_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    provider text NOT NULL CHECK (length(trim(provider)) > 0),
    provider_version text NOT NULL CHECK (length(trim(provider_version)) > 0),
    purpose text NOT NULL CHECK (length(trim(purpose)) > 0),
    requested_fields jsonb NOT NULL DEFAULT '[]'::jsonb
        CHECK (jsonb_typeof(requested_fields) = 'array' AND jsonb_array_length(requested_fields) > 0),
    evidence_ids jsonb NOT NULL DEFAULT '[]'::jsonb
        CHECK (jsonb_typeof(evidence_ids) = 'array' AND jsonb_array_length(evidence_ids) > 0),
    facts jsonb NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(facts) = 'array'),
    unknowns jsonb NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(unknowns) = 'array'),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE enrichment_run_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    enrichment_run_id uuid NOT NULL REFERENCES enrichment_runs(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, enrichment_run_id, evidence_id)
);

CREATE TABLE opportunity_handoffs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    opportunity_id uuid NOT NULL REFERENCES opportunities(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    score numeric(7,6) NOT NULL CHECK (score BETWEEN 0 AND 1),
    confidence numeric(7,6) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    hypothesis text NOT NULL CHECK (length(trim(hypothesis)) > 0),
    evidence_ids jsonb NOT NULL DEFAULT '[]'::jsonb
        CHECK (jsonb_typeof(evidence_ids) = 'array' AND jsonb_array_length(evidence_ids) > 0),
    recommended_persona text,
    recommended_angle text,
    timing text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE opportunity_handoff_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    handoff_id uuid NOT NULL REFERENCES opportunity_handoffs(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, handoff_id, evidence_id)
);

ALTER TABLE enrichment_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY enrichment_runs_tenant_isolation ON enrichment_runs
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());
ALTER TABLE enrichment_run_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY enrichment_run_evidence_tenant_isolation ON enrichment_run_evidence
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

ALTER TABLE opportunity_handoffs ENABLE ROW LEVEL SECURITY;
CREATE POLICY opportunity_handoffs_tenant_isolation ON opportunity_handoffs
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());
ALTER TABLE opportunity_handoff_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY opportunity_handoff_evidence_tenant_isolation ON opportunity_handoff_evidence
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER enrichment_runs_account_tenant
BEFORE INSERT OR UPDATE ON enrichment_runs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER enrichment_run_evidence_run_tenant
BEFORE INSERT OR UPDATE ON enrichment_run_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('enrichment_runs','enrichment_run_id');
CREATE TRIGGER enrichment_run_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON enrichment_run_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

CREATE TRIGGER opportunity_handoffs_opportunity_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoffs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('opportunities','opportunity_id');
CREATE TRIGGER opportunity_handoffs_account_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoffs FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER opportunity_handoff_evidence_handoff_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoff_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('opportunity_handoffs','handoff_id');
CREATE TRIGGER opportunity_handoff_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON opportunity_handoff_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

GRANT SELECT, INSERT ON enrichment_runs, enrichment_run_evidence,
    opportunity_handoffs, opportunity_handoff_evidence TO tads_app;
