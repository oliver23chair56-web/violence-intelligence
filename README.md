# Violence Intelligence — dashboard codebase (v2)

Public research / prevention-intelligence dashboard about gun violence,
Chicago pilot. Live: https://violence-intelligence.vercel.app
Repo: https://github.com/oliver23chair56-web/violence-intelligence

Deploys automatically from the main branch via Vercel.

## What this is
A static site (no build step) that reads live aggregates from the Supabase
project's public edge functions — no keys needed in the browser:

- `public-analytics` — Chicago gunshot victimizations (annual, monthly, hours, locations, areas, weekdays)
- `public-community-map` — community-area/year aggregates for the map
- `public-circumstance-benchmarks` — FBI SHR 2018 + Illinois 2018 circumstance codes
- `public-case-review-sample` — 500-record case review queue (no motive labels)

## Verified state (2026-11-08)
- Dataset: Chicago Violence Reduction — Victims; grain: one row per gunshot
  victimization. Coverage: 2020 and 2022–2025; 2021 not imported.
  Totals across imported years: 15,330 victimizations, 2,778 fatal, 12,293 cases.
- The conversation's `public-map-data` and `public-dashboard` function names
  return 404 — the live code does not call them; it calls
  `public-community-map` and `public-case-review-sample`, which are live.
- Numbers in the earlier ChatGPT conversation are internally inconsistent in
  places (e.g. 13,007 vs 3,300 homicides; expressive 41.6% / instrumental
  58.4% / unknown 71.7% cannot all be shares of one whole). This codebase
  publishes only figures verified against the live endpoints, and the Research
  tab flags the unresolved denominators instead of picking one silently.
- Raw incident tables are never published — aggregated, anonymized only.
  Motive is a research signal, never a final label; 0 motives reviewed.

## Deploy
Static site. From this directory:

```
vercel deploy --prod
```

Or connect a Git repository to the Vercel project `violence-intelligence`
(team `black-dolphin1`) and deploy from Git. No environment variables are
required — the Supabase function URLs are public endpoints baked into
`index.html`.

## Layout
- `index.html` — the whole dashboard (Overview, Interactive map,
  Circumstances, Case explorer, National expansion, Research & methods)
- `transform_v2.py` — the script that built this v2 file from the previously
  deployed `index.html`; re-run after pulling a fresh copy of the live page
- `supabase/migrations/0001_initial.sql` — original schema (starter package)
- `pipelines/ingest_chicago.py` — Chicago sample ingest (starter package)
