-- M11 feedback/evaluation persistence. Outcomes are immutable and time-ordered.
CREATE TABLE evaluation_outcomes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    opportunity_id uuid NOT NULL REFERENCES opportunities(id),
    prediction_at timestamptz NOT NULL,
    label_at timestamptz NOT NULL,
    outcome text NOT NULL CHECK (length(trim(outcome)) > 0),
    source text NOT NULL CHECK (length(trim(source)) > 0),
    policy_version text NOT NULL CHECK (length(trim(policy_version)) > 0),
    predicted_confidence numeric(7,6) NOT NULL CHECK (predicted_confidence BETWEEN 0 AND 1),
    observed_success boolean NOT NULL,
    value numeric,
    idempotency_key text NOT NULL CHECK (length(trim(idempotency_key)) > 0),
    recorded_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT evaluation_outcomes_temporal_order CHECK (label_at >= prediction_at)
);

CREATE UNIQUE INDEX evaluation_outcomes_idempotency_idx
    ON evaluation_outcomes(tenant_id, idempotency_key);

ALTER TABLE evaluation_outcomes ENABLE ROW LEVEL SECURITY;
CREATE POLICY evaluation_outcomes_tenant_isolation ON evaluation_outcomes
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER evaluation_outcomes_opportunity_tenant
BEFORE INSERT OR UPDATE ON evaluation_outcomes FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('opportunities','opportunity_id');

CREATE TRIGGER evaluation_outcomes_append_only
BEFORE UPDATE OR DELETE ON evaluation_outcomes FOR EACH ROW
EXECUTE FUNCTION tads_block_append_only_mutation();

REVOKE UPDATE, DELETE ON evaluation_outcomes FROM tads_app;
GRANT SELECT, INSERT ON evaluation_outcomes TO tads_app;
