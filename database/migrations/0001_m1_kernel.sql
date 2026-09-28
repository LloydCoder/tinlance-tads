CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE tenants (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL CHECK (length(trim(name)) > 0), created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE accounts (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), canonical_name text NOT NULL CHECK (length(trim(canonical_name)) > 0), status text NOT NULL DEFAULT 'active', created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), UNIQUE (tenant_id, canonical_name));
CREATE TABLE organizations (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), account_id uuid NOT NULL REFERENCES accounts(id), legal_name text, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE domains (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), account_id uuid NOT NULL REFERENCES accounts(id), domain text NOT NULL, normalized_domain text NOT NULL, UNIQUE (tenant_id, normalized_domain));
CREATE TABLE sources (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), provider text NOT NULL, name text NOT NULL, source_class text NOT NULL, access_mechanism text NOT NULL, terms_reference text NOT NULL, trust_authority numeric(5,4) NOT NULL DEFAULT .5 CHECK (trust_authority BETWEEN 0 AND 1), trust_directness numeric(5,4) NOT NULL DEFAULT .5 CHECK (trust_directness BETWEEN 0 AND 1), trust_historical_accuracy numeric(5,4) NOT NULL DEFAULT .5 CHECK (trust_historical_accuracy BETWEEN 0 AND 1), enabled boolean NOT NULL DEFAULT false, created_at timestamptz NOT NULL DEFAULT now(), UNIQUE (tenant_id, provider, name));
CREATE TABLE source_snapshots (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), source_id uuid NOT NULL REFERENCES sources(id), captured_at timestamptz NOT NULL, content_hash text NOT NULL, content_type text, byte_size bigint CHECK (byte_size IS NULL OR byte_size >= 0), storage_uri text, metadata jsonb NOT NULL DEFAULT '{}'::jsonb, UNIQUE (tenant_id, source_id, content_hash));
CREATE TABLE observations (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), source_id uuid NOT NULL REFERENCES sources(id), snapshot_id uuid NOT NULL REFERENCES source_snapshots(id), observed_at timestamptz NOT NULL, locator text, payload jsonb NOT NULL, content_hash text NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), UNIQUE (tenant_id, source_id, content_hash));
CREATE TABLE canonical_events (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), event_type text NOT NULL, occurred_at timestamptz, event_time_confidence numeric(5,4) NOT NULL DEFAULT .5 CHECK (event_time_confidence BETWEEN 0 AND 1), normalized_payload jsonb NOT NULL DEFAULT '{}'::jsonb, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE event_observations (tenant_id uuid NOT NULL REFERENCES tenants(id), event_id uuid NOT NULL REFERENCES canonical_events(id), observation_id uuid NOT NULL REFERENCES observations(id), PRIMARY KEY (tenant_id,event_id,observation_id));
CREATE TABLE evidence (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), source_id uuid NOT NULL REFERENCES sources(id), snapshot_id uuid NOT NULL REFERENCES source_snapshots(id), observation_id uuid REFERENCES observations(id), locator text, excerpt text, content_hash text NOT NULL, confidence numeric(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1), observed_at timestamptz NOT NULL, extractor text NOT NULL, extractor_version text NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE relationships (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), from_account_id uuid REFERENCES accounts(id), from_entity_type text NOT NULL, from_entity_id uuid NOT NULL, relationship_type text NOT NULL, to_entity_type text NOT NULL, to_entity_id uuid NOT NULL, confidence numeric(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1), evidence_id uuid REFERENCES evidence(id), created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE signals (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL REFERENCES tenants(id), account_id uuid NOT NULL REFERENCES accounts(id), event_id uuid NOT NULL REFERENCES canonical_events(id), signal_type text NOT NULL, signal_subtype text, confidence numeric(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1), relevance numeric(5,4) NOT NULL CHECK (relevance BETWEEN 0 AND 1), freshness numeric(5,4) NOT NULL CHECK (freshness BETWEEN 0 AND 1), reliability numeric(5,4) NOT NULL CHECK (reliability BETWEEN 0 AND 1), business_impact numeric(5,4) NOT NULL CHECK (business_impact BETWEEN 0 AND 1), direction smallint NOT NULL CHECK (direction IN (-1,0,1)), first_seen_at timestamptz NOT NULL, last_seen_at timestamptz NOT NULL, expires_at timestamptz, created_at timestamptz NOT NULL DEFAULT now(), CHECK (last_seen_at >= first_seen_at), CHECK (expires_at IS NULL OR expires_at >= first_seen_at));
CREATE TABLE signal_evidence (tenant_id uuid NOT NULL REFERENCES tenants(id), signal_id uuid NOT NULL REFERENCES signals(id), evidence_id uuid NOT NULL REFERENCES evidence(id), PRIMARY KEY (tenant_id,signal_id,evidence_id));

CREATE INDEX accounts_tenant_idx ON accounts(tenant_id);
CREATE INDEX observations_tenant_observed_idx ON observations(tenant_id,observed_at DESC);
CREATE INDEX events_tenant_occurred_idx ON canonical_events(tenant_id,occurred_at DESC);
CREATE INDEX signals_account_time_idx ON signals(tenant_id,account_id,last_seen_at DESC);
CREATE INDEX evidence_source_time_idx ON evidence(tenant_id,source_id,observed_at DESC);

CREATE OR REPLACE FUNCTION tads_touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN NEW.updated_at=now(); RETURN NEW; END $$;
CREATE TRIGGER accounts_touch_updated_at BEFORE UPDATE ON accounts FOR EACH ROW EXECUTE FUNCTION tads_touch_updated_at();

CREATE OR REPLACE FUNCTION tads_block_evidence_mutation() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'evidence is immutable'; END $$;
CREATE TRIGGER evidence_immutable BEFORE UPDATE OR DELETE ON evidence FOR EACH ROW EXECUTE FUNCTION tads_block_evidence_mutation();

CREATE OR REPLACE FUNCTION tads_tenant_id() RETURNS uuid LANGUAGE sql STABLE AS $$ SELECT NULLIF(current_setting('app.tenant_id',true),'')::uuid $$;

DO $$
DECLARE table_name text;
BEGIN
 FOREACH table_name IN ARRAY ARRAY['accounts','organizations','domains','sources','source_snapshots','observations','canonical_events','event_observations','evidence','relationships','signals','signal_evidence']
 LOOP
  EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY',table_name);
  EXECUTE format('CREATE POLICY %I_tenant_isolation ON %I USING (tenant_id=tads_tenant_id()) WITH CHECK (tenant_id=tads_tenant_id())',table_name,table_name);
 END LOOP;
END $$;

CREATE OR REPLACE FUNCTION tads_enforce_parent_tenant()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    parent_tenant uuid;
    parent_id uuid;
BEGIN
    parent_id := (to_jsonb(NEW) ->> TG_ARGV[1])::uuid;
    IF parent_id IS NULL THEN
        RETURN NEW;
    END IF;
    EXECUTE format('SELECT tenant_id FROM %I WHERE id = $1', TG_ARGV[0])
        INTO parent_tenant USING parent_id;
    IF parent_tenant IS NULL OR parent_tenant <> NEW.tenant_id THEN
        RAISE EXCEPTION 'cross-tenant reference rejected';
    END IF;
    RETURN NEW;
END $$;

CREATE TRIGGER organizations_account_tenant
BEFORE INSERT OR UPDATE ON organizations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER domains_account_tenant
BEFORE INSERT OR UPDATE ON domains FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER snapshots_source_tenant
BEFORE INSERT OR UPDATE ON source_snapshots FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('sources','source_id');
CREATE TRIGGER observations_source_tenant
BEFORE INSERT OR UPDATE ON observations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('sources','source_id');
CREATE TRIGGER observations_snapshot_tenant
BEFORE INSERT OR UPDATE ON observations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('source_snapshots','snapshot_id');
CREATE TRIGGER events_observation_tenant
BEFORE INSERT OR UPDATE ON event_observations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('canonical_events','event_id');
CREATE TRIGGER events_observation_source_tenant
BEFORE INSERT OR UPDATE ON event_observations FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('observations','observation_id');
CREATE TRIGGER evidence_source_tenant
BEFORE INSERT OR UPDATE ON evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('sources','source_id');
CREATE TRIGGER evidence_snapshot_tenant
BEFORE INSERT OR UPDATE ON evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('source_snapshots','snapshot_id');
CREATE TRIGGER evidence_observation_tenant
BEFORE INSERT OR UPDATE ON evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('observations','observation_id');
CREATE TRIGGER relationships_account_tenant
BEFORE INSERT OR UPDATE ON relationships FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','from_account_id');
CREATE TRIGGER relationships_evidence_tenant
BEFORE INSERT OR UPDATE ON relationships FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');
CREATE TRIGGER signals_account_tenant
BEFORE INSERT OR UPDATE ON signals FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('accounts','account_id');
CREATE TRIGGER signals_event_tenant
BEFORE INSERT OR UPDATE ON signals FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('canonical_events','event_id');
CREATE TRIGGER signal_evidence_signal_tenant
BEFORE INSERT OR UPDATE ON signal_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('signals','signal_id');
CREATE TRIGGER signal_evidence_evidence_tenant
BEFORE INSERT OR UPDATE ON signal_evidence FOR EACH ROW
EXECUTE FUNCTION tads_enforce_parent_tenant('evidence','evidence_id');

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'tads_app') THEN
        CREATE ROLE tads_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
    END IF;
END $$;

GRANT tads_app TO CURRENT_USER;
GRANT USAGE ON SCHEMA public TO tads_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON
    accounts, organizations, domains, sources, source_snapshots, observations,
    canonical_events, event_observations, evidence, relationships, signals, signal_evidence
TO tads_app;
