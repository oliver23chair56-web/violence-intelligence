# Violence Intelligence — program plan
Goal: goal_7809ad35eaf1 · Owner (lead): Mortimer · Oliver helps where only he can
Live: https://violence-intelligence.vercel.app · Repo: https://github.com/oliver23chair56-web/violence-intelligence
DB: Supabase oqhupkfbelmrubctknzj (FounderOS org) · Status: v2 live, deploys from Git main

## The goal, in Oliver's words
Comprehensive optics on gun violence in America — trends, graphs — and, most
importantly, a database of the circumstances behind every single incident:
does it fall into an expressive or instrumental act, plus new, innovative ways
to look at causes — how arguments escalate, which misunderstandings lead to
actions resulting in violence.

## Standing rules (do not break)
- Real data only. Every published figure traces to a named source, a retrieval
  date, and a stated denominator. Where sources disagree, show the disagreement.
- Motive is a research signal, never a label. No expressive/instrumental
  classification is published without human review. 0 reviewed motives today.
- No raw incident tables published — aggregated, anonymized only. No personal
  identifiers, no exact victim locations, no predictive policing, no
  person-level risk scores.
- No fabricated statistics. A missing year is shown as missing, never as zero.

## Phases

### Phase 1 — Circumstance database foundation (now)
- [ ] Circumstance schema v1 (SQL migration 0002): `incident_circumstances`,
  `motive_signals`, `escalation_pathways`, `circumstance_sources`.
  Design doc: `research/circumstance-schema-v1.md`.
- [ ] Escalation taxonomy v1: trigger → misunderstanding → escalation →
  violence, with misunderstanding types and de-escalation points.
  Doc: `research/escalation-taxonomy-v1.md`. Shipped on the dashboard
  Research tab as a living framework, marked as hypotheses to test, not findings.
- [ ] Seed the DB with what is already verified: Illinois 2018 circumstance
  families (874 records), FBI SHR 2018 benchmarks — as aggregate rows, with
  denominators attached.

### Phase 2 — National optics (scouting now, build next)
- National trends + graphs: firearm homicide/mortality by year and state,
  from FBI CDE and CDC WONDER (scout report: `national-data-scout.md`).
- Same grain discipline as Chicago: one chart = one dataset, one denominator,
  one coverage note. No cross-source rankings until definitions match.
- National expansion tab graduates from "readiness checklist" to real charts
  once the first verified national series lands.

### Phase 3 — Incident-level circumstances (the core database)
- Illinois 2018 is an aggregate benchmark, NOT an incident-level source
  (verified 2026-11-08 vs the ISP PDF: 845 incidents, 894 victims, 874
  murder victims; the 74,884-record figure cited earlier does not exist in
  any verified source and is retired). Incident-level circumstance data
  comes next from NIBRS extracts — each row keeps its source circumstance
  code, verbatim, plus a mapped motive *signal* (never a label).
- Verify the FBI SHR file record counts against the FBI publication before
  publishing any share computed on them.
- Escalation-pathway coding: reviewed cases get a coded pathway
  (trigger type, misunderstanding type, escalation steps, turning points).
  Published only in aggregate (e.g. "of N reviewed pathways, X% involved a
  misread threat").

### Phase 4 — Prevention intelligence
- Package-level pages: what interventions address which pathways, with
  evidence levels and time-to-effect (the `prevention_packages` table already
  exists in Supabase with 10 packages — verify and source each one).
- "What would have to be true" notes: for each pathway, the de-escalation
  point and what is known about interrupting it.

## What Oliver does (only he can)
- Direction calls: which cities/states next, what "comprehensive" must include.
- Source access that needs his identity (e.g. data-use requests, partnerships).
- Reviewing motive classifications before publication (human review gate).
- The social/content side: he has said a social-media content expert would
  agree with the research angle — distribution is his call.

## What I do (the lead)
- Everything else: data scouting, ingestion, schema, dashboard builds,
  verification, deployment, and keeping the numbers honest.

## Open questions (not blockers)
- 2021 Chicago data: import it, or document why it cannot be fetched?
- State-table denominators (24,871 / 8,479): reconcile against ISP/FBI sources.
- National series: which source becomes the national source of truth — FBI CDE
  or CDC WONDER — once the scout reports back?
