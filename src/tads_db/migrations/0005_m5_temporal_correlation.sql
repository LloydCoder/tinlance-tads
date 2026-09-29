CREATE TABLE signal_correlations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    window_start timestamptz NOT NULL,
    window_end timestamptz NOT NULL,
    count integer NOT NULL CHECK (count >= 0),
    density numeric(7,6) NOT NULL CHECK (density BETWEEN 0 AND 1),
    diversity numeric(7,6) NOT NULL CHECK (diversity BETWEEN 0 AND 1),
    independence numeric(7,6) NOT NULL CHECK (independence BETWEEN 0 AND 1),
    momentum numeric(7,6) NOT NULL CHECK (momentum BETWEEN 0 AND 1),
    contradiction numeric(7,6) NOT NULL CHECK (contradiction BETWEEN 0 AND 1),
    rule_version text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (window_end > window_start)
);

CREATE INDEX signal_correlations_account_time_idx
    ON signal_correlations(tenant_id, account_id, window_end DESC);

ALTER TABLE signal_correlations ENABLE ROW LEVEL SECURITY;
CREATE POLICY signal_correlations_tenant_isolation ON signal_correlations
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER signal_correlations_account_tenant
BEFORE INSERT OR UPDATE ON signal_correlations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON signal_correlations TO tads_app;
