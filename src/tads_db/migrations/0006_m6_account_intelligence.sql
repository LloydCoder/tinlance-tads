CREATE TABLE account_states (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    account_id uuid NOT NULL REFERENCES accounts(id),
    signal_strength numeric(7,6) NOT NULL CHECK (signal_strength BETWEEN 0 AND 1),
    signal_diversity numeric(7,6) NOT NULL CHECK (signal_diversity BETWEEN 0 AND 1),
    momentum numeric(7,6) NOT NULL CHECK (momentum BETWEEN 0 AND 1),
    negative_evidence numeric(7,6) NOT NULL CHECK (negative_evidence BETWEEN 0 AND 1),
    data_confidence numeric(7,6) NOT NULL CHECK (data_confidence BETWEEN 0 AND 1),
    active_signal_count integer NOT NULL CHECK (active_signal_count >= 0),
    state_version text NOT NULL,
    drivers jsonb NOT NULL DEFAULT '[]'::jsonb,
    calculated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, account_id, state_version, calculated_at)
);

CREATE INDEX account_states_timeline_idx
    ON account_states(tenant_id, account_id, calculated_at DESC);

ALTER TABLE account_states ENABLE ROW LEVEL SECURITY;
CREATE POLICY account_states_tenant_isolation ON account_states
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER account_states_account_tenant
BEFORE INSERT OR UPDATE ON account_states FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON account_states TO tads_app;
