# Screening register provenance and reconciliation

Release 3.6.3 - evidence recovered on 3 November 2026.

## Authoritative layers

Stage 1 bibliographic inventory is `Stage1_Screening_Worksheet_926.csv`. Its 926 final-decision fields were blank, so it is not used as the adjudicated-decision source. Final labels come from `Stage1_Screening_Adjudikasi_Admin_926_v1.1.xlsx`, sheet ADJUDIKASI; the pre-adjudication reviewer labels come from IMPORT_R1 and IMPORT_R2. The normalized join is `screening/stage1_register.csv`.

Stage 2 comes from `Formulir_Ekstraksi_Data_Stage2_610_v1.2_READY.xlsx`, primarily DAFTAR_STUDI_STAGE2_610. FULLTEXT_REVIEW, PREPRINT_RIGOR_REVIEW, STUDY_FAMILY_REVIEW, and LOG_ADJUDIKASI are exported separately. Full source-workbook SHA-256 values and normalized export identities are retained in `search_sources/source_manifest.json`.

## Recomputed selection and agreement

Stage 1: 926 = 610 ADVANCE_FULLTEXT + 236 EXCLUDE_STAGE1 + 78 CONTEXT_ONLY + 2 LINK_REPORT_VERSION. The 610 advanced source IDs exactly equal the Stage 2 candidate set.

Stage 2: 610 = 442 ELIGIBLE_INCLUDED + 166 EXCLUDED_FULLTEXT + 2 MERGED_STUDY_FAMILY. Included source IDs and recorded PDF hashes match the 442 canonical studies. Exclusions: EC1 53; EC2 3; EC4 76; EC5 19; language 1; EC_RIGOR_1 9; EC_RIGOR_2 5.

Tier 1/Tier 2 counts are 432/494 at Stage 1 and 263/347 at Stage 2. Rigor: 331 pass, 14 fail, 2 merged/not assessed, and 263 Tier 1 exemptions. The included reports contain 212 Tier 1 and 230 Tier 2 records.

Raw five-class agreement is 646/926 (69.7624%); Cohen kappa is 0.4172147324. Binary agreement (ADVANCE_FULLTEXT versus all other labels) is 685/926; kappa is 0.4446313652. Calculations are implemented in `scripts/screening_support.py` and written to `results/screening_summary.json`.

## Historical states and unresolved metadata

The supplied narrative's “Batch 1 & Batch 2 still under review” describes an earlier state. The recovered register has completed eligibility dispositions for all 610 candidates. Its extraction fields still record a pilot-stage snapshot (45 CLAIMS_EXTRACTED / 565 NOT_STARTED). Neither that snapshot nor the workbook filename determines current Stage 3 extraction maturity; the five final canonical CSVs do.

The original Reviewer 2 date field had 100 pre-search dates and four non-date strings. On 3 November 2026 the user confirmed 2026-10-16 as the correct date for these 104 entries. The active normalized register is corrected to that date; `protocol/screening_date_corrections.csv` retains the original values, source IDs, and confirmation basis. There are zero active date issues. Final administrator dates remain 2026-10-17 for all 926 records. Decision labels and kappa are unchanged. This confirmed metadata correction does not independently authenticate reviewer identities.

The presence of two reviewer records per report and a recorded READY formula cache is not proof of independent human review. Original XLSX files, individual signatures, primary PDF contents, and the separate Stage 3 review-audit trail are outside the distributed register exports. Physical primary PDFs were not re-audited for this integration.
