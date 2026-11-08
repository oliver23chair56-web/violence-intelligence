# VIRS Comparison Validation 1.0 — audit design

**Date:** 2026-11-08
**Status:** Design approved in principle by Oliver (VIRS pilot package, 2026-11-08).
Blocked only on naming the independent second reviewer.
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

## Inter-reviewer agreement

- **Cohen's kappa** on the core binary decision (is this a firearm
  homicide victim?), computed per city and overall. Raw agreement %
  reported alongside.
- **Acceptance bar:** kappa ≥ 0.80 AND victim-count error rate < 5%
  AND no systematic bias found (e.g. Baltimore multi-victim cases
  systematically undercounted).
- If kappa < 0.80, the measure stays unapproved. The disagreement
  patterns become the next fix list — they are findings, not failures.

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
