-- ============================================================================
-- 0003_virs_compatibility.sql — VIRS Intake + Provenance Crosswalk v0.1
-- Violence Intelligence / Supabase project oqhupkfbelmrubctknzj
-- Author: Mortimer (lead developer) — 2026-11-08
-- Approved by Oliver Chairez 2026-11-08 (VIRS pilot approval package).
--
-- HOW IT IS APPLIED: paste into the Supabase SQL Editor and run.
-- NOTE ON NUMBERING: the local files 0001/0002 were applied the same way
-- (SQL Editor) and do NOT appear in supabase_migrations.schema_migrations,
-- which only tracks ChatGPT's timestamped CLI migrations (26 rows, latest
-- 20261108080207 as of 2026-11-08 02:37 CST). This file follows the same
-- pattern: local sequential numbering, applied by hand, recorded in
-- TAKEOVER-NOTES.md and in git (rebuild/supabase/migrations/).
--
-- NON-DESTRUCTIVE BY DESIGN: only ADDs. No DROP, no column removal, no
-- data changes, no RLS policy changes. Every statement is idempotent
-- (IF NOT EXISTS / DO-block guards) so re-running it is a no-op.
-- New tables get RLS enabled with NO policies (default deny), matching
-- the 0002 pattern. Nothing in this migration makes any row public.
--
-- WHAT IT FIXES (from docs/virs-schema-reconciliation.md):
--   (a) 0002 gap: `approved` without a reviewer was possible. Now a
--       review_status of 'approved' requires reviewed_by AND reviewed_at
--       on motive_signals and escalation_pathways.
--   (b) 0002 gap: basis_codes (a text[]) could not trace to evidence.
--       New junction tables link each signal/pathway to specific
--       claim_evidence rows.
--   (c) Source registry: circumstance_sources is declared the canonical
--       dataset registry (versioning columns added); case_source_references
--       stays the canonical per-case registry. No duplicate registry table.
--   (d) Linkage integrity: the pilot's "one victimization -> one event"
--       rule (verified 2026-11-08: 0 duplicated victimization IDs across
--       576 links) is now enforced by a partial unique index, and a
--       queryable integrity view backs the public metadata endpoint.
--   (e) Missingness: empty arrays mean "not recorded", never false.
--       Recorded as column comments so no reader infers otherwise.
--   (f) Canonical write path: motive_signals is THE store for motive
--       signals. classifications (older general table) must not be used
--       for public motive claims.
-- ============================================================================

-- --------------------------------------------------------------------------
-- (a) Reviewer gate: approved requires a reviewer and a timestamp.
-- Tables are empty today (0 rows), so the constraint cannot fail on
-- existing data. Guarded so a re-run is a no-op.
-- --------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'motive_signals_approved_requires_reviewer'
  ) THEN
    ALTER TABLE public.motive_signals
      ADD CONSTRAINT motive_signals_approved_requires_reviewer
      CHECK (
        review_status <> 'approved'
        OR (reviewed_by IS NOT NULL AND reviewed_by <> ''
            AND reviewed_at IS NOT NULL)
      );
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'escalation_pathways_approved_requires_reviewer'
  ) THEN
    ALTER TABLE public.escalation_pathways
      ADD CONSTRAINT escalation_pathways_approved_requires_reviewer
      CHECK (
        review_status <> 'approved'
        OR (reviewed_by IS NOT NULL AND reviewed_by <> ''
            AND reviewed_at IS NOT NULL)
      );
  END IF;
END $$;

-- Keep review_status values honest on the two 0002 interpretation tables.
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'motive_signals_review_status_values'
  ) THEN
    ALTER TABLE public.motive_signals
      ADD CONSTRAINT motive_signals_review_status_values
      CHECK (review_status IS NULL
             OR review_status IN ('pending', 'in_review', 'approved', 'rejected'));
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'escalation_pathways_review_status_values'
  ) THEN
    ALTER TABLE public.escalation_pathways
      ADD CONSTRAINT escalation_pathways_review_status_values
      CHECK (review_status IS NULL
             OR review_status IN ('pending', 'in_review', 'approved', 'rejected'));
  END IF;
END $$;

-- --------------------------------------------------------------------------
-- (b) Evidence trace: junction tables from each 0002 interpretation row
-- to the specific claim_evidence rows that support it.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.motive_signal_evidence (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  motive_signal_id uuid NOT NULL REFERENCES public.motive_signals (id) ON DELETE CASCADE,
  claim_evidence_id uuid NOT NULL REFERENCES public.claim_evidence (id) ON DELETE CASCADE,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (motive_signal_id, claim_evidence_id)
);

CREATE TABLE IF NOT EXISTS public.escalation_pathway_evidence (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  escalation_pathway_id uuid NOT NULL REFERENCES public.escalation_pathways (id) ON DELETE CASCADE,
  claim_evidence_id uuid NOT NULL REFERENCES public.claim_evidence (id) ON DELETE CASCADE,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (escalation_pathway_id, claim_evidence_id)
);

ALTER TABLE public.motive_signal_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.escalation_pathway_evidence ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE public.motive_signal_evidence IS
  'Evidence trace for motive_signals: one row per (signal, claim_evidence) pair. A motive signal with no rows here is unattributed and must not be published.';
COMMENT ON TABLE public.escalation_pathway_evidence IS
  'Evidence trace for escalation_pathways: one row per (pathway, claim_evidence) pair. A pathway with no rows here is unattributed and must not be published.';

-- --------------------------------------------------------------------------
-- (c) Source registry: version circumstance_sources; declare canonical paths.
-- --------------------------------------------------------------------------
ALTER TABLE public.circumstance_sources
  ADD COLUMN IF NOT EXISTS source_version text,
  ADD COLUMN IF NOT EXISTS file_sha256 text,
  ADD COLUMN IF NOT EXISTS record_count integer;

COMMENT ON TABLE public.circumstance_sources IS
  'CANONICAL dataset registry: one row per source dataset/file (versioned via source_version + file_sha256). Per-case source rows live in case_source_references — do not duplicate them here.';
COMMENT ON COLUMN public.circumstance_sources.source_version IS
  'Version of the source dataset as published by its owner (e.g. file date or release label). NULL = unversioned.';
COMMENT ON COLUMN public.circumstance_sources.file_sha256 IS
  'SHA-256 of the source file as ingested, when available. Re-ingest of a changed file gets a new row, never an overwrite.';
COMMENT ON COLUMN public.circumstance_sources.record_count IS
  'Rows in the source file as ingested. Used to detect silent truncation on re-ingest.';

COMMENT ON TABLE public.case_source_references IS
  'CANONICAL per-case source registry: one row per (case, source) link. Dataset-level metadata lives in circumstance_sources.';

-- --------------------------------------------------------------------------
-- (d) Linkage integrity: enforce one victimization -> one VIRS event, and
-- expose the pilot integrity counts as a queryable view.
-- Verified pre-migration 2026-11-08 02:37 CST: 576 links, 0 duplicates,
-- fatal_victim_count sum 119 (<= 576 linked victims), all 500 events
-- provisional_source_case / imported_unreviewed.
-- --------------------------------------------------------------------------
CREATE UNIQUE INDEX IF NOT EXISTS virs_event_source_links_one_event_per_victimization
  ON public.virs_event_source_links (chicago_victimization_id)
  WHERE chicago_victimization_id IS NOT NULL;

CREATE OR REPLACE VIEW public.v_virs_linkage_integrity AS
SELECT
  (SELECT count(*) FROM public.virs_events) AS provisional_groups,
  (SELECT count(*) FROM public.virs_event_source_links) AS linked_victim_rows,
  (SELECT count(DISTINCT chicago_victimization_id)
     FROM public.virs_event_source_links
    WHERE chicago_victimization_id IS NOT NULL) AS distinct_linked_victimizations,
  (SELECT count(*) FROM (
     SELECT chicago_victimization_id
       FROM public.virs_event_source_links
      WHERE chicago_victimization_id IS NOT NULL
      GROUP BY chicago_victimization_id HAVING count(*) > 1
   ) d) AS duplicated_victimization_ids,
  (SELECT coalesce(sum(fatal_victim_count), 0) FROM public.virs_events) AS fatal_victim_sum,
  (SELECT count(*) FROM public.virs_events
    WHERE linkage_status = 'provisional_source_case') AS provisional_linkage_count,
  (SELECT count(*) FROM public.virs_events
    WHERE record_status = 'imported_unreviewed') AS unreviewed_count,
  (SELECT count(*) FROM public.virs_evidence_assertions) AS evidence_assertions,
  (SELECT count(*) FROM public.virs_evidence_assertions
    WHERE review_status = 'approved') AS approved_interpretations;

COMMENT ON VIEW public.v_virs_linkage_integrity IS
  'Pilot integrity counts backing the public VIRS metadata endpoint. Healthy when duplicated_victimization_ids = 0 and fatal_victim_sum <= linked_victim_rows. Read-only; computes from live tables.';

-- --------------------------------------------------------------------------
-- (e) Missingness: empty arrays mean "not recorded", never false.
-- --------------------------------------------------------------------------
COMMENT ON COLUMN public.motive_signals.basis_codes IS
  'Source codes the signal rests on. Empty array {} means "not recorded" — never read as false or as confirmed absent.';
COMMENT ON COLUMN public.escalation_pathways.misunderstanding_types IS
  'Misunderstanding types observed in the evidence. Empty array {} means "not recorded" — never read as none occurred.';
COMMENT ON COLUMN public.escalation_pathways.escalation_mechanisms IS
  'Escalation mechanisms observed in the evidence. Empty array {} means "not recorded".';
COMMENT ON COLUMN public.escalation_pathways.deescalation_points IS
  'De-escalation opportunities observed in the evidence. Empty array {} means "not recorded".';

-- --------------------------------------------------------------------------
-- (f) Canonical write path for motive.
-- --------------------------------------------------------------------------
COMMENT ON TABLE public.motive_signals IS
  'CANONICAL store for motive signals (L3 interpretation). Public motive claims may only be drawn from rows here that are review_status = approved with evidence rows in motive_signal_evidence. The older classifications table must not independently decide an event''s motive.';
COMMENT ON TABLE public.classifications IS
  'Legacy general classification store (evidence-research foundation). NOT the canonical motive store — see motive_signals. Do not use for public motive claims.';

-- --------------------------------------------------------------------------
-- Verification queries (run after applying; expect: 2 junction tables exist,
-- 0 rows each; 2 constraints present per table; 1 partial unique index;
-- view returns provisional_groups 500, linked_victim_rows 576,
-- duplicated_victimization_ids 0, fatal_victim_sum 119).
-- --------------------------------------------------------------------------
-- SELECT table_name FROM information_schema.tables
--  WHERE table_schema = 'public'
--    AND table_name IN ('motive_signal_evidence', 'escalation_pathway_evidence');
-- SELECT * FROM public.v_virs_linkage_integrity;
