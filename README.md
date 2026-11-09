# Evidence companion, critical revision R3 (4 November 2026)

The detailed PDF is evidence_supplement.pdf. The canonical data remain release 3.6.3; R3 adds targeted source checks and post hoc sensitivities without changing canonical extraction records. The designated repository is https://github.com/azureice10/agentic-crypto-slr; this release has not yet been uploaded and an archival DOI is pending. The original package documentation follows.

# Cryptographic Assurance Gaps in LLM-Based Agentic Systems

## R3 update: raw Stage 3 archive and reproduced agreement

The later supplied `stage3_irr/` archive contains the 18 reviewer worksheets, extended E05 version, nine adjudication masters and the author's script/results. This supersedes earlier statements below about absence of Stage 3 raw worksheets; historical review logs not contained in this archive remain unavailable. Run `scripts/reproduce_stage3_irr.py` for independently computed first-row, single-claim and order-paired results. Current findings and corrections are in `results/stage3_irr_reproduction_report.md`. The initial author-summary CSV and feasibility check are historical, not the final IRR results. The archive's original README/script are preserved, including a documented maturity-ranking bug; do not interpret that output as valid highest-maturity aggregation. The author confirms Herman checked/approved these R1 worksheets before adjudication; legacy AI-draft/UNASSIGNED metadata remain, and approval notes are being located.

Supplementary package release **3.6.3**, reconciled on **3 November 2026**. The analytical data remain the adjudicated **v3.5 baseline**, with recorded human sign-off dated 2 November 2026. Reporting corrections in this release do not constitute a new human source review or a new sign-off.

**CS1 manuscript analysis revision (3 November 2026):** the manuscript now includes post hoc role, QA, formal-category, source-statistic and PQC-linkage sensitivity analyses. The numerical data release remains 3.6.3. These additions do not change canonical records or screening dates. Figures 2-4 have clarified interpretive labels; their underlying numbers are unchanged.

Run `node scripts/critical_synthesis.mjs` with Node.js 22 or newer to reproduce `results/critical_synthesis.json` and `results/critical_synthesis.md`. The outputs record input hashes, explicit denominators and selected claim IDs. The older `Strict_Formal` indicator name denotes the three-category focused grouping (29 claims), not an independently verified proof class. Including THEORETIC_PROOF gives 83 claims. Latency medians summarize heterogeneous extracted values, not pooled workload p50 or incremental overhead.

Run `python scripts/validate_critical_synthesis.py` for independent pandas checks of the new aggregates and, when the parent manuscript is present, its new numerical tables and local links.

Full search expressions formerly in the manuscript body are preserved in `protocol/search_strings_appendix.md`. Batch accounting and detailed historical QA examples are in `results/extraction_batch_table.md` and `results/claim_appraisal_examples.md`. The CS1 source-statistic restriction, report-level PQC joins, and role contrasts are explicitly post hoc; original evidence labels are preserved.

## Source of truth and populations

The five canonical files in `data/` are the source of numerical reporting. This revision does not modify their records.

| File | Scope |
|---|---|
| `studies.csv` | 442 canonical reports: 212 Tier 1 + 230 Tier 2 |
| `claims.csv` | 584 claims: 530 READY + 54 FLAGGED; 406 reports have at least one READY claim |
| `rq3_metrics.csv` | 1,111 rows: 1,091 numeric + 20 NR; 1,020 rows belong to READY claims, including 1,008 numeric + 12 NR |
| `rq3_latency_crosswalk.csv` | All 454 time-unit rows: 399 eligible + 26 sibling duplicates + 3 quarantined conflicts + 26 other strata; 0 HOLD |
| `rq4_dependencies.csv` | 283 inventory rows on 248 claims / 245 reports: 266 active crypto/attestation dependencies + 17 excluded non-cryptographic records |

Active RQ4 dependencies consist of 222 concrete algorithm/protocol/enclave-class records and 44 unspecified-suite records. The READY inventory contains 241 rows: 224 active + 17 excluded. Stage 4-5 comprises seven claims on **four reports**; four READY claims occur on two reports.

Claim QA is separate from metric eligibility: a READY claim can have an excluded duplicate, a nonnumeric NR record, or a quarantined source conflict. An absent active dependency link does not establish a non-cryptographic mechanism. NOT_DISCUSSED and Stage 0 retain batch-dependent historical labels and are combined as **no demonstrated PQC migration** in the harmonized analysis.

## Contents and reproducibility

- `protocol/`: search and eligibility summaries, the complete 188-column `data_dictionary.csv`, and a reporting map in Markdown/PDF. Complete ACM/arXiv strings are now in `protocol/acm_arxiv_queries.md`: arXiv is corroborated by source code; ACM is author-supplied with original UI settings unverified.
- `scripts/validate_data.py`: checks supplied CSV integrity, parent-child metadata, numerical partitions, adjudication accounting, and derived reporting consistency.
- `scripts/reproduce_results.py`: regenerates the 55-row `results/summary_tables.csv`, four 300-DPI figures, and the derived reporting views below.
- `scripts/reporting_support.py`: shared CSV aggregation, column dictionary, and audit-report generation. Running it also refreshes `protocol/data_dictionary.csv`.
- `results/latency_statistics.csv`: All/READY observation quartiles, IQRs, report counts, and report-clustered medians corresponding to the numerical portion of Table 3.10.
- `results/rq4_category_statistics.csv`: category-level record/claim/report counts corresponding to the numerical portion of Table 3.12.
- `results/tier_sensitivity.csv`: claim/report indicators corresponding to Table 3.14.
- `results/manuscript_tables.md`: readable numerical views of those three tables.
- `results/adjudication_register.csv`: all 220 distinct recorded decision IDs linked to their affected records, source hashes, locators, rationales, and recorded sign-offs.
- `results/audit_summary.md`: generated final partitions, category counts, adjudication accounting, and scope limitations.

The scripts summarize final recorded adjudications; they do not independently repeat primary-source review or infer new adjudication decisions. Figure 2d displays only the four candidate groups recoverable from distributed fields, grouping red-zone R1-R4 together; subgroup history remains described in the manuscript. Figure 3b prioritizes Data_Status=NOT_REPORTED before grouping Unit. Figure 4c calculates source-evaluated counts from Exposure_Provenance_Class. Figure 4d retains explicit, labeled reference-size inputs in the plotting code; these are not calculated from the five data CSVs. The generator does not recreate every qualitative manuscript table.

## Adjudication accounting

**220 decisions = 86 RQ3 + 123 RQ4 + 11 P3 claim decisions.** The RQ3 decisions comprise 25 BUG and 61 REC IDs applied to 77 metric rows: 76 time rows with 85 decision IDs, plus the USD row `R12-E07-MET-081` / `HUM-RQ3-BUG-025`. Multiple decisions may affect one row. Crosswalk rows mirror the time decisions and are not counted again.

Canonical examples:

- Human comparators: 2,700 s and 4,200 s (`R1-E02-MET-137/138`, `REC-016/017`).
- Additional sibling duplicate: `PILOT-MET-007`, duplicating `R1-E05-MET-006`.
- Synthetic-zero/non-time exclusions: `REC-044/052`.
- Bound/model strata: MemLineage `<1 ms` (`REC-045`) and SAGA 220 ms model (`REC-049`).
- NiyamAI source conflicts: `CLM-0003`, `R1-E05-MET-006..008`.

## Availability and review limits

The search history reports 6,860 raw entries, 926 screened records, 610 full texts, 166 full-text exclusions, two linked companions, and 442 included canonical reports. Selection counts, exclusions, and agreement are now recomputable from the normalized registers in `screening/`. The total four-platform raw yield is reported history; compact arXiv exports reproduce its 4,142 returns / 3,894 base IDs / 529 gate-passing IDs.

This package now contains normalized Stage 1 decisions; Stage 2 eligibility/exclusion, reviewer, rigor, family-link and adjudication exports; and compact arXiv query/gate-pass provenance. Original XLSX files, full publisher exports/abstracts, primary PDFs, the Stage 3 workbook, the 1,951 underlying Stage 3 review-audit records, individual signatures, historical latency crosswalks, and the internal 107-candidate matrix are not redistributed. Export hashes preserve reported file identity; they do not replace the missing files. Reviewer names and sign-off strings are recorded provenance and do not authenticate reviewer independence.

The recorded data-release roles are Herman Kabetta (Reviewer 1), I Komang Setia Buana (Reviewer 2), and Raden Budiarto (Adjudicator). See `CITATION.cff` for citation metadata and `LICENSE` for licensing.

## Commands

From the package directory:

```bash
pip install -r requirements.txt
python scripts/screening_support.py
python scripts/reporting_support.py
python scripts/reproduce_results.py
python scripts/validate_data.py
```

These commands regenerate numerical reporting and figures without modifying `data/*.csv`. A validation PASS concerns the supplied dataset and reporting artifacts, not authentication of source-PDF contents, cryptographic proofs, reviewer identities, or historical ACM UI settings.


## Added screening evidence and unresolved source metadata

The complete file inventory and provenance are described in `screening/README.md`, `protocol/screening_register.md`, and `protocol/search_sources/source_manifest.json`. `scripts/screening_support.py` regenerates `results/screening_summary.json`, `results/screening_audit.md`, and `results/screening_date_issues.csv`. The Stage 2 workbook contains historical pilot extraction states; current Stage 3 completion uses `data/*.csv`. The user confirmed 2026-10-16 for all 104 flagged Reviewer 2 date entries. Active values are corrected; originals and confirmation provenance are retained in `protocol/screening_date_corrections.csv`. The active date-issue export has zero rows. Decisions, agreement, and all final adjudication dates are unchanged.
