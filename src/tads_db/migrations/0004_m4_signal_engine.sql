CREATE TABLE signal_detections (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    observation_id uuid NOT NULL REFERENCES observations(id),
    signal_kind text NOT NULL,
    signal_subtype text NOT NULL,
    taxonomy_version text NOT NULL,
    state text NOT NULL CHECK (state IN ('candidate','validated','expired','rejected')),
    strength numeric(5,4) NOT NULL CHECK (strength BETWEEN 0 AND 1),
    freshness numeric(5,4) NOT NULL CHECK (freshness BETWEEN 0 AND 1),
    reliability numeric(5,4) NOT NULL CHECK (reliability BETWEEN 0 AND 1),
    quality numeric(7,6) GENERATED ALWAYS AS (strength * freshness * reliability) STORED,
    rationale jsonb NOT NULL DEFAULT '[]'::jsonb,
    detected_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX signal_detections_dedup_idx
    ON signal_detections(tenant_id, observation_id, signal_kind, signal_subtype, taxonomy_version);
CREATE INDEX signal_detections_timeline_idx
    ON signal_detections(tenant_id, detected_at DESC);

ALTER TABLE signal_detections ENABLE ROW LEVEL SECURITY;
CREATE POLICY signal_detections_tenant_isolation ON signal_detections
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER signal_detections_observation_tenant
BEFORE INSERT OR UPDATE ON signal_detections FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('observations','observation_id');

CREATE TABLE signal_detection_evidence (
    tenant_id uuid NOT NULL REFERENCES tenants(id),
    detection_id uuid NOT NULL REFERENCES signal_detections(id),
    evidence_id uuid NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (tenant_id, detection_id, evidence_id)
);

ALTER TABLE signal_detection_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY signal_detection_evidence_tenant_isolation ON signal_detection_evidence
    USING (tenant_id = tads_tenant_id()) WITH CHECK (tenant_id = tads_tenant_id());

CREATE TRIGGER signal_detection_evidence_detection_tenant
BEFORE INSERT OR UPDATE ON signal_detection_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('signal_detections','detection_id');

CREATE TRIGGER signal_detection_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON signal_detection_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

GRANT SELECT, INSERT, UPDATE, DELETE ON signal_detections, signal_detection_evidence TO tads_app;
