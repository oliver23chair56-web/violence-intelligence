# Comparability matrix v1 — which cities can be compared, on what

**Date:** 2026-11-08 (02:40 CST)
**Source:** live `public-virs-specification` endpoint (11 city mappings, retrieved 2026-11-08) + direct DB inspection. All mappings are reporting year **2025** unless noted.
**Status today: 0 of 11 mappings approved for city comparison.**

## The rule

Three measures are separately comparable. They are never merged into one
number, and no city is ranked on a common scale until its mapping for that
measure is approved:

1. **Distinct firearm-discharge events** — one gunfire event, however many
   victims or offense rows it produced.
2. **Gunshot victimizations** — one victim shot, as recorded by the source.
3. **Firearm homicide victims** — one victim killed by gunshot.

A mapping is approved for comparison only after a human audit confirms the
source field means what the rule says it means. Until then it is
`approved_for_city_comparison = false`, and the dashboard must say so.

## Matrix

| City | Gunshot victimizations | Firearm homicide victims | Distinct firearm-discharge events |
|---|---|---|---|
| **Chicago** | SUPPORTED — `gunshot_injury = YES`, victim rows (15,330 gunshot victimizations, 2020 + 2022–2025; 2021 missing) | SUPPORTED — `gunshot_injury = YES AND victimization_primary = HOMICIDE` (2,778 fatal gunshot victimizations) | NOT SUPPORTED — case numbers are not events. The 344-case gap is SOLVED (2026-11-08): the catalog's 12,293 cases are exactly the gunshot cases; the 344 are homicide cases with no gunshot victimization row (354 rows, 10 cases with 2 rows). The 500 pilot groupings remain provisional and unreviewed. |
| **Baltimore** | NOT SUPPORTED — source is offense rows, not victims. `Shooting = Y` flags an offense, and multiple offense rows can share one case ID. | NOT SUPPORTED — no victim-level homicide flag in the mapping. Deriving it from offense rows would be a guess. | NOT SUPPORTED — distinct CCNumber among Shooting=Y rows counts cases associated with shooting-coded offenses, not distinct gunfire events. |
| **Kansas City** | NOT SUPPORTED — `firearmusedflag = true` on selected offenses proves a firearm was involved, not that it was discharged, and not that anyone was shot. Multiple rows per report. | NOT SUPPORTED — same reason; no victim grain. | NOT SUPPORTED — distinct report numbers among firearm-used offenses are not shooting counts. |
| **Detroit** | NOT SUPPORTED — "selected violent offense" (four categories) includes offense entries with no known firearm involvement. | NOT SUPPORTED — same reason. | NOT SUPPORTED — distinct report_number within selected offenses is not a shooting count. |
| **Oakland** | NOT SUPPORTED — same as Detroit (four selected offense categories, firearm involvement unknown). | NOT SUPPORTED — same reason. | NOT SUPPORTED — distinct casenumber among selected offenses is not a gunshot incident count. |

## What "supported" means, and what it doesn't

Chicago's two supported measures are supported **as victim counts within
Chicago's own feed** — they are the only measures that currently clear the
bar for cross-city comparison, and only against another city whose mapping
for the same measure is also approved. Today no other city has an approved
mapping for either measure, so **no cross-city comparison is publishable
yet**. The dashboard's compare page says this; it must keep saying it.

"SUPPORTED" does not mean perfect. Chicago's feed has known limits:
2021 entirely missing (never shown as zero), victim grain (not events),
and the 344-case gap between the catalog (12,293) and distinct case
numbers in the feed (12,637).

## What unblocks the first comparison

The first publishable comparison is the one ChatGPT and Oliver both
prioritized: **a common firearm-homicide-victims measure for Chicago and
Baltimore**. To get there:

1. **VIRS Comparison Validation 1.0** — 100-case audit (Chicago + Baltimore):
   confirm the Baltimore `Shooting = Y` offense rows correspond to real
   shooting events, confirm how Baltimore records homicide victims, and
   measure how often one Baltimore case ID hides multiple offense rows.
   Design doc pending; review needs Oliver (gate) + one independent
   second reviewer (not yet named).
2. Resolve the **344-case gap** (Chicago) — SOLVED 2026-11-08 ~02:43 CST: the catalog's 12,293 cases are exactly the gunshot cases; the 344 are homicide cases with no gunshot victimization row (354 rows, all HOMICIDE, 10 cases with 2 rows; years 2020: 75, 2022: 70, 2023: 60, 2024: 69, 2025: 70). gunshot_injury is clean: YES 15,330 / NO 363 / NULL 0; 9 NO rows sit on mixed cases that also have a gunshot victim.
3. Then, and only then, flip Baltimore's firearm-homicide mapping to
   approved — or document why it cannot be approved and what source would
   be needed instead.

## Standing cautions (unchanged)

- `national_incident_records` (23,289 rows: Detroit 9,773 / Kansas City
  7,282 / Oakland 5,927 / Baltimore 307) uses **different units per city**.
  It must not be ranked on a common scale.
- Missing cities (Memphis, Little Rock, Cleveland, Peoria, Birmingham,
  St. Louis) have no mappings at all — absence of data, not zero violence.
- WONDER (death certificates) vs FBI (police-reported) are different
  universes — shown separately, never merged.
- Motive is a research signal, never a label. 0 motives reviewed.
