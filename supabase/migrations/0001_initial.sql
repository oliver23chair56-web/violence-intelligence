-- Apply only to a separate Violence Intelligence Supabase project.
create extension if not exists pgcrypto;
create table public.incidents (
  id uuid primary key default gen_random_uuid(),
  source_system text not null,
  source_record_id text not null,
  occurred_at timestamptz,
  city text not null,
  state text not null,
  offense_type text,
  community_area text,
  description text,
  raw_record jsonb not null default '{}'::jsonb,
  published boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(source_system,source_record_id)
);
create table public.sources (
 id uuid primary key default gen_random_uuid(),
 source_url text not null unique,
 publisher text not null,
 retrieved_at timestamptz not null default now()
);
create table public.incident_sources (
 incident_id uuid not null references public.incidents(id) on delete cascade,
 source_id uuid not null references public.sources(id) on delete cascade,
 primary key(incident_id,source_id)
);
create table public.classifications (
 id uuid primary key default gen_random_uuid(),
 incident_id uuid not null references public.incidents(id) on delete cascade,
 category text not null check(category in ('expressive','instrumental','mixed','undetermined')),
 evidence_summary text,
 review_status text not null default 'pending' check(review_status in ('pending','approved','rejected')),
 created_at timestamptz not null default now()
);
create index on public.incidents(occurred_at);
create index on public.incidents(city,state);
alter table public.incidents enable row level security;
alter table public.sources enable row level security;
alter table public.incident_sources enable row level security;
alter table public.classifications enable row level security;
-- No public policies: default deny until the publishing API and access rules are reviewed.
