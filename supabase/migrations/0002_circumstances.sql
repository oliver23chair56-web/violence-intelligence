-- 0002: circumstance database v1
-- Applies to the separate Violence Intelligence Supabase project (not Founder OS).
-- Design doc: research/circumstance-schema-v1.md
-- Taxonomy: research/escalation-taxonomy-v1.md
--
-- Principles:
--  1. Verbatim first: every circumstance code is stored exactly as the source
--     reported it. Mapping to motive/escalation lives in separate tables and
--     is always labelled as a signal, never as a fact about the incident.
--  2. Unknown is a value: missing circumstance data is stored as unknown and
--     published as its own share. Nothing is imputed.
--  3. No public read on incident-level rows (RLS default deny, as in 0001).
--     The public API serves aggregates only, from views that never expose
--     identifiers, locations, or narrative detail.
--  4. Human review gate: no motive signal or pathway is published until
--     review_status = 'approved'.

create extension if not exists pgcrypto;

-- Sources of circumstance data (one row per source table/file).
create table if not exists public.circumstance_sources (
  id uuid primary key default gen_random_uuid(),
  source_system text not null,          -- e.g. 'FBI_SHR', 'ISP_SHR', 'NIBRS', 'GVA'
  source_name text not null,            -- human name
  source_url text,
  coverage text,                        -- e.g. 'Illinois, 2018' / 'United States, 2018'
  grain text not null default 'incident', -- 'incident' or 'aggregate'
  retrieved_at timestamptz not null default now(),
  notes text,
  unique(source_system, source_name, coverage)
);

-- Incident-level circumstance codes, verbatim from the source.
create table if not exists public.incident_circumstances (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid references public.incidents(id) on delete cascade,
  -- For sources ingested before a matching incidents row exists, keep the
  -- source's own record id so the row is still traceable.
  source_system text not null,
  source_record_id text not null,
  circumstance_code text not null,      -- verbatim code, e.g. 'OTHER ARGUMENTS'
  source_label text,                    -- verbatim label as published
  source_family text,                   -- source's own grouping, if any
  is_unknown boolean not null default false,
  circumstance_source_id uuid references public.circumstance_sources(id),
  created_at timestamptz not null default now(),
  unique(source_system, source_record_id, circumstance_code)
);
create index if not exists idx_incident_circumstances_incident
  on public.incident_circumstances(incident_id);
create index if not exists idx_incident_circumstances_code
  on public.incident_circumstances(source_system, circumstance_code);

-- Motive signal for one incident: expressive/instrumental as a RESEARCH SIGNAL.
create table if not exists public.motive_signals (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid references public.incidents(id) on delete cascade,
  source_system text not null,
  source_record_id text not null,
  signal text not null check (signal in
    ('expressive_leaning','instrumental_leaning','mixed','indeterminate','unknown')),
  confidence text not null default 'low' check (confidence in ('low','medium','high')),
  basis_codes text[] not null default '{}',  -- circumstance codes that drove the signal
  evidence_summary text,                    -- what in the record supports it, in plain words
  review_status text not null default 'pending'
    check (review_status in ('pending','approved','rejected')),
  reviewed_by text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now(),
  unique(source_system, source_record_id)
);
create index if not exists idx_motive_signals_signal
  on public.motive_signals(signal, review_status);

-- Escalation pathway for one incident, coded against the taxonomy.
-- See research/escalation-taxonomy-v1.md. All array fields store taxonomy
-- terms verbatim; empty array means "not recorded", never "did not happen".
create table if not exists public.escalation_pathways (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid references public.incidents(id) on delete cascade,
  source_system text not null,
  source_record_id text not null,
  stage_reached int check (stage_reached between 1 and 8),
  trigger_type text check (trigger_type in
    ('status_challenge','resource_dispute','relationship_jealousy',
     'prior_grievance_retaliation','instrumental_objective',
     'mistaken_identity','chaos_accident','unknown')),
  misunderstanding_types text[] not null default '{}',
    -- taxonomy terms: misread_intent, misread_words, misread_audience,
    -- misread_capability, misread_relationship, no_face_saving_exit
  escalation_mechanisms text[] not null default '{}',
    -- audience_presence, alcohol_drugs, group_vs_individual, prior_history,
    -- weapon_visible, time_pressure, prior_incident_same_day
  deescalation_points text[] not null default '{}',
    -- stage_3_clarification, stage_4_third_party, stage_4_one_side_leaves,
    -- stage_5_interruption, none_observed
  retaliation_link_source_record_id text,   -- prior incident, if this was payback
  evidence_summary text,
  review_status text not null default 'pending'
    check (review_status in ('pending','approved','rejected')),
  reviewed_by text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now(),
  unique(source_system, source_record_id)
);
create index if not exists idx_escalation_pathways_trigger
  on public.escalation_pathways(trigger_type, review_status);

-- Row level security: default deny on all new tables (as in 0001).
-- Public read is granted only through aggregate views defined separately,
-- after review, and never on incident-level rows.
alter table public.circumstance_sources enable row level security;
alter table public.incident_circumstances enable row level security;
alter table public.motive_signals enable row level security;
alter table public.escalation_pathways enable row level security;
