-- M5-M7 materialized intelligence lineage.
CREATE TABLE signal_correlation_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    correlation_id uuid NOT NULL REFERENCES signal_correlations(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, correlation_id, evidence_id)
);

CREATE TABLE account_state_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_state_id uuid NOT NULL REFERENCES account_states(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, account_state_id, evidence_id)
);

CREATE TABLE opportunity_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    opportunity_id uuid NOT NULL REFERENCES opportunities(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, opportunity_id, evidence_id)
);

DO $$
DECLARE
    table_name text;
BEGIN
    FOREACH table_name IN ARRAY ARRAY[
        'signal_correlation_evidence',
        'account_state_evidence',
        'opportunity_evidence'
    ]
    LOOP
        EXECUTE format(
            'ALTER TABLE %I ENABLE ROW LEVEL SECURITY',
            table_name
        );
        EXECUTE format(
            'CREATE POLICY %I_tenant_isolation ON %I USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id())',
            table_name,
            table_name
        );
    END LOOP;
END $$;

CREATE TRIGGER signal_correlation_evidence_correlation_tenant
BEFORE INSERT OR UPDATE ON signal_correlation_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('signal_correlations','correlation_id');

CREATE TRIGGER signal_correlation_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON signal_correlation_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

CREATE TRIGGER account_state_evidence_state_tenant
BEFORE INSERT OR UPDATE ON account_state_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('account_states','account_state_id');

CREATE TRIGGER account_state_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON account_state_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

CREATE TRIGGER opportunity_evidence_opportunity_tenant
BEFORE INSERT OR UPDATE ON opportunity_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('opportunities','opportunity_id');

CREATE TRIGGER opportunity_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON opportunity_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

GRANT SELECT, INSERT ON
    signal_correlation_evidence,
    account_state_evidence,
    opportunity_evidence
TO tads_app;
