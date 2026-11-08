# Unified dashboard — recovery snapshot

**Recovered:** 2026-11-08 ~02:25 CST, from production deployment dpl_ABuE9qrTtwUsXSwRNmbP3akKt4Qr via Vercel API v8 (file contents endpoint; v6 is disabled).
**Verification:** all 6 files' SHA-1 hashes match the deployment file list exactly. index.html is 18,511 bytes — identical to the live homepage fetched by curl. This is byte-for-byte the code currently serving https://violence-intelligence.vercel.app.

Files: index.html (shell/nav), map.html (national city explorer), dashboard.html (Chicago analytics + 500-case queue), catalog.html (Chicago case catalog), compare.html (definitions + metric comparison lab), standard.html (VIRS data dictionary + methodology).

**Status:** recovered to disk only — NOT yet committed to Git. Committing/merging awaits Oliver's source-of-truth decision (Git-owned v5 vs unified dashboard). The unified pages call Edge Functions public-analytics, public-community-map, public-national-incidents, public-virs-specification, public-circumstance-benchmarks, public-expansion, public-research-readiness. They contain none of Mortimer's v5 national content (no WONDER, no 165,675 SHR).
