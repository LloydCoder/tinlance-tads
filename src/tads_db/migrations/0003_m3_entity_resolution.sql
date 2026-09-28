CREATE TABLE entity_aliases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    alias text NOT NULL,
    normalized_alias text NOT NULL,
    evidence_id uuid REFERENCES evidence(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, organization_id, normalized_alias)
);

CREATE TABLE resolution_candidates (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    input_name text,
    input_domain text,
    name_similarity numeric(5,4) NOT NULL CHECK (name_similarity BETWEEN 0 AND 1),
    domain_exact boolean NOT NULL DEFAULT false,
    alias_exact boolean NOT NULL DEFAULT false,
    confidence numeric(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    state text NOT NULL CHECK (state IN ('matched','probable','ambiguous','unresolved','rejected')),
    rationale jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_id uuid REFERENCES evidence(id),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX resolution_candidates_input_idx ON resolution_candidates(tenant_id, input_domain, input_name);
CREATE INDEX entity_aliases_lookup_idx ON entity_aliases(tenant_id, normalized_alias);

ALTER TABLE entity_aliases ENABLE ROW LEVEL SECURITY;
CREATE POLICY entity_aliases_tenant_isolation ON entity_aliases
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

ALTER TABLE resolution_candidates ENABLE ROW LEVEL SECURITY;
CREATE POLICY resolution_candidates_tenant_isolation ON resolution_candidates
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER entity_aliases_org_tenant
BEFORE INSERT OR UPDATE ON entity_aliases FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('organizations','organization_id');

CREATE TRIGGER entity_aliases_evidence_tenant
BEFORE INSERT OR UPDATE ON entity_aliases FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

CREATE TRIGGER resolution_candidates_org_tenant
BEFORE INSERT OR UPDATE ON resolution_candidates FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('organizations','organization_id');

CREATE TRIGGER resolution_candidates_evidence_tenant
BEFORE INSERT OR UPDATE ON resolution_candidates FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON entity_aliases, resolution_candidates TO tads_app;
