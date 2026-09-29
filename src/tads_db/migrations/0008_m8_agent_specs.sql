CREATE TABLE agent_specs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    name text NOT NULL,
    purpose text NOT NULL,
    risk text NOT NULL CHECK (risk IN ('low','medium','high')),
    required_evidence boolean NOT NULL,
    max_steps integer NOT NULL CHECK (max_steps > 0),
    requires_human_approval boolean NOT NULL,
    tools jsonb NOT NULL DEFAULT '[]'::jsonb,
    prohibited_actions jsonb NOT NULL DEFAULT '[]'::jsonb,
    failure_modes jsonb NOT NULL DEFAULT '[]'::jsonb,
    eval_criteria jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, name)
);

ALTER TABLE agent_specs ENABLE ROW LEVEL SECURITY;
CREATE POLICY agent_specs_tenant_isolation ON agent_specs
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

GRANT SELECT, INSERT, UPDATE, DELETE ON agent_specs TO tads_app;
