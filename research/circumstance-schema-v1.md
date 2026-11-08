# Circumstance schema v1 — design notes
Migration: `supabase/migrations/0002_circumstances.sql` · Taxonomy: `escalation-taxonomy-v1.md`

## Tables
| Table | One row per | Purpose |
|---|---|---|
| `circumstance_sources` | source table/file | Registry: system, name, URL, coverage, grain, retrieval date |
| `incident_circumstances` | (incident, circumstance code) | Verbatim circumstance codes as the source reported them |
| `motive_signals` | incident | Expressive/instrumental **signal** + confidence + basis codes + review status |
| `escalation_pathways` | incident | Coded pathway: stage reached, trigger, misunderstandings, mechanisms, de-escalation points, retaliation link |

## Design decisions
- **Verbatim first.** Circumstance codes are stored exactly as reported.
  Mapping lives in `motive_signals` / `escalation_pathways`, never by editing
  the source row. A mapping can be wrong; the source row cannot be.
- **Unknown is a value.** `is_unknown` and the `unknown` signal are real
  categories. Nothing is imputed, and unknowns are always published as their
  own share.
- **Separation of incident identity.** Rows carry `source_system` +
  `source_record_id` so circumstance data can be ingested before a matching
  `incidents` row exists, and stay traceable if it never does.
- **Review gate.** `review_status` defaults to `pending` on both signal and
  pathway tables. Nothing with `pending` is published. `approved` requires a
  named reviewer and a timestamp.
- **RLS default deny.** Like migration 0001: no public policies on
  incident-level tables. The public API serves aggregates only, from views
  defined later — after review — that cannot expose identifiers, locations,
  or narrative detail.
- **Arrays, not booleans.** Misunderstandings, mechanisms, and
  de-escalation points are text arrays of taxonomy terms. An empty array
  means "not recorded", never "did not happen."

## What is NOT in v1 (deliberately)
- No free-text narrative storage (narratives stay in the source system until
  a redaction policy exists).
- No victim/offender identifiers beyond the source record id.
- No automated classification: the schema stores human-coded signals only.
  Any future automated suggestion would be a separate table with its own
  confidence and review fields.

## Status (2026-11-08)
Schema designed and committed to the repo. Not yet applied to the live
Supabase project — applying it needs the service-role key via the Supabase
dashboard (SQL editor) or CLI, which is a write action to take with Oliver
in the loop. 0 incidents coded. Seed data (Illinois 2018 families, FBI 2018
benchmarks) already lives in `circumstance_benchmarks` as aggregates.
