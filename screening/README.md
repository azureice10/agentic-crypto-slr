# Screening and arXiv provenance exports

Release 3.6.3. These files were extracted from the user-identified local source workbooks and exports on 3 November 2026. The source workbooks were not modified. The normalized Stage 1 export includes the 104 explicitly confirmed date corrections documented in the correction ledger. No publisher abstracts are included.

| Export | Rows | Source and unit |
|---|---:|---|
| stage1_register.csv | 926 | One screened source ID; metadata from Stage1_Screening_Worksheet_926.csv, raw reviewer decisions from IMPORT_R1/IMPORT_R2, final decisions from ADJUDIKASI |
| stage2_register.csv | 610 | One full-text candidate from DAFTAR_STUDI_STAGE2_610 |
| stage2_fulltext_reviews.csv | 1,220 | One reviewer/report assessment from FULLTEXT_REVIEW; two reviewer IDs per report |
| stage2_rigor_reviews.csv | 694 | One reviewer/preprint assessment from PREPRINT_RIGOR_REVIEW; two reviewer IDs per 347 preprints |
| stage2_family_links.csv | 2 | Verified companion-to-canonical links from STUDY_FAMILY_REVIEW |
| stage2_adjudication_log.csv | 183 | Recorded Stage 2 adjudication/amendment log rows from LOG_ADJUDIKASI |
| arxiv_query_occurrences.csv | 4,142 | One raw query-return occurrence; selected identity/provenance fields, no abstract |
| arxiv_gate_pass_register.csv | 529 | One unique gate-passing base ID, including 35 superseded / 494 new preprints |

Source-workbook names, sheet names, and SHA-256 identities accompany the decision exports. All input and normalized-export identities are listed in `protocol/search_sources/source_manifest.json`. Full original XLSX files and physical PDFs are not redistributed. Compact arXiv exports omit abstracts and retain query labels, stable IDs, version strings, and source-row provenance.

## Reading the fields

- `Source_Record_ID` joins Stage 1 and Stage 2 records; the 442 included Stage 2 IDs join the unchanged `data/studies.csv` exactly. `Screening_ID` is the upstream operational identifier. `seq` preserves the Stage 1 administrator's order.
- `R1_*` / `R2_*` fields contain recorded pre-adjudication labels and metadata. `FINAL_*` fields contain the administrator's final Stage 1 decisions. They are separate states, not competing denominators.
- `Fulltext_Eligibility` controls the Stage 2 partition. `Preprint_Rigor_Gate_Status` is an additional assessment; passing the gate does not guarantee substantive inclusion. Tier 1 exemption applies only to that additional gate.
- Stage 2 `Extraction_Status` is a historical pilot snapshot (45 extracted / 565 not started), not current Stage 3 completion. Two merged entries retain PENDING_REVIEW in Confirmed_Stream; their final eligibility is already MERGED_STUDY_FAMILY.
- Source formula caches, including Row_QA, are retained as recorded values and are not evidence of fresh recalculation. Blank caches are not filled by guessing formulas. Some source date cells retain raw Excel serial values; they have not been relabeled as ISO dates.
- The user confirmed 2026-10-16 for all 104 previously flagged Reviewer 2 dates. Active register values are corrected; original values and confirmation provenance remain in `protocol/screening_date_corrections.csv`. `results/screening_date_issues.csv` now has zero active issues. All final adjudication dates remain 2026-10-17.
- Source locators and hashes preserve references to evidence. They do not authenticate independent human review or replicate the substantive judgment against a primary PDF.

Run `python scripts/screening_support.py` from the package directory to recompute flow, agreement, exclusion counts, arXiv provenance, and date issues. `scripts/validate_data.py` checks the register joins and compares the derived summary with a fresh computation.
