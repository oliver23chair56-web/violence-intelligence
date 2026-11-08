# VIRS Comparison Validation 1.0 — audit design

**Date:** 2026-11-08
**Status:** v1.1 — REVISE BEFORE EXECUTION. ChatGPT reviewed the v1.0 design
2026-11-08 ~08:54 CST and found it a good starting point with five gaps
(A–E below). Do not run the audit until the revisions are applied.
**Goal:** validate ONE measure — firearm-homicide victims, Chicago vs
Baltimore — so it can become the first approved cross-city comparison.
Nothing else is validated by this audit. No ranking. No motive work
(that is the separate 30–50-case circumstance sample).

## Why this measure, why these cities

- Chicago has the only victim-grain firearm-homicide measure that is
  already supported (`gunshot_injury = YES AND victimization_primary =
  HOMICIDE`, 2,778 fatal gunshot victimizations, 2020 + 2022–2025).
- Baltimore is the only other city with a shooting flag (`Shooting = Y`
  on NIBRS offense rows), but its grain is offense rows, not victims.
  The audit must establish whether Baltimore's flag can be turned into a
  victim count at all — and if not, what source would be needed instead.
- Both ChatGPT and Oliver independently prioritized this measure first.

## Sample: 100 cases

- **50 Chicago**, drawn from fatal gunshot victimization cases
  (gunshot_injury = YES, victimization_primary = HOMICIDE).
  Stratified by year in proportion to the data (2020, 2022, 2023, 2024,
  2025; 2021 does not exist). Oversample the tricky slices: multi-victim
  cases, and the 9 mixed cases where a non-gunshot victim shares a case
  number with a gunshot victim.
- **50 Baltimore**, drawn from 2025 Shooting = Y offense rows.
  Stratified by month. Oversample the known failure mode: case IDs with
  multiple offense rows (the mapping's own limitation warns that
  multiple rows can share one case ID).
- Random draw within each stratum, seeded and recorded so the draw is
  reproducible. Case IDs are listed in the audit record, never published.

### Revision A — test specificity (ChatGPT review, critical)
The v1.0 Chicago sample contains only known firearm-homicide cases, so
it cannot test whether the measure wrongly counts non-cases. Add
negative / ambiguous cases to the Chicago arm: non-firearm homicides
(the 344 non-gunshot homicide cases are the natural pool), nonfatal
shootings, and unclear records. The audit must report false positives,
not just agreement on known positives.

### Revision B — Baltimore needs a victim-level reference source (critical, biggest issue)
Baltimore's "Shooting = Y" flag identifies a shooting-related source
record, not necessarily a person who died from gunshot injury. The
offense rows alone cannot establish the number of firearm-homicide
victims. **Before validation, an independent victim-level reference
source for Baltimore must be identified** — candidates: Maryland death
certificate data, Baltimore medical-examiner / homicide records, or
CDC WONDER state-level firearm-homicide counts for aggregate-level
checks. Until that source exists, the Baltimore arm is a feasibility
assessment, not a validation. This is the first next action.

### Revision C — match years and outcome rules
Compare the same year on both sides: **2025 for both cities** (v1.0
compared Chicago 2020 + 2022–2025 with Baltimore 2025). Specify the
incident-year rule, the extraction cutoff date, and the amendment
policy (how later corrections are handled) before drawing the sample.
NOTE: ChatGPT cited a "Baltimore Police December 2025 clarification"
— UNVERIFIED, do not treat as fact until checked against a primary
source.

## What each reviewer checks per case (independent, double-blind)

1. **Is this a firearm homicide victim?** The core binary decision.
   Chicago: does the source record actually show a person killed by
   gunshot? Baltimore: does the Shooting = Y offense row correspond to a
   person killed by gunshot, or only to a firearm offense?
2. **Victim count.** How many firearm-homicide victims does this case
   contain, per the source? (Catches multi-victim undercounting.)
3. **Case identity.** Is one case ID one event, or do multiple events
   share an ID? (Baltimore's known risk; Chicago's pilot groups are
   provisional for the same reason.)
4. **Date/year.** Does the recorded year match the source?
5. **Baltimore only: what does Shooting = Y mean here?** Reviewer
   records the offense type and whether any victim information exists
   in the source row at all.

Each check is recorded as: confirmed / contradicted / insufficient
evidence (unknown) / not assessed. Reviewers work from the restricted
case evidence; only aggregates leave the review.

## Reviewers

- **Oliver Chairez** — review gate. Final call on approval.
- **One independent second reviewer** — NOT YET NAMED. Must be someone
  who did not build the mappings or the sample. No expert appointment is
  required to begin; a careful second reader suffices.
- Disagreements are resolved by discussion and recorded, not silently
  overwritten. The disagreement log is part of the audit record.

### Revision E — make independence explicit (ChatGPT review)
Two independent coders, blind to each other's work AND blind to the
system's proposed classification. A separate adjudicator resolves
disputes. Oliver remains the final gatekeeper. "Second reviewer" alone
is not enough — the roles are coder, coder, adjudicator, gate.

### Reviewer suggestion from ChatGPT (2026-11-08, verification status noted)
- Profile: independent injury epidemiologist or public-health research
  data analyst comfortable with death-certificate data, medical-examiner
  findings, police incident data, and inter-rater reliability, with a
  senior epidemiologist overseeing.
- **Cassandra Crifasi — VERIFIED real:** Co-Director / Co-Executive
  Director, Johns Hopkins Center for Gun Violence Solutions; Professor
  of Health Policy and Management; injury epidemiologist (confirmed via
  JHU faculty page + Bloomberg School magazine, 2026-11-08). Senior
  academic contact, not necessarily the coder.
- **"Goldie Hellman, Senior Research Data Analyst" — NOT VERIFIED, do
  not contact under that name:** no such person appears in search
  results or on the Center's team page (its listed data analysts are
  Ethan Bartlett, Nandita Somayaji, and Elizabeth Wagner). ChatGPT's
  name is unconfirmed — possibly hallucinated or outdated.
- Neither person has been contacted or agreed to participate.
  Independence, availability, and conflicts still need checking — note
  the Center combines research with gun-violence-prevention advocacy,
  which Oliver should weigh when judging independence.

## Inter-reviewer agreement

- **Cohen's kappa** on the core binary decision (is this a firearm
  homicide victim?), computed per city and overall. Raw agreement %
  reported alongside.
- **Acceptance bar:** kappa ≥ 0.80 AND victim-count error rate < 5%
  AND no systematic bias found (e.g. Baltimore multi-victim cases
  systematically undercounted).
- If kappa < 0.80, the measure stays unapproved. The disagreement
  patterns become the next fix list — they are findings, not failures.

### Revision D — strengthen statistics (ChatGPT review)
- Kappa ≥ 0.80 stays as an agreement TARGET, not the sole approval
  gate. Report raw agreement, positive agreement, and negative
  agreement, each with confidence intervals, plus case-level
  disagreement — so a high kappa on an easy sample cannot hide real
  problems.
- Define the victim-count error formula and its denominator EXACTLY
  before the audit (e.g. |counted − reference| / reference victims,
  per case and in aggregate) — do not decide it after seeing results.
- The 100 cases are a PILOT. Passing them authorizes the next step,
  not publication of national comparisons.

## Approval

A mapping flips to `approved_for_city_comparison = true` only when:
- the audit passes the bar above for that city and measure, AND
- Oliver, as gate, signs off on the audit record.

Until then the compare page keeps showing the measure as unapproved,
with the reason stated. The audit record (sample definition, per-case
decisions in aggregate, kappa, disagreement log, approval decision)
lives in the repo under `research/validation-1.0/`.

## Explicitly out of scope

- Motive / expressive vs instrumental classification (separate 30–50
  Chicago sample, separate review).
- Any ranking of cities.
- Any publication of individual case details.
- Detroit, Kansas City, Oakland (no shooting/victim grain to audit yet).
