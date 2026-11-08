# Violence Intelligence — dashboard codebase (v6, merged)

Public research / prevention-intelligence dashboard about gun violence,
Chicago pilot. Live: https://violence-intelligence.vercel.app
Repo: https://github.com/oliver23chair56-web/violence-intelligence

**Deploys automatically from the main branch via Vercel. Git is the ONLY
deploy path — no direct Vercel API/CLI production deploys.** (Before the
merge, API deploys from the ChatGPT side overwrote Git deploys twice; the
merge on 2026-11-08 recovered those pages into this repo so it cannot
happen again. If production ever stops matching main, check the Vercel
deployment list for a non-Git deployment.)

## What this is
A static site (no build step) that reads live aggregates from the Supabase
project's public edge functions — no keys needed in the browser.

Homepage (`index.html`, v5 lineage): Overview, Interactive map,
Circumstances, Case explorer, National expansion (FBI CDE homicide trend
2015–2024 + SHR circumstance breakdown + CDC WONDER firearm mortality
1999–2020 by intent), Research & methods (escalation taxonomy, circumstance
database, Illinois 2018 reconciliation).

Merged module pages (recovered byte-for-byte from the live unified build,
2026-11-08, SHA-1 verified against the production deployment):
- `map.html` — national city explorer (Leaflet, 77 Chicago community areas)
- `dashboard.html` — Chicago dashboard + 500-case review queue
- `catalog.html` — searchable Chicago case catalog (12,293 cases)
- `compare.html` — definitions + metric comparison lab (explicitly NOT a ranking)
- `standard.html` — VIRS 0.1 data dictionary + methodology

## Verified state (2026-11-08)
- Chicago victimizations table: 15,693 rows; gunshot injuries 15,330
  (2,778 fatal, 12,293 cases). The extra 363 rows are non-gunshot
  homicides in the same table — a grain difference, not an error.
  Coverage: 2020 and 2022–2025; 2021 not imported.
- Illinois 2018 (ISP PDF, verified line by line): 845 homicide incidents,
  894 victims, circumstance table 874 (Unable 290, Interpersonal 222,
  Gang 176, Felony 125, Other 61). The 74,884-record figure cited in
  earlier conversation material does not exist in any verified source and
  was removed from the dashboard in v6. Reconciliation:
  research/illinois-2018-reconciliation.md.
- VIRS 0.1 (pilot, not an adopted standard): 15 fields, 500 provisional
  Chicago event groups, 576 linked victimizations, 0 approved motives.
  Spec: handoff/VIRS_v0.1_Mortimer_Implementation_Spec.md. Schema
  reconciliation: docs/virs-schema-reconciliation.md.
- 10 public Edge Functions live: public-chicago-incidents,
  public-analytics, public-circumstance-benchmarks,
  public-case-review-sample, public-community-map, public-expansion,
  public-research-readiness, public-national-incidents,
  public-metric-comparability, public-virs-specification.
- Raw incident tables are never published — aggregated, anonymized only.
  Motive is a research signal, never a final label; 0 motives reviewed.
- Numbers in the earlier ChatGPT conversation are internally inconsistent
  in places. This codebase publishes only figures verified against the
  live endpoints, the ISP PDF, or the database — and flags the rest
  instead of picking one silently.

## Deploy
Static site. Push to main; Vercel deploys automatically. Do NOT deploy
to production via `vercel deploy --prod` or the Vercel API — that breaks
the Git-only rule and will be overwritten by the next push.
