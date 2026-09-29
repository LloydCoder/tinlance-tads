-- M10/M18 hardening: make historical intelligence append-only and bind
-- portable evidence snapshots to their authoritative normalized lineage.
CREATE OR REPLACE FUNCTION tads_block_append_only_mutation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '% is append-only; % is not permitted', TG_TABLE_NAME, TG_OP;
END $$;

CREATE OR REPLACE FUNCTION tads_validate_enrichment_evidence_snapshot()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    row_id uuid;
    row_tenant uuid;
    snapshot jsonb;
    expected_count integer;
    actual_count integer;
BEGIN
    IF TG_OP = 'DELETE' THEN
        row_id := OLD.enrichment_run_id;
        row_tenant := OLD.tenant_id;
        SELECT evidence_ids INTO snapshot
        FROM enrichment_runs
        WHERE id = row_id;
    ELSE
        IF TG_TABLE_NAME = 'enrichment_runs' THEN
            row_id := NEW.id;
            row_tenant := NEW.tenant_id;
            snapshot := NEW.evidence_ids;
        ELSE
            row_id := NEW.enrichment_run_id;
            row_tenant := NEW.tenant_id;
            SELECT evidence_ids INTO snapshot
            FROM enrichment_runs
            WHERE id = row_id;
        END IF;
    END IF;

    IF snapshot IS NULL THEN
        RETURN COALESCE(NEW, OLD);
    END IF;

    SELECT count(*) INTO expected_count
    FROM jsonb_array_elements_text(snapshot);

    SELECT count(*) INTO actual_count
    FROM enrichment_run_evidence
    WHERE tenant_id = row_tenant
      AND enrichment_run_id = row_id;

    IF expected_count <> actual_count OR EXISTS (
        SELECT 1
        FROM jsonb_array_elements_text(snapshot) item
        WHERE NOT EXISTS (
            SELECT 1
            FROM enrichment_run_evidence link
            WHERE link.tenant_id = row_tenant
              AND link.enrichment_run_id = row_id
              AND link.evidence_id = item.value::uuid
        )
    ) THEN
        RAISE EXCEPTION 'enrichment evidence snapshot does not match normalized lineage';
    END IF;
    RETURN COALESCE(NEW, OLD);
END $$;

CREATE OR REPLACE FUNCTION tads_validate_handoff_evidence_snapshot()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    row_id uuid;
    row_tenant uuid;
    snapshot jsonb;
    expected_count integer;
    actual_count integer;
BEGIN
    IF TG_OP = 'DELETE' THEN
        row_id := OLD.handoff_id;
        row_tenant := OLD.tenant_id;
        SELECT evidence_ids INTO snapshot
        FROM opportunity_handoffs
        WHERE id = row_id;
    ELSE
        IF TG_TABLE_NAME = 'opportunity_handoffs' THEN
            row_id := NEW.id;
            row_tenant := NEW.tenant_id;
            snapshot := NEW.evidence_ids;
        ELSE
            row_id := NEW.handoff_id;
            row_tenant := NEW.tenant_id;
            SELECT evidence_ids INTO snapshot
            FROM opportunity_handoffs
            WHERE id = row_id;
        END IF;
    END IF;

    IF snapshot IS NULL THEN
        RETURN COALESCE(NEW, OLD);
    END IF;

    SELECT count(*) INTO expected_count
    FROM jsonb_array_elements_text(snapshot);

    SELECT count(*) INTO actual_count
    FROM opportunity_handoff_evidence
    WHERE tenant_id = row_tenant
      AND handoff_id = row_id;

    IF expected_count <> actual_count OR EXISTS (
        SELECT 1
        FROM jsonb_array_elements_text(snapshot) item
        WHERE NOT EXISTS (
            SELECT 1
            FROM opportunity_handoff_evidence link
            WHERE link.tenant_id = row_tenant
              AND link.handoff_id = row_id
              AND link.evidence_id = item.value::uuid
        )
    ) THEN
        RAISE EXCEPTION 'handoff evidence snapshot does not match normalized lineage';
    END IF;
    RETURN COALESCE(NEW, OLD);
END $$;

CREATE CONSTRAINT TRIGGER enrichment_evidence_snapshot_consistent
AFTER INSERT OR UPDATE ON enrichment_runs
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION tads_validate_enrichment_evidence_snapshot();

CREATE CONSTRAINT TRIGGER enrichment_evidence_link_consistent
AFTER INSERT OR UPDATE OR DELETE ON enrichment_run_evidence
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION tads_validate_enrichment_evidence_snapshot();

CREATE CONSTRAINT TRIGGER handoff_evidence_snapshot_consistent
AFTER INSERT OR UPDATE ON opportunity_handoffs
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION tads_validate_handoff_evidence_snapshot();

CREATE CONSTRAINT TRIGGER handoff_evidence_link_consistent
AFTER INSERT OR UPDATE OR DELETE ON opportunity_handoff_evidence
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION tads_validate_handoff_evidence_snapshot();

DO $$
DECLARE
    table_name text;
BEGIN
    FOREACH table_name IN ARRAY ARRAY[
        'source_snapshots',
        'observations',
        'event_observations',
        'evidence',
        'relationships',
        'signals',
        'entity_aliases',
        'resolution_candidates',
        'signal_correlations',
        'account_states',
        'opportunities',
        'agent_specs',
        'enrichment_runs',
        'enrichment_run_evidence',
        'opportunity_handoffs',
        'opportunity_handoff_evidence'
    ]
    LOOP
        EXECUTE format(
            'DROP TRIGGER IF EXISTS %I ON %I',
            table_name || '_append_only',
            table_name
        );
        EXECUTE format(
            'CREATE TRIGGER %I BEFORE UPDATE OR DELETE ON %I FOR EACH ROW EXECUTE FUNCTION tads_block_append_only_mutation()',
            table_name || '_append_only',
            table_name
        );
        EXECUTE format(
            'REVOKE UPDATE, DELETE ON %I FROM tads_app',
            table_name
        );
    END LOOP;
END $$;

GRANT UPDATE, DELETE ON source_ingestion_runs, source_fetch_attempts, signal_detections
TO tads_app;
