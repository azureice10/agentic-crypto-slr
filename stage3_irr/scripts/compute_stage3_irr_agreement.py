#!/usr/bin/env python3
"""
Standalone Reproducible Stage 3 Inter-Reviewer Agreement (IRR) Script
=====================================================================
Run from the root of `stage3_r1_r2_raw_worksheets_and_irr_package`:
    python3 scripts/compute_stage3_irr_agreement.py

Reads the 18 raw Stage 3 extraction worksheets:
  - `raw_reviewer_1_herman_kabetta/LEMBAR_KERJA_REVIEWER_1_BATCH_E01..E09_*.csv` (533 claims across 442 studies)
  - `raw_reviewer_2_i_komang_setia_buana/LEMBAR_KERJA_REVIEWER_2_BATCH_E01..E09_*.csv` (508 claims across 442 studies)

Computes exact observed agreement (Po), unweighted Cohen's kappa (k), and Gwet's AC1
under four explicit methodological rules:
  - Rule 1 (Study-Level Primary Claim, N = 442 studies): First/primary claim row per study (`index 0`).
  - Rule 2 (Study-Level Union/Aggregation, N = 442 studies): Union/hierarchical aggregation of all claims per study.
  - Rule 3A (Claim-Level 1-to-1 Subset, N = 319 studies/claims): Studies where both R1 and R2 extracted exactly 1 claim.
  - Rule 3B & 3C (Claim-Level Paired Claims, N = 474 pairs): All min(n_R1, n_R2) = 474 claim pairs matched by order (3B)
    and by maximum attribute similarity bipartite matching (3C), alongside Study-Level Claim-Multiplicity Agreement (N = 442).
"""

import csv
import itertools
import os
from collections import Counter, defaultdict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R1_DIR = os.path.join(ROOT_DIR, "raw_reviewer_1_herman_kabetta")
R2_DIR = os.path.join(ROOT_DIR, "raw_reviewer_2_i_komang_setia_buana")
RES_DIR = os.path.join(ROOT_DIR, "results")

BATCH_FILES = [
    ("BATCH_E01", "LEMBAR_KERJA_REVIEWER_1_BATCH_E01_TIER1_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E01_TIER1_50.csv"),
    ("BATCH_E02", "LEMBAR_KERJA_REVIEWER_1_BATCH_E02_TIER1_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E02_TIER1_50.csv"),
    ("BATCH_E03", "LEMBAR_KERJA_REVIEWER_1_BATCH_E03_TIER1_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E03_TIER1_50.csv"),
    ("BATCH_E04", "LEMBAR_KERJA_REVIEWER_1_BATCH_E04_TIER1_62.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E04_TIER1_62.csv"),
    ("BATCH_E05", "LEMBAR_KERJA_REVIEWER_1_BATCH_E05_PILOT_24.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E05_PILOT_24.csv"),
    ("BATCH_E06", "LEMBAR_KERJA_REVIEWER_1_BATCH_E06_ARXIV_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E06_ARXIV_50.csv"),
    ("BATCH_E07", "LEMBAR_KERJA_REVIEWER_1_BATCH_E07_ARXIV_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E07_ARXIV_50.csv"),
    ("BATCH_E08", "LEMBAR_KERJA_REVIEWER_1_BATCH_E08_ARXIV_50.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E08_ARXIV_50.csv"),
    ("BATCH_E09", "LEMBAR_KERJA_REVIEWER_1_BATCH_E09_ARXIV_56.csv", "LEMBAR_KERJA_REVIEWER_2_BATCH_E09_ARXIV_56.csv"),
]

FE_RANK = {
    "NONE": 0,
    "INFORMAL_ARGUMENT": 1,
    "FORMAL_MODEL": 2,
    "THEORETIC_PROOF": 3,
    "LOGICAL_AXIOMS_WITH_PROOF": 4,
    "SECURITY_REDUCTION": 5,
    "TOOL_SUPPORTED_VERIFICATION": 6,
}

IM_RANK = {
    "CONCEPTUAL_ARCHITECTURE_ONLY": 0,
    "SIMULATION_OR_EMULATION": 1,
    "PROOF_OF_CONCEPT_PROTOTYPE": 2,
    "BENCHMARKED_PROTOTYPE": 3,
    "PRODUCTION_OR_OPEN_WEIGHTS_DEPLOYED": 4,
}

CS_RANK = {
    "NOT_SUPPORTED": 0,
    "PARTIALLY_SUPPORTED": 1,
    "SUPPORTED_WITHIN_SCOPE": 2,
}

PQC_RANK = {
    "NOT_DISCUSSED": 0,
    "STAGE_0_PRE_QUANTUM_ONLY": 1,
    "STAGE_1_SUGGESTED_MIGRATION": 2,
    "STAGE_2_ANALYTICAL_PROPOSAL": 3,
    "STAGE_3_SIMULATION_OR_EMULATION": 4,
    "STAGE_4_PRIMITIVE_IMPLEMENTED": 5,
    "STAGE_5_AGENT_WORKLOAD_BENCHMARK": 6,
}


def calc_irr(pairs):
    """Computes exact agreement count, N, Po, unweighted Cohen's kappa, and Gwet's AC1."""
    n = len(pairs)
    if n == 0:
        return 0, 0, 0.0, 0.0, 0.0
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    cats = sorted(set(a for a, _ in pairs) | set(b for _, b in pairs))
    k = len(cats)
    if k <= 1:
        return agree, n, po, 1.0, 1.0
    c1 = Counter(a for a, _ in pairs)
    c2 = Counter(b for _, b in pairs)
    pe_k = sum((c1[c] / n) * (c2[c] / n) for c in cats)
    kappa = (po - pe_k) / (1.0 - pe_k) if (1.0 - pe_k) > 1e-12 else 1.0
    pis = [((c1[c] + c2[c]) / (2.0 * n)) for c in cats]
    pe_ac1 = (1.0 / (k - 1.0)) * sum(pi * (1.0 - pi) for pi in pis)
    ac1 = (po - pe_ac1) / (1.0 - pe_ac1) if (1.0 - pe_ac1) > 1e-12 else 1.0
    return agree, n, po, kappa, ac1


def get_lim_set(row):
    raw = (row.get("Limitation_Codes_DG_AD_UG_NG") or "").strip()
    return set(x.strip() for x in raw.split(";") if x.strip())


def get_bset(row):
    bc = (row.get("Boundary_Codes") or "").strip()
    if bc:
        parts = set(x.strip() for x in bc.split(";") if x.strip() in ("B1", "B2", "B3", "B4"))
        if parts:
            return parts
    tb = (row.get("Target_Boundary") or "").strip()
    if tb.startswith("B1"):
        return {"B1"}
    if tb.startswith("B2"):
        return {"B2"}
    if tb.startswith("B3"):
        return {"B3"}
    if tb.startswith("B4"):
        return {"B4"}
    return {"MULTI"}


def norm_pqc_collapsed(stage_str):
    s = (stage_str or "").strip()
    if s in ("NOT_DISCUSSED", "STAGE_0_PRE_QUANTUM_ONLY", ""):
        return "PRE_QUANTUM_OR_ND"
    return "PQC_STAGE_1_TO_5"


def extract_row_features(row):
    tb = row["Target_Boundary"].strip()
    fe = row["Formal_Evidence_Type"].strip()
    im = row["Implementation_Maturity"].strip()
    cs = row["Claim_Support_Status"].strip()
    cc = row["Claim_Category"].strip()
    lc = row["Lifecycle_Stage"].strip()
    pqc = row["PQC_Migration_Stage"].strip()
    lims = get_lim_set(row)
    bset = get_bset(row)
    return {
        "Source_PDF_SHA256": row["Source_PDF_SHA256"].strip(),
        "Target_Boundary_5Class": tb,
        "Target_Boundary_Binary": "MULTI_BOUNDARY" if tb == "MULTI_BOUNDARY" else "SINGLE_BOUNDARY",
        "Boundary_Set_Exact": ";".join(sorted(bset)),
        "Claim_Support_Status": cs,
        "Claim_Category": cc,
        "Lifecycle_Stage": lc,
        "Formal_Evidence_Type": fe,
        "Strict_Formal_Proof_Binary": "STRICT_FORMAL" if fe in ("TOOL_SUPPORTED_VERIFICATION", "SECURITY_REDUCTION", "LOGICAL_AXIOMS_WITH_PROOF") else "NON_STRICT",
        "Implementation_Maturity": im,
        "Limitation_AD_Binary": "YES" if "AD" in lims else "NO",
        "Limitation_DG_Binary": "YES" if "DG" in lims else "NO",
        "Limitation_UG_Binary": "YES" if "UG" in lims else "NO",
        "Limitation_Exact_Set": ";".join(sorted(lims)),
        "PQC_Migration_Stage_Exact": pqc,
        "PQC_Migration_Stage_Collapsed": norm_pqc_collapsed(pqc),
    }


def aggregate_study_features(rows):
    """Rule 2: Aggregates all claims extracted for a given study into a study-level profile."""
    if len(rows) == 1:
        return extract_row_features(rows[0])
    bset = set()
    tbs = set()
    lims = set()
    for r in rows:
        bset |= get_bset(r)
        tbs.add(r["Target_Boundary"].strip())
        lims |= get_lim_set(r)
    if "MULTI_BOUNDARY" in tbs or len(bset - {"MULTI"}) > 1 or len(tbs) > 1:
        tb_5 = "MULTI_BOUNDARY"
    else:
        tb_5 = next(iter(tbs))
    tb_bin = "MULTI_BOUNDARY" if tb_5 == "MULTI_BOUNDARY" else "SINGLE_BOUNDARY"
    fe_best = max((r["Formal_Evidence_Type"].strip() for r in rows), key=lambda x: FE_RANK.get(x, -1))
    im_best = max((r["Implementation_Maturity"].strip() for r in rows), key=lambda x: IM_RANK.get(x, -1))
    cs_min = min((r["Claim_Support_Status"].strip() for r in rows), key=lambda x: CS_RANK.get(x, 99))
    pqc_best = max((r["PQC_Migration_Stage"].strip() for r in rows), key=lambda x: PQC_RANK.get(x, -1))
    cc_union = ";".join(sorted(set(r["Claim_Category"].strip() for r in rows)))
    lc_union = ";".join(sorted(set(r["Lifecycle_Stage"].strip() for r in rows)))
    return {
        "Source_PDF_SHA256": rows[0]["Source_PDF_SHA256"].strip(),
        "Target_Boundary_5Class": tb_5,
        "Target_Boundary_Binary": tb_bin,
        "Boundary_Set_Exact": ";".join(sorted(bset - {"MULTI"})) if (bset - {"MULTI"}) else "MULTI",
        "Claim_Support_Status": cs_min,
        "Claim_Category": cc_union,
        "Lifecycle_Stage": lc_union,
        "Formal_Evidence_Type": fe_best,
        "Strict_Formal_Proof_Binary": "STRICT_FORMAL" if fe_best in ("TOOL_SUPPORTED_VERIFICATION", "SECURITY_REDUCTION", "LOGICAL_AXIOMS_WITH_PROOF") else "NON_STRICT",
        "Implementation_Maturity": im_best,
        "Limitation_AD_Binary": "YES" if "AD" in lims else "NO",
        "Limitation_DG_Binary": "YES" if "DG" in lims else "NO",
        "Limitation_UG_Binary": "YES" if "UG" in lims else "NO",
        "Limitation_Exact_Set": ";".join(sorted(lims)),
        "PQC_Migration_Stage_Exact": pqc_best,
        "PQC_Migration_Stage_Collapsed": norm_pqc_collapsed(pqc_best),
    }


def match_bipartite_rows(L1, L2):
    """Rule 3C: Pairs min(len(L1), len(L2)) claims within a study by maximum attribute similarity."""
    if len(L1) == 1 and len(L2) == 1:
        return [(L1[0], L2[0])]
    best_pairs = None
    best_score = -1
    if len(L1) <= len(L2):
        for perm in itertools.permutations(range(len(L2)), len(L1)):
            score = sum(
                (L1[i]["Claim_Category"].strip() == L2[j]["Claim_Category"].strip()) * 4
                + (L1[i]["Target_Boundary"].strip() == L2[j]["Target_Boundary"].strip()) * 3
                + (L1[i]["Lifecycle_Stage"].strip() == L2[j]["Lifecycle_Stage"].strip()) * 2
                + (L1[i]["Formal_Evidence_Type"].strip() == L2[j]["Formal_Evidence_Type"].strip()) * 1
                + (1 if i == j else 0)
                for i, j in enumerate(perm)
            )
            if score > best_score:
                best_score = score
                best_pairs = [(L1[i], L2[j]) for i, j in enumerate(perm)]
    else:
        for perm in itertools.permutations(range(len(L1)), len(L2)):
            score = sum(
                (L1[i]["Claim_Category"].strip() == L2[j]["Claim_Category"].strip()) * 4
                + (L1[i]["Target_Boundary"].strip() == L2[j]["Target_Boundary"].strip()) * 3
                + (L1[i]["Lifecycle_Stage"].strip() == L2[j]["Lifecycle_Stage"].strip()) * 2
                + (L1[i]["Formal_Evidence_Type"].strip() == L2[j]["Formal_Evidence_Type"].strip()) * 1
                + (1 if i == j else 0)
                for j, i in enumerate(perm)
            )
            if score > best_score:
                best_score = score
                best_pairs = [(L1[i], L2[j]) for j, i in enumerate(perm)]
    return best_pairs


def main():
    os.makedirs(RES_DIR, exist_ok=True)
    r1_by_study = defaultdict(list)
    r2_by_study = defaultdict(list)
    study_order = []
    study_batch = {}

    for batch_id, f1_name, f2_name in BATCH_FILES:
        p1 = os.path.join(R1_DIR, f1_name)
        p2 = os.path.join(R2_DIR, f2_name)
        with open(p1, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                s = row["Source_Record_ID"].strip()
                if s not in r1_by_study:
                    study_order.append(s)
                    study_batch[s] = batch_id
                r1_by_study[s].append(row)
        with open(p2, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                s = row["Source_Record_ID"].strip()
                r2_by_study[s].append(row)

    assert len(study_order) == 442, f"Expected 442 canonical studies, got {len(study_order)}"
    total_r1 = sum(len(v) for v in r1_by_study.values())
    total_r2 = sum(len(v) for v in r2_by_study.values())
    print(f"[PASS] Loaded 442 canonical studies across 9 batches (R1={total_r1} claims, R2={total_r2} claims).")

    mult_pairs = [(str(len(r1_by_study[s])), str(len(r2_by_study[s]))) for s in study_order]
    m_ag, m_n, m_po, m_k, m_ac1 = calc_irr(mult_pairs)

    dimensions = [
        "Source_PDF_SHA256",
        "PQC_Migration_Stage_Collapsed",
        "Strict_Formal_Proof_Binary",
        "Limitation_AD_Binary",
        "Target_Boundary_Binary",
        "Target_Boundary_5Class",
        "Claim_Support_Status",
        "Limitation_DG_Binary",
        "Claim_Category",
        "PQC_Migration_Stage_Exact",
        "Boundary_Set_Exact",
        "Lifecycle_Stage",
        "Formal_Evidence_Type",
        "Implementation_Maturity",
        "Limitation_UG_Binary",
        "Limitation_Exact_Set",
    ]

    summary_rows = [{
        "Dimension": "Claim_Count_Per_Study_Exact (1 vs 2 vs 3)",
        "Rule1_Primary_Study_N442_Agree": f"{m_ag}/442 ({m_po*100:.2f}%)",
        "Rule1_Kappa": f"{m_k:.4f}",
        "Rule1_AC1": f"{m_ac1:.4f}",
        "Rule2_Union_Study_N442_Agree": f"{m_ag}/442 ({m_po*100:.2f}%)",
        "Rule2_Kappa": f"{m_k:.4f}",
        "Rule2_AC1": f"{m_ac1:.4f}",
        "Rule3A_1to1_Claims_N319_Agree": "319/319 (100.00%)",
        "Rule3A_Kappa": "1.0000",
        "Rule3A_AC1": "1.0000",
        "Rule3B_OrderPaired_N474_Agree": "N/A (study-level multiplicity)",
        "Rule3B_Kappa": "N/A",
        "Rule3B_AC1": "N/A",
        "Rule3C_BipartitePaired_N474_Agree": "N/A (study-level multiplicity)",
        "Rule3C_Kappa": "N/A",
        "Rule3C_AC1": "N/A",
    }]

    for dim in dimensions:
        p1 = [(extract_row_features(r1_by_study[s][0])[dim], extract_row_features(r2_by_study[s][0])[dim]) for s in study_order]
        p2 = [(aggregate_study_features(r1_by_study[s])[dim], aggregate_study_features(r2_by_study[s])[dim]) for s in study_order]
        p3a = [
            (extract_row_features(r1_by_study[s][0])[dim], extract_row_features(r2_by_study[s][0])[dim])
            for s in study_order
            if len(r1_by_study[s]) == 1 and len(r2_by_study[s]) == 1
        ]
        p3b, p3c = [], []
        for s in study_order:
            L1, L2 = r1_by_study[s], r2_by_study[s]
            for k in range(min(len(L1), len(L2))):
                p3b.append((extract_row_features(L1[k])[dim], extract_row_features(L2[k])[dim]))
            for ra, rb in match_bipartite_rows(L1, L2):
                p3c.append((extract_row_features(ra)[dim], extract_row_features(rb)[dim]))

        a1, n1, po1, k1, ac1 = calc_irr(p1)
        a2, n2, po2, k2, ac2 = calc_irr(p2)
        a3a, n3a, po3a, k3a, ac3a = calc_irr(p3a)
        a3b, n3b, po3b, k3b, ac3b = calc_irr(p3b)
        a3c, n3c, po3c, k3c, ac3c = calc_irr(p3c)

        summary_rows.append({
            "Dimension": dim,
            "Rule1_Primary_Study_N442_Agree": f"{a1}/{n1} ({po1*100:.2f}%)",
            "Rule1_Kappa": f"{k1:.4f}",
            "Rule1_AC1": f"{ac1:.4f}",
            "Rule2_Union_Study_N442_Agree": f"{a2}/{n2} ({po2*100:.2f}%)",
            "Rule2_Kappa": f"{k2:.4f}",
            "Rule2_AC1": f"{ac2:.4f}",
            "Rule3A_1to1_Claims_N319_Agree": f"{a3a}/{n3a} ({po3a*100:.2f}%)",
            "Rule3A_Kappa": f"{k3a:.4f}",
            "Rule3A_AC1": f"{ac3a:.4f}",
            "Rule3B_OrderPaired_N474_Agree": f"{a3b}/{n3b} ({po3b*100:.2f}%)",
            "Rule3B_Kappa": f"{k3b:.4f}",
            "Rule3B_AC1": f"{ac3b:.4f}",
            "Rule3C_BipartitePaired_N474_Agree": f"{a3c}/{n3c} ({po3c*100:.2f}%)",
            "Rule3C_Kappa": f"{k3c:.4f}",
            "Rule3C_AC1": f"{ac3c:.4f}",
        })

    with open(os.path.join(RES_DIR, "stage3_irr_by_method.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)

    print("[PASS] Regenerated results/stage3_irr_by_method.csv")


if __name__ == "__main__":
    main()
