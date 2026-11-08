# VIRS Schema Reconciliation (draft — 2026-11-08)

**Purpose:** per VIRS v0.1 spec §8 scope item 1 — audit the live Supabase schema against Mortimer's migration 0002 and the VIRS 0.1 pilot tables, list duplicate concepts, and choose ONE canonical write path for motive/circumstance data. No live tables are renamed or removed by this doc; it is the basis for migration 0003 (compatibility), not a migration itself.

**Status:** DRAFT. Table-level inventory is verified (full count(*) inventory, 2026-11-08 ~02:10 CST). Column-level detail for the VIRS tables is pending a read-only inspection task (running); this doc will be updated with exact columns when it lands.

## 1. Verified live inventory (public schema, 52 tables)

### VIRS 0.1 pilot (built by ChatGPT, in the DB)
| Table | Rows | Role |
|---|---|---|
| virs_versions | 1 | Standard version registry |
| virs_fields | 15 | Standardized field definitions |
| virs_events | 500 | Provisional Chicago source-case groups |
| virs_event_source_links | 576 | Links: event group → victimization rows |
| virs_event_revisions | 500 | Import revisions |
| virs_evidence_assertions | 0 | Verified motive/evidence assertions (empty — zero approved motives) |

### Mortimer 0002 (applied 2026-11-08 02:04 CST, verified 02:10)
| Table | Rows | Role |
|---|---|---|
| circumstance_sources | 0 | Dataset/file provenance |
| incident_circumstances | 0 | Verbatim source-reported codes |
| motive_signals | 0 | Human-reviewable interpretation proposals |
| escalation_pathways | 0 | Coded escalation taxonomy |

All four have RLS enabled, 0 policies (default deny), 0 rows. Nothing has been written to them yet.

### Pre-existing circumstance / claims tables (ChatGPT)
| Table | Rows | Role |
|---|---|---|
| circumstance_claims | 0 | One specific proposition per event |
| claim_evidence | 0 | Evidence rows behind claims |
| classification_reviews | 0 | Review records for classifications |
| classifications | 0 | Classification outcomes |
| reported_circumstances | 0 | Reported (source) circumstances |
| circumstance_sources | 0 | (0002 table; also listed above) |
| circumstance_codebooks | 3 | Illinois 2018 / FBI / Chicago codebooks |
| circumstance_codes | 19 | Circumstance code list |
| circumstance_aggregate_counts | 19 | Aggregate counts (Illinois 2018 = 874 per PDF; API extraction is 3 low — see research/illinois-2018-reconciliation.md) |
| circumstance_benchmarks | 3 | Benchmark snapshots |
| incident_factors | 0 | Factor records |
| interventions | 0 | Intervention records |

### Chicago / national source data
| Table | Rows | Notes |
|---|---|---|
| chicago_victimizations | 15,693 | 2020 + 2022–2025; 2021 missing. Live API reports 15,330 victimizations — 363-row discrepancy to check |
| chicago_case_catalog | 12,293 | Distinct gunshot case numbers; matches verified case count |
| case_review_queue | 500 | Selected cases (~100/year); not human-reviewed |
| case_source_references | 500 | Official dataset references |
| case_evidence_tasks | 1,500 | Evidence tasks, uncompleted |
| national_incident_records | 23,289 | Detroit 9,773 / Kansas City 7,282 / Oakland 5,927 / Baltimore 307 (2025) |
| national_incident_sources | 4 | KC, Oakland, Baltimore, Detroit |
| national_import_windows | 26 | Monthly 2025 city API extractions |
| incidents | 100 | IL/Chicago sample only |

### Licensing / commercial (intentionally inactive)
vi_licensing_plans 3 rows; vi_organizations, vi_organization_members, vi_organization_licenses, vi_entitlement_audit, vi_plan_features — 0 rows except plans/features (10). **Do not activate without Oliver's explicit direction.**

## 2. Duplicate concepts — the collisions to resolve in migration 0003

| Concept | Competing tables | Proposed canonical write path (DRAFT — confirm against column detail) |
|---|---|---|
| Event grouping | virs_events (500 live groups) vs chicago_case_catalog (12,293 cases) | virs_events is the VIRS grouping layer; chicago_case_catalog is the source-case register. Link, don't merge. |
| Circumstance claim | circumstance_claims (0) vs incident_circumstances (0002, 0) vs reported_circumstances (0) | ONE write path: circumstance_claims as the canonical claim record (spec §3), with incident_circumstances as the verbatim source-code store linked by claim. reported_circumstances must not become a third motive table — resolve in 0003 (view or deprecate). |
| Interpretation / motive | motive_signals (0002, 0) vs classifications (0) vs virs_evidence_assertions (0) | motive_signals as the human-reviewable proposal (hypothesis, never fact); virs_evidence_assertions as the approved assertion store. classifications must not independently decide motive — resolve in 0003. |
| Evidence linkage | claim_evidence (0) vs virs_event_source_links (576) | virs_event_source_links for event↔victimization links; claim_evidence for claim↔source links. Distinct grains, both kept. |
| Review / approval | classification_reviews (0) vs case_review_queue (500) | case_review_queue is the work queue; classification_reviews is the review record. Keep both, link by case. |
| Source provenance | circumstance_sources (0002, 0) vs incident_sources (100) vs national_incident_sources (4) | circumstance_sources as the versioned source registry (spec §8 item 2); the others are source-specific registers to be linked, not replaced. |

**Rule (spec §5): choose one canonical write path and expose compatibility views — not parallel competing motive truth tables. No two tables may independently decide an event's motive.**

## 3. Gaps in 0002 to fix in 0003 (from spec §5)
- `review_status='approved'` must require `reviewed_by` + `reviewed_at` (currently unenforced).
- `basis_codes` alone cannot substantiate a motive — add evidence/claim references + optional contradictory evidence.
- Text arrays defaulting to `{}` mean "not recorded", not false — UI and SQL must honor that.
- Do not label the taxonomy construct "no face-saving exit" as a factual misunderstanding without evidence.

## 4. Migration 0003 — planned scope (not yet written)
1. This reconciliation doc (done, pending column detail).
2. Versioned source registry (`source_datasets` + `source_records`, or compatibility views on existing source tables) with (source_system, source_record_id, source_revision) uniqueness, grain, retrieval time, URL, hash.
3. Linkage: keep virs_events / virs_event_source_links as-is; tests that source victims link exactly once under the pilot and fatal ≤ gunshot victim count. No auto-created "verified" incident IDs.
4. Evidence trace: one claim ↔ source-evidence link path with epistemic_state, review status, revision tracking; `approved` requires named reviewer + date + ≥1 primary supporting link; counterevidence allowed. Start with zero inferred motives.
5. Safe metadata API (public-virs-specification already live) + VIRS dictionary UI in the Git-owned dashboard.
6. Tests: migration idempotence on staging + live; 500/576 fixture counts; duplicate source record no-op; missing ≠ zero; no automatic motive inference; reviewer gate; RLS anon denied; aggregate endpoint reveals no identifying information; Git → Vercel smoke test.

## 5. Open questions for migration 0003
- Exact columns of virs_events / virs_event_source_links / virs_fields (pending inspection task).
- What explains chicago_victimizations 15,693 rows vs live API 15,330 (363-row gap)?
- Correct the 3 low Illinois 2018 categories in the DB extraction (Arson, Alcohol Fight, Suspected Felony) to PDF values.
- Confirm the live migration history before choosing the number 0003.
- Staging/backup plan before any 0003 test run (never test destructive ops on production).

## 6. Column detail — verified 2026-11-08 02:11–02:20 CST (read-only inspection)
- **virs_events (16):** id uuid, standard_version text, source_system text, source_case_number text, linkage_status text, event_time timestamp, source_timezone text, city_name text, state_code text, discharge_status text, firearm_involved text, victim_count int, fatal_victim_count int, record_status text, created_at, updated_at. First 5 rows: all 2020-12-19 Chicago, source_system chicago-victims, version 0.1.0, linkage_status provisional_source_case, discharge_status reported, firearm_involved yes, record_status imported_unreviewed, created 2026-11-08 07:54:54 UTC.
- **virs_event_source_links (7):** id bigint, event_id uuid, chicago_victimization_id uuid, national_offense_id bigint, source_role text, verification_status text, created_at.
- **virs_fields (11):** field_key, standard_version, layer, data_type, definition, permitted_values, unit_of_analysis, evidence_requirement, missingness_rule, publication_level, required boolean. Missingness rule on all sampled fields: "unknown distinct from not_assessed and confirmed_absent". Sample: discharge_status permitted "confirmed,reported,unknown,contradicted,not_assessed", evidence "explicit source assertion; never infer from firearm used".
- **virs_versions (7):** version 0.1.0, title "Violence Intelligence Reporting Standard", lifecycle pilot, effective_date 2026-11-08, mission "Separate observed facts, documented circumstances, and reviewed research interpretations with auditable provenance", scope_notes "Independent experimental research specification. Not an FBI, CDC, or government standard. This pilot records source case groupings as provisional; it never asserts each grouping equals a verified shooting event."
- **case_review_queue (9):** id, source_system, case_number, queue_status, priority, assigned_to, reviewer_notes, created_at, updated_at.
- **circumstance_aggregate_counts (9):** id, code_id, reporting_year int, geography, unit, reported_count int, source_url, source_note, created_at. All 19 rows: reporting_year 2018, geography "Illinois statewide", unit "first and second degree murder circumstances", source_note "Source-reported statewide 2018 category count. Not a Chicago incidence or firearm-specific statistic", created 2026-11-08 06:29:26 UTC.
- **circumstance_codes (8):** id, codebook_id, source_code, source_label, source_family, is_unknown boolean, operational_definition, priority_note. All 19 share codebook_id 44a9def1-3315-49df-84ff-f2315eae9ee2; operational_definition and priority_note NULL on all. Families: interpersonal (alcohol_fight, lovers_triangle, money_argument, narcotics_fight, other_arguments), felony (arson, gambling, larceny, narcotics, other_felony, other_sex, prostitution, robbery, suspected_felony), gang (gang_killings, juvenile_gang), other (babysitter, other), unknown (unable_determine — the only is_unknown=true).
- **chicago_victimizations (16):** id, source_unique_id, case_number, occurred_at, victimization_primary, incident_primary, gunshot_injury, community_area, location_type, age_group, sex, race, hour_of_day, day_of_week, source_updated_at, imported_at.
- **chicago_case_catalog (9):** case_number, last_occurred_at, first_occurred_at, source_year int, gunshot_victimizations int, fatal_victimizations int, community_area, location_type, refreshed_at.

## 7. The 363-row gap — SOLVED
- chicago_victimizations = 15,693 rows. gunshot_injury='YES' = exactly 15,330 (the live API figure). gunshot_injury='NO' = exactly 363 rows, ALL victimization_primary='HOMICIDE' (2020: 80, 2022: 73, 2023: 62, 2024: 71, 2025: 77). The table holds 363 non-gunshot homicides on top of the 15,330 gunshot victimizations. Not an error — a grain difference. The API counts gunshot victimizations only.
- By year (occurred_at): 2020: 4,172; 2022: 3,607; 2023: 3,054; 2024: 2,922; 2025: 1,938; 2021 absent; no NULL occurred_at; 15,693 distinct source_unique_id.
- victimization_primary overall: BATTERY 11,952; HOMICIDE 3,141; ROBBERY 509; NON-FATAL 89; PUBLIC PEACE VIOLATION 1; CRIMINAL SEXUAL ASSAULT 1.
- chicago_case_catalog = 12,293 cases vs 12,637 distinct case_numbers in victimizations — 344 fewer. Hypothesis (unverified): the catalog excludes the non-gunshot homicide cases. To check before asserting.

## 8. Correction: DB circumstance table = 874 (matches PDF), API response differs
- The DB table circumstance_aggregate_counts sums to **874** (alcohol_fight 5, arson 3, suspected_felony 4) — matching the PDF exactly. The earlier note that "the API is 3 low" is corrected: the public-circumstance-benchmarks API returned 871 at ~02:15 CST while its own underlying table holds 874. The API likely reads a different source (possibly circumstance_benchmarks or a hardcoded snapshot) — verify the Edge Function's data source before trusting API totals.
- v2 dashboard (874) and the DB table (874) both match the PDF. No correction needed to either.
