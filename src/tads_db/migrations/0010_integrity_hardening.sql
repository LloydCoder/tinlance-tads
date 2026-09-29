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
    expected_count integer;
    actual_count integer;
BEGIN
    SELECT count(*) INTO expected_count
    FROM jsonb_array_elements_text(NEW.evidence_ids);

    SELECT count(*) INTO actual_count
    FROM enrichment_run_evidence
    WHERE tenant_id = NEW.tenant_id
      AND enrichment_run_id = NEW.id;

    IF expected_count <> actual_count OR EXISTS (
        SELECT 1
        FROM jsonb_array_elements_text(NEW.evidence_ids) item
        WHERE NOT EXISTS (
            SELECT 1
            FROM enrichment_run_evidence link
            WHERE link.tenant_id = NEW.tenant_id
              AND link.enrichment_run_id = NEW.id
              AND link.evidence_id = item.value::uuid
        )
    ) THEN
        RAISE EXCEPTION 'enrichment evidence snapshot does not match normalized lineage';
    END IF;
    RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION tads_validate_handoff_evidence_snapshot()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    expected_count integer;
    actual_count integer;
BEGIN
    SELECT count(*) INTO expected_count
    FROM jsonb_array_elements_text(NEW.evidence_ids);

    SELECT count(*) INTO actual_count
    FROM opportunity_handoff_evidence
    WHERE tenant_id = NEW.tenant_id
      AND handoff_id = NEW.id;

    IF expected_count <> actual_count OR EXISTS (
        SELECT 1
        FROM jsonb_array_elements_text(NEW.evidence_ids) item
        WHERE NOT EXISTS (
            SELECT 1
            FROM opportunity_handoff_evidence link
            WHERE link.tenant_id = NEW.tenant_id
              AND link.handoff_id = NEW.id
              AND link.evidence_id = item.value::uuid
        )
    ) THEN
        RAISE EXCEPTION 'handoff evidence snapshot does not match normalized lineage';
    END IF;
    RETURN NEW;
END $$;

-- The JSON evidence identifiers are a portable snapshot only. The normalized
-- link tables are authoritative, and deferred triggers require exact equality
-- at transaction commit.
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

-- Historical artifacts cannot be rewritten or deleted through the application
-- role. This is defense in depth in addition to RLS and repository discipline.
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

-- These lifecycle tables legitimately change state.
GRANT UPDATE, DELETE ON source_ingestion_runs, source_fetch_attempts, signal_detections
TO tads_app;
