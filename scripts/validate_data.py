#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_data.py — Referential Integrity, Denominator, and Final Bogor Sign-Off Validator (v3.6)
Verifies all structural invariants, PRISMA counts, RQ1–RQ4 denominators, and confirms
ZERO remaining HOLD or PENDING statuses across all 5 canonical CSV datasets.
"""

import pathlib
import sys
import numpy as np
import pandas as pd
from reporting_support import (load_tables, unit_groups, adjudication_register,
                               latency_statistics, category_statistics,
                               sensitivity_statistics)
from screening_support import compute as compute_screening
import json

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def main():
    studies = pd.read_csv(DATA / "studies.csv")
    claims = pd.read_csv(DATA / "claims.csv")
    rq3_m = pd.read_csv(DATA / "rq3_metrics.csv")
    rq3_cw = pd.read_csv(DATA / "rq3_latency_crosswalk.csv")
    rq4_dep = pd.read_csv(DATA / "rq4_dependencies.csv")

    # 1. Row and QA stratum counts
    assert len(studies) == 442, f"Expected 442 studies, got {len(studies)}"
    assert len(claims) == 584, f"Expected 584 claims, got {len(claims)}"
    assert int((claims["Claim_QA"] == "READY").sum()) == 530
    assert int((claims["Claim_QA"] == "FLAGGED").sum()) == 54
    assert len(rq3_m) == 1111, f"Expected 1111 RQ3 metrics, got {len(rq3_m)}"
    assert len(rq3_cw) == 454, f"Expected 454 RQ3 latency crosswalk rows, got {len(rq3_cw)}"
    assert len(rq4_dep) == 283, f"Expected 283 RQ4 dependency rows, got {len(rq4_dep)}"

    # Unique row identities and exact parent-child ownership, not just set membership.
    for frame, key in [(studies, "Source_Record_ID"), (claims, "Claim_ID"),
                       (rq3_m, "Metric_ID"), (rq3_cw, "Metric_ID"), (rq4_dep, "Dependency_ID")]:
        assert frame[key].notna().all() and frame[key].is_unique, f"Missing/duplicate {key}"
    parents = claims.set_index("Claim_ID")
    for frame in [rq3_m, rq3_cw, rq4_dep]:
        for col in ["Source_Record_ID", "Study_Family_ID", "Source_PDF_SHA256", "Claim_QA",
                    "Claim_Support_Status", "Implementation_Maturity", "PQC_Migration_Stage"]:
            if col in frame and col in parents:
                assert frame[col].eq(frame.Claim_ID.map(parents[col])).all(), f"Parent mismatch: {col}"
    assert claims.Source_PDF_SHA256.eq(claims.Source_Record_ID.map(studies.set_index("Source_Record_ID").Source_PDF_SHA256)).all()
    assert set(rq3_m.loc[rq3_m.Unit.isin(["ms", "s"]), "Metric_ID"]) == set(rq3_cw.Metric_ID)
    metric_parent = rq3_m.set_index("Metric_ID")
    for col in ["Claim_ID", "Source_Record_ID", "Adjudication_ID_v35"]:
        assert rq3_cw[col].fillna("").eq(rq3_cw.Metric_ID.map(metric_parent[col]).fillna("")).all()
    vals = rq3_cw.Metric_ID.map(metric_parent.Adjudicated_Numeric_Value_v35.fillna(metric_parent.Numeric_Value))
    units = rq3_cw.Metric_ID.map(metric_parent.Adjudicated_Unit_v35.fillna(metric_parent.Unit))
    normalized = vals * np.where(units.eq("s"), 1000, 1)
    valid = rq3_cw.Adjudicated_Latency_ms_v35.notna()
    assert np.allclose(normalized[valid], rq3_cw.loc[valid, "Adjudicated_Latency_ms_v35"])
    assert rq3_cw.loc[~valid, "Pooling_Eligibility_v35"].eq("EXCLUDED_SYNTHETIC_ZERO_OR_NON_TIME").all()

    # 2. Study_Family_ID normalization (SF-<Source_Record_ID>, 0 'SINGLE')
    for name, df in [("studies", studies), ("claims", claims), ("rq3_m", rq3_m), ("rq3_cw", rq3_cw), ("rq4_dep", rq4_dep)]:
        expected_sf = "SF-" + df["Source_Record_ID"].astype(str)
        assert (df["Study_Family_ID"] == expected_sf).all(), f"Study_Family_ID mismatch in {name}"
        assert not (df["Study_Family_ID"] == "SINGLE").any(), f"Found legacy SINGLE in {name}"
    assert claims["Study_Family_ID"].nunique() == 442

    # 3. Referential integrity across tables
    study_ids = set(studies["Source_Record_ID"])
    claim_ids = set(claims["Claim_ID"])
    claim_qa_map = claims.set_index("Claim_ID")["Claim_QA"].to_dict()
    assert set(claims["Source_Record_ID"]) == study_ids
    for name, df in [("rq3_metrics", rq3_m), ("rq3_latency_crosswalk", rq3_cw), ("rq4_dependencies", rq4_dep)]:
        assert set(df["Claim_ID"]).issubset(claim_ids), f"Orphan Claim_ID in {name}"
        assert set(df["Source_Record_ID"]).issubset(study_ids), f"Orphan Source_Record_ID in {name}"
        mapped_qa = df["Claim_ID"].map(claim_qa_map)
        assert (df["Claim_QA"] == mapped_qa).all(), f"Claim_QA mismatch in {name}"

    # 4. RQ1 multi-boundary & single-boundary invariants
    assert int((claims["Target_Boundary"] == "MULTI_BOUNDARY").sum()) == 472
    assert int(((claims["Target_Boundary"] == "MULTI_BOUNDARY") & (claims["Claim_QA"] == "READY")).sum()) == 425
    assert int((claims["Target_Boundary"] != "MULTI_BOUNDARY").sum()) == 112

    # 5. RQ2 Formal_Evidence_Type invariants (29 All / 27 READY)
    fe_counts = claims["Formal_Evidence_Type"].value_counts().to_dict()
    assert fe_counts.get("TOOL_SUPPORTED_VERIFICATION", 0) == 15
    assert fe_counts.get("SECURITY_REDUCTION", 0) == 11
    assert fe_counts.get("LOGICAL_AXIOMS_WITH_PROOF", 0) == 3
    strict_formal = ["TOOL_SUPPORTED_VERIFICATION", "SECURITY_REDUCTION", "LOGICAL_AXIOMS_WITH_PROOF"]
    f_all = int(claims["Formal_Evidence_Type"].isin(strict_formal).sum())
    f_rdy = int((claims["Formal_Evidence_Type"].isin(strict_formal) & (claims["Claim_QA"] == "READY")).sum())
    assert (f_all, f_rdy) == (29, 27), f"Expected (29, 27) strict formal claims, got {(f_all, f_rdy)}"

    # 5b. Finding A: RQ2 Limitation_Codes_DG_AD_UG_NG exact counts (All n=584 vs READY n=530)
    for lim_code, exp_all, exp_rdy in [("AD", 515, 463), ("DG", 240, 226), ("UG", 222, 169)]:
        has_lim = claims["Limitation_Codes_DG_AD_UG_NG"].fillna("").apply(lambda s: lim_code in [x.strip() for x in s.split(";")])
        got_all = int(has_lim.sum())
        got_rdy = int((has_lim & (claims["Claim_QA"] == "READY")).sum())
        assert (got_all, got_rdy) == (exp_all, exp_rdy), f"RQ2 {lim_code} mismatch: got {(got_all, got_rdy)}, expected {(exp_all, exp_rdy)}"

    # 6. Zero HOLD / Zero PENDING across all status columns & 220/220 Bogor Sign-Off verification
    status_cols_map = {
        "studies": (studies, ["Extraction_Status", "Verification_Status"]),
        "claims": (claims, ["Verification_Status", "Claim_QA", "QA_Adjudication_Disposition", "Human_Sign_Off_v35"]),
        "rq3_metrics": (rq3_m, ["Data_Status", "Verification_Status", "Reviewer1_Decision_v35", "Adjudicated_Action_v35", "Audit_Verification_State", "Public_Adjudication_Status", "Human_Sign_Off_v35"]),
        "rq3_latency_crosswalk": (rq3_cw, ["Data_Status", "Verification_Status", "Reclassified_Estimand_Level", "Audit_Verification_State", "Reviewer1_Decision_v35", "Pooling_Eligibility_v35", "Human_Sign_Off_v35", "Dim1_Timer_Boundary", "Public_Adjudication_Status"]),
        "rq4_dependencies": (rq4_dep, ["Reviewer_Inference_Status", "Analysis_Status", "Verification_Status", "Audit_Verification_State", "Reviewer1_Decision_v35", "Denominator_Status_v35", "Human_Sign_Off_v35", "Adjudicated_Category_v35", "Adjudicated_Exposure_Tier_v35", "Public_Adjudication_Status"]),
    }
    for tname, (df, cols) in status_cols_map.items():
        for c in cols:
            if c in df.columns:
                bad = df[c].fillna("").astype(str).str.contains(r"\bPENDING|\bHOLD|PENDING_|_HOLD", case=False, regex=True)
                assert not bad.any(), f"Found remaining PENDING/HOLD in {tname}.{c}: {df.loc[bad, c].unique().tolist()}"

    for tname, df in [("claims", claims), ("rq3_metrics", rq3_m), ("rq3_latency_crosswalk", rq3_cw), ("rq4_dependencies", rq4_dep)]:
        assert df["Human_Sign_Off_v35"].str.startswith("APPROVED_FINAL_2026-11-02 (R1: Herman Kabetta; R2: I Komang Setia Buana; Adjudicator: Raden Budiarto — Bogor)").all(), (
            f"Missing Bogor 2026-11-02 sign-off in {tname}"
        )

    adj_p3_ids = set(x for s in claims["Adjudication_ID_v35"].dropna() for x in str(s).split(";") if x.startswith("HUM-P3-"))
    adj_rq3_m_ids = set(x for s in rq3_m["Adjudication_ID_v35"].dropna() for x in str(s).split(";") if x.startswith("HUM-RQ3-"))
    adj_rq3_cw_ids = set(x for s in rq3_cw["Adjudication_ID_v35"].dropna() for x in str(s).split(";") if x.startswith("HUM-RQ3-"))
    adj_rq4_ids = set(x for s in rq4_dep["Adjudication_ID_v35"].dropna() for x in str(s).split(";") if x.startswith("HUM-RQ4-"))
    assert len(adj_p3_ids) == 11
    assert len(adj_rq3_m_ids) == 86
    assert len(adj_rq3_cw_ids) == 85
    assert len(adj_rq4_ids) == 123
    assert len(adj_p3_ids | adj_rq3_m_ids | adj_rq4_ids) == 220

    # 7. Exact RQ3 Pooling_Eligibility_v35 partition (n=454 -> 399 eligible [362 READY]; 0 HOLD)
    pe_counts = rq3_cw["Pooling_Eligibility_v35"].value_counts().to_dict()
    expected_pe = {
        "ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS": 399,
        "EXCLUDED_SIBLING_DUPLICATE": 26,
        "STRATIFIED_OFFLINE_SCAN_BATCH": 8,
        "STRATIFIED_ADVERSARIAL_OR_DETECTION_TIME": 5,
        "STRATIFIED_BATCH_OR_EPISODE_WORKLOAD": 4,
        "EXCLUDED_WARM_PATH_BYPASS_INDICATOR": 3,
        "QUARANTINED_SOURCE_TABLE_CONFLICT": 3,
        "EXCLUDED_HUMAN_BASELINE": 2,
        "EXCLUDED_SYNTHETIC_ZERO_OR_NON_TIME": 2,
        "STRATIFIED_BOUND_OR_MODELED_CURVE": 2,
    }
    assert pe_counts == expected_pe, f"Pooling_Eligibility_v35 mismatch: {pe_counts}"
    el_rdy = int(((rq3_cw["Pooling_Eligibility_v35"] == "ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS") & (rq3_cw["Claim_QA"] == "READY")).sum())
    assert el_rdy == 362

    # 8. Finding B: Exact RQ4 Record / Claim / Report unit accounting (283 Total = 266 Active [222 Concrete + 44 Suite NR] + 17 Excluded; 0 HOLD)
    excl_denom = rq4_dep["Denominator_Status_v35"].str.startswith("EXCLUDED_")
    excl_tier = rq4_dep["Adjudicated_Exposure_Tier_v35"] == "Non-Cryptographic Baselines & Excluded Own Non-Crypto"
    assert (excl_denom == excl_tier).all(), "Contradiction between Denominator_Status_v35 and Adjudicated_Exposure_Tier_v35"
    rdy_mask = rq4_dep["Claim_QA"] == "READY"
    suite_nr = rq4_dep["Adjudicated_Exposure_Tier_v35"] == "Unspecified Algorithm / Generic Scheme (Suite NR)"

    # Total RQ4 (283 records, 248 claims, 245 reports; READY: 241 records, 214 claims, 212 reports)
    assert (len(rq4_dep), rq4_dep["Claim_ID"].nunique(), rq4_dep["Source_Record_ID"].nunique()) == (283, 248, 245)
    assert (int(rdy_mask.sum()), rq4_dep.loc[rdy_mask, "Claim_ID"].nunique(), rq4_dep.loc[rdy_mask, "Source_Record_ID"].nunique()) == (241, 214, 212)

    # Active Crypto (266 records, 231 claims, 228 reports; READY: 224 records, 197 claims, 195 reports)
    act_mask = ~excl_denom
    assert (int(act_mask.sum()), rq4_dep.loc[act_mask, "Claim_ID"].nunique(), rq4_dep.loc[act_mask, "Source_Record_ID"].nunique()) == (266, 231, 228)
    assert (int((act_mask & rdy_mask).sum()), rq4_dep.loc[act_mask & rdy_mask, "Claim_ID"].nunique(), rq4_dep.loc[act_mask & rdy_mask, "Source_Record_ID"].nunique()) == (224, 197, 195)

    # Concrete Crypto (222 records, 189 claims, 186 reports; READY: 188 records, 162 claims, 160 reports)
    conc_mask = act_mask & (~suite_nr)
    assert (int(conc_mask.sum()), rq4_dep.loc[conc_mask, "Claim_ID"].nunique(), rq4_dep.loc[conc_mask, "Source_Record_ID"].nunique()) == (222, 189, 186)
    assert (int((conc_mask & rdy_mask).sum()), rq4_dep.loc[conc_mask & rdy_mask, "Claim_ID"].nunique(), rq4_dep.loc[conc_mask & rdy_mask, "Source_Record_ID"].nunique()) == (188, 162, 160)

    # Suite = NR (44 records, 44 claims, 44 reports; READY: 36 records, 36 claims, 36 reports)
    assert (int(suite_nr.sum()), rq4_dep.loc[suite_nr, "Claim_ID"].nunique(), rq4_dep.loc[suite_nr, "Source_Record_ID"].nunique()) == (44, 44, 44)
    assert (int((suite_nr & rdy_mask).sum()), rq4_dep.loc[suite_nr & rdy_mask, "Claim_ID"].nunique(), rq4_dep.loc[suite_nr & rdy_mask, "Source_Record_ID"].nunique()) == (36, 36, 36)

    # Excluded Non-Crypto (17 records, 17 claims, 17 reports; READY: 17 records, 17 claims, 17 reports)
    assert (int(excl_denom.sum()), rq4_dep.loc[excl_denom, "Claim_ID"].nunique(), rq4_dep.loc[excl_denom, "Source_Record_ID"].nunique()) == (17, 17, 17)
    assert (int((excl_denom & rdy_mask).sum()), rq4_dep.loc[excl_denom & rdy_mask, "Claim_ID"].nunique(), rq4_dep.loc[excl_denom & rdy_mask, "Source_Record_ID"].nunique()) == (17, 17, 17)

    # Reporting corrections: decision count differs from affected row count.
    assert rq3_m.Adjudication_ID_v35.notna().sum() == 77
    assert rq3_cw.Adjudication_ID_v35.notna().sum() == 76
    assert rq3_m.Audit_Verification_State.value_counts().to_dict() == {
        "VERIFIED_STAGE3_READY_V35": 952, "VERIFIED_FLAGGED_SENSITIVITY_STRATUM_V35": 82,
        "ADJUDICATED_FINAL_V35": 77}
    strict_pqc = claims[claims.PQC_Migration_Stage.str.startswith(("STAGE_4", "STAGE_5"))]
    assert strict_pqc.Source_Record_ID.nunique() == 4
    assert set(claims.loc[claims.Claim_QA.eq("FLAGGED") & claims.Claim_Support_Status.eq("SUPPORTED_WITHIN_SCOPE"), "Claim_ID"]) == {"CLM-0422"}
    assert int(((rq3_cw.Pooling_Eligibility_v35 == "EXCLUDED_SIBLING_DUPLICATE") & rq3_cw.Claim_QA.eq("READY")).sum()) == 23
    assert unit_groups(rq3_m).value_counts().sum() == 1111
    dictionary = pd.read_csv(ROOT / "protocol/data_dictionary.csv")
    actual_columns = {(path.name, col) for path in DATA.glob("*.csv") for col in pd.read_csv(path, nrows=0).columns}
    assert set(zip(dictionary.Table_Name, dictionary.Column_Name)) == actual_columns
    assert len(dictionary) == len(actual_columns) == 188
    tables = load_tables()
    expected_views = {
        "adjudication_register.csv": adjudication_register(tables),
        "latency_statistics.csv": latency_statistics(rq3_cw),
        "rq4_category_statistics.csv": category_statistics(rq4_dep),
        "tier_sensitivity.csv": sensitivity_statistics(claims, studies, rq4_dep),
    }
    for filename, expected in expected_views.items():
        actual = pd.read_csv(ROOT / "results" / filename).fillna("")
        pd.testing.assert_frame_equal(actual, expected.fillna("").reset_index(drop=True), check_dtype=False)
    screening, date_issues = compute_screening()
    stored = json.loads((ROOT / "results/screening_summary.json").read_text(encoding="utf-8"))
    assert stored == screening, "Screening summary differs from register recomputation"
    assert len(pd.read_csv(ROOT / "results/screening_date_issues.csv")) == len(date_issues) == 0
    corrections = pd.read_csv(ROOT / "protocol/screening_date_corrections.csv", dtype=str)
    assert len(corrections) == 104 and corrections.Corrected_Value.eq("2026-10-16").all()

    print("[PASS] Supplied CSV integrity, RQ1-RQ4 partitions, recorded sign-off fields, and derived reporting checks succeeded:")
    print("  - Sign-Off Authority: Reviewer 1: Herman Kabetta | Reviewer 2: I Komang Setia Buana | Adjudicator: Raden Budiarto (Bogor, 2 November 2026)")
    print(f"  - Studies: {len(studies)} canonical reports (442 unique Study_Family_IDs; 0 PENDING/HOLD)")
    print(f"  - Claims:  {len(claims)} claims (530 READY, 54 FLAGGED; 472 multi-boundary; 29/27 focused formal-category records, not independently replayed proofs; 0 PENDING/HOLD)")
    print(f"  - RQ3:     {len(rq3_m)} metrics -> {len(rq3_cw)} time rows -> 399 eligible online runtime (362 READY), 26 sibling dup, 3 quarantined source conflict, 26 non-online (0 HOLD)")
    print(f"  - RQ4:     {len(rq4_dep)} dependency rows -> 266 active crypto/attestation (224 READY: 222 concrete + 44 Suite NR) + 17 excluded non-crypto (17 READY) (0 HOLD)")
    print("  - Adjudication: 220/220 enacted and signed off (APPROVED_FINAL_2026-11-02), 0 pending / 0 hold rows across all tables.")
    print("  - Reporting: complete 188-column dictionary; 220 decision IDs across 77 RQ3 rows, 123 RQ4 rows, and 11 P3 claims.")
    print("  - Screening: 926 -> 610 -> 442 included / 166 excluded / 2 merged; kappa 0.4172 five-class / 0.4446 binary.")
    print("  - Dates: 104 user-confirmed R2 corrections to 2026-10-16; 0 active date issues; original values retained in correction ledger.")
    print("  - Scope: PASS does not authenticate human review, primary-PDF contents, or historical ACM UI settings.")

if __name__ == "__main__":
    main()
