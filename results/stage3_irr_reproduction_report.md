# Stage 3: reproduction from the supplied raw worksheets

4 November 2026. **This report supersedes the provisional interpretation of the first author-supplied summary.** The source package is preserved without modification under `../stage3_irr/`; all 18 input worksheet hashes are recorded in `stage3_irr_reproduction_audit.json`. The extended E05 file is excluded from pre-adjudication agreement because the package identifies it as a later split version.

## What was reproduced

The 18 worksheets contain 533 R1 and 508 R2 rows across nine batches. Both contain the same 442 report identifiers as canonical `studies.csv`, with the same recorded PDF hash within every report. This checks the recorded identifiers and hashes, not the contents of the original PDFs.

The author script uses the **first stored row per Source_Record_ID** for its primary N=442 comparison. It was rerun with output redirected so the supplied package was unchanged. Its complete summary CSV was reproduced exactly. Independent calculations from the raw rows also reproduced all 45 method/dimension combinations checked across first-row, single-claim-subset and ordered-pair analyses, to the reported four decimals. The independently generated pair locators, contingency cells, counts and coefficients are supplied alongside this report.

## Corrections to the earlier summary

| Item | Initial summary | Reproduced result |
|---|---|---|
| Grouped PQC | 427/442; κ .6399; AC1 .9654 | **431/442; 97.51%; κ .7320; AC1 .9726** |
| Support | Labeled binary; 367/442; κ .2878; AC1 .8074 | These values are correct for **three observed codes**: SUPPORTED_WITHIN_SCOPE, PARTIALLY_SUPPORTED, NOT_EVALUATED |
| Support dichotomy | Not reproduced in initial table | SUPPORTED versus all other recorded codes: **368/442; 83.26%; κ .2965; AC1 .7803**; this collapses a missing evaluation with partial support and is not the preferred substantive interpretation |
| Maturity categories | Seven in the initial message; five in package README | **Eight observed labels:** seven substantive categories and NE |

The earlier binary-feasibility audit remains a valid diagnostic for its stated input assumptions, but **does not describe a continuing unexplained coefficient failure**. The support discrepancy arose from the wrong category-count description; the revised raw package supplies different PQC counts and coefficients. The original message numbers remain in `author_reported_stage3_agreement.csv` as history, not current results.

Excluding the single NOT_EVALUATED support pair gives 367/441, 83.22%, κ .2863, AC1 .7806. Excluding two NE maturity pairs gives 230/440, 52.27%, κ .2904, AC1 .4671. Missing states are explicitly identified rather than silently interpreted as negative outcomes. These sensitivity results are in `stage3_irr_complete_case_sensitivity.csv`.

## Findings that materially qualify the synthesis

- **UG:** 180/442 matches, 40.72%, κ .0934, AC1 −.1831. R1 marks UG in 88 first rows and R2 in 334; joint positives are 80, joint negatives 100. This directional coding difference is much larger than the initial summary suggested.
- **Exact boundary sets:** 149/442, 33.71%, versus 87.56% for multiple/single and 87.10% for the collapsed five-class label. Agreement on MULTI does not establish agreement on which boundaries were involved.
- **Focused formal grouping:** 418/442 matches include **407 joint negatives and 11 joint positives**, with 10 R1-only and 14 R2-only positives. High Po alone is not strong positive-class agreement.
- **AD:** 396 matches include **394 joint positives and two joint negatives**. The initial interpretation of 396 as joint AD presence was slightly overstated.
- Formal type, maturity and lifecycle each match in 230/442 pairs. These remain the archived pre-adjudication judgments; adjudication does not prove that the initial rubric was reproducible.

## Pairing and selection sensitivity

Claim multiplicity agrees in 349/442 reports (78.96%; κ .2752; AC1 .7541). The pair-count distribution is (1,1):319, (1,2):34, (2,1):58, (2,2):29, (3,2):1, (3,3):1. Ordered pairing therefore yields 474 pairs and leaves 59 R1 and 34 R2 claims unmatched.

The 319 single-claim reports are a selected subset, not a claim-selection-independent sample. The ordered 474 pairs are not established semantic matches merely because their row positions align. Nevertheless, these alternatives show UG agreement remains 40.44%/41.56% and exact-boundary agreement 34.17%/34.18%. Thus differing numbers of claims do not alone explain the low agreement.

## Problems in alternative analyses supplied with the package

The author script's maturity rank dictionary uses labels that match **none** of the actual worksheet maturity values. All receive default rank −1, so “highest maturity” selects the first stored row when several claims occur. Its unchanged maturity result under aggregation is therefore not evidence of robustness. The supplied source script is preserved for provenance, but this aggregation is not used for the manuscript. A defensible replacement should explicitly define a substantive ordering, handle NE separately, or compare sets without pretending all maturity states have a natural total order.

The bipartite method maximizes agreement on claim category, target boundary, lifecycle and formal type. Its agreement on those same attributes is selection-conditioned and cannot independently validate them. Likewise, a formal-evidence ranking is an analysis choice, not a proven hierarchy of security assurance. The author's script regenerates the method-summary CSV, but does not regenerate its separate per-batch/alignment files; those files are not represented here as fully independently reproduced. The independent pair file provides exact raw row locators instead.

## Human approval confirmed; historical notes pending

The corresponding author confirms independent human review by Herman Kabetta and I Komang Setia Buana. However, the archived R1 files contain **148 UNASSIGNED extractor labels**, and **212 rationales explicitly describing an AI draft with human identity not yet assigned**. These sets overlap and must not be added together. All supplied reviewer rows have verification status EXTRACTED. The corresponding author subsequently clarified that **Herman checked and approved these supplied worksheets before adjudication**; the approval notes are being located. The labels are therefore treated as legacy metadata, not evidence that human review did not occur. The manuscript distinguishes author-confirmed human approval from independently reproduced worksheet calculations. No reviewer identity or state has been changed retrospectively.

## Reproduction

Run `python scripts/reproduce_stage3_irr.py` from the supplementary package (any working directory works). The implementation uses the Python standard library and reads the archived CSVs. Outputs include `stage3_irr_reproduced.csv`, `stage3_irr_contingency.csv`, `stage3_irr_pairs.csv`, `stage3_irr_batch_counts.csv`, complete-case sensitivities and the audit JSON. The script also reruns the supplied author script in a separate output directory. The archive's illustrative arithmetic connecting pre-adjudication counts to 584 final claims is not treated as a complete assertion-level lineage audit.
