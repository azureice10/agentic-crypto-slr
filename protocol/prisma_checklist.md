# PRISMA reporting and availability map

Release 3.6.3 / manuscript CS1 - 3 November 2026. Analytical baseline v3.5; recorded data-release sign-off 2 November 2026.

This map describes the supplied manuscript and supplementary files. It is not a certification of full PRISMA compliance, an independently verified screening register, or a substitute for the journal's complete reporting checklist. The PDF with the same basename is a rendered copy of this map.

## Data-supported reporting

| Reporting area | Available evidence and current interpretation |
|---|---|
| Title, rationale, and objectives | Manuscript Sections 1-2 identify a systematic review and define RQ1-RQ4 and boundaries B1-B4. |
| Included corpus and claim appraisal | studies.csv and claims.csv: 442 reports; 584 claims (530 READY, 54 FLAGGED); support 482 within scope, 101 partial, 1 unsupported. |
| Formal evidence and limitations | 29 focused-category claims (27 READY); 83 including THEORETIC_PROOF. Categories are not proof replay. AD 515, DG 240, UG 222. |
| Runtime synthesis | 1,111 metric rows (1,091 numeric + 20 NR); 454 time rows = 399 eligible + 26 duplicates + 3 quarantined conflicts + 26 other strata. READY pool: 362. |
| Quantum inventory | 283 inventory rows = 266 active dependencies (222 concrete-class + 44 Suite NR) + 17 excluded non-crypto. Stage 4-5: 7 claims / 4 reports; 4 READY / 2 reports. |
| Adjudication accounting | 220 distinct decision IDs = 86 RQ3 + 123 RQ4 + 11 P3. RQ3 decisions affect 77 rows (76 time + 1 USD). Flattened register: results/adjudication_register.csv. |
| Definitions and derived outputs | 188-column dictionary; 55-row summary; four figures; latency/category/tier views. CS1 adds post hoc role, QA, proof-definition, statistic and PQC-linkage sensitivity. |

## Reporting limitations and unavailable evidence

| Reporting area | Availability limit or qualification |
|---|---|
| Search expressions | Seven ACM/arXiv expressions are supplied. Four arXiv strings match archived code, including pagination/filter settings. ACM strings are author-supplied; original UI field/proximity settings remain unverified. |
| Selection flow and agreement | Normalized registers reproduce 926 screened, 610 full texts, 442 included, 166 excluded, 2 merged; kappa 0.4172 five-class / 0.4446 binary. Complete four-platform raw yield 6,860 remains reported history. |
| Screening and primary-source review | Stage 1/2 decisions, reviewer rows, exclusions, links, and compact arXiv provenance are supplied. Original XLSX files, primary PDFs, individual signatures, and the separate Stage 3 review-audit records are not redistributed. |
| Reviewer date metadata | User-confirmed date 2026-10-16 applied to all 104 flagged R2 entries. Originals remain in the correction ledger. No active date issues; labels and agreement unchanged. |
| Migration categories | NOT_DISCUSSED and Stage 0 retain batch-dependent historical labels and are combined as no demonstrated PQC migration. No active dependency link is not evidence of a non-cryptographic mechanism. |
| Figure inputs | Figures summarize CSV data; Figure 4d uses labeled size references. Latency medians mix source statistics; no pooled overhead is estimated. Scripts do not repeat human adjudication. |
| Historical artifacts | The 436/428-observation exploratory crosswalks and the internal 107-candidate matrix are not distributed. The final 454-row crosswalk is supplied. |
| Validation scope | PASS checks canonical data, screening joins, agreement, and derived reporting. It does not authenticate reviewer independence, primary-source judgments, or historical ACM UI settings. |

## Reproduction

Run scripts/screening_support.py, scripts/reporting_support.py, scripts/reproduce_results.py, then scripts/validate_data.py. Run node scripts/critical_synthesis.mjs for CS1 analyses (Node 22+). Python dependencies: requirements.txt; optional PDF dependencies: requirements-reporting.txt. Render with scripts/render_reporting_map.py.
