# Screening and query-provenance audit

Release 3.6.3. Computed from normalized register exports in `screening/`. Original XLSX files were read without editing or recalculating their formulas. The normalized Stage 1 register incorporates 104 user-confirmed R2 date corrections, with original values retained separately. Final decisions use ADJUDIKASI; reviewer labels use IMPORT_R1/IMPORT_R2; Stage 2 uses DAFTAR_STUDI_STAGE2_610.

## Selection flow

Stage 1: 926 records = 610 ADVANCE_FULLTEXT + 236 EXCLUDE_STAGE1 + 78 CONTEXT_ONLY + 2 LINK_REPORT_VERSION. Tier split: 432 peer-reviewed / 494 preprint records.

Stage 2: all 610 advanced IDs match the Stage 2 register. Tier split: 263 / 347. Final eligibility: 442 included + 166 excluded + 2 merged. Rigor: 331 PASS, 14 FAIL, 2 merged/not assessed, plus 263 Tier 1 exempt from the additional preprint gate. The 442 included source IDs and recorded PDF hashes match studies.csv exactly. The 1,220 full-text review records contain two reviewer IDs for each of 610 reports; 694 rigor records cover two reviewer IDs for each of 347 preprints. Row presence and completed labels do not authenticate independent human review.

The Stage 2 workbook retains pilot extraction states (45 CLAIMS_EXTRACTED / 565 NOT_STARTED). Those historical extraction states are not the current Stage 3 completion denominator. Final Stage 3 reporting continues to use the five unchanged canonical CSVs. Two merged rows retain PENDING_REVIEW in Confirmed_Stream, but their eligibility is MERGED_STUDY_FAMILY, not an unresolved eligibility decision.

## Recomputed agreement

Five-class labels: 646/926 match (69.7624%); 280 differ; Cohen kappa = 0.4172147324.

Binary ADVANCE_FULLTEXT versus all other labels: 685/926 match; Cohen kappa = 0.4446313652. These are pre-adjudication label statistics, not post-adjudication consensus or claim-extraction reliability.

## Confirmed date corrections

The user confirmed 2026-10-16 as the correct date for all 104 previously flagged Reviewer 2 entries (100 pre-search dates and four non-date strings). The active R2_Decision_Date values are corrected to 2026-10-16. Original values, source IDs, and confirmation provenance are retained in protocol/screening_date_corrections.csv. The active date-issue export contains zero rows. All 926 final adjudication dates remain 2026-10-17. Decision labels and agreement are unchanged. User confirmation resolves the recorded date errors; it does not independently authenticate reviewer identities.

## arXiv query provenance

The compact raw-occurrence export contains 4,142 query returns / 3,894 base IDs. The 529 gate-passing IDs partition into 494 new preprints and 35 superseded versions. Four arXiv query strings match the archived pipeline constants. Raw occurrences resolve the seed-query assignments by stable arXiv ID; historical seed reference numbers are translated to the manuscript numbering. No live API rerun was performed.

The three supplied ACM strings are documented as author-supplied Boolean expressions. They do not contain the proximity operator mentioned in earlier narrative descriptions. Exact historical UI settings are not recovered from the supplied strings; original yield reproduction is not claimed.

## Source identity

Source-workbook and export SHA-256 values, selected sheet names, normalized export identities, and the archived arXiv pipeline identity are recorded in protocol/search_sources/source_manifest.json. The Stage 1 inventory CSV had 926 blank final-decision fields and was used only for bibliographic metadata. Final decisions were recovered from the administrator workbook instead. Formula QA caches were not freshly recalculated.
