#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reproduce_results.py — End-to-End Reproducible Synthesis & Figure Generator (v3.5)
Computes all RQ1–RQ4 summary tables (`results/summary_tables.csv`) AND regenerates
all four 300-DPI publication figures (`figures/figure_1_rq1.png` .. `figure_4_rq4.png`)
directly from the canonical datasets in `data/*.csv`.
"""

import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reporting_support import unit_groups, qa_zones, generate_reporting

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Calibri"],
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 0.8,
})

def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)

    studies = pd.read_csv(DATA / "studies.csv")
    claims = pd.read_csv(DATA / "claims.csv")
    rq3_m = pd.read_csv(DATA / "rq3_metrics.csv")
    rq3_cw = pd.read_csv(DATA / "rq3_latency_crosswalk.csv")
    rq4_dep = pd.read_csv(DATA / "rq4_dependencies.csv")

    rows = []

    # --------------------------------------------------------------------------
    # 1. RQ1 SUMMARY TABLE METRICS
    # --------------------------------------------------------------------------
    mb_all = int((claims["Target_Boundary"] == "MULTI_BOUNDARY").sum())
    mb_rdy = int(((claims["Target_Boundary"] == "MULTI_BOUNDARY") & (claims["Claim_QA"] == "READY")).sum())
    sb_all = int((claims["Target_Boundary"] != "MULTI_BOUNDARY").sum())
    sb_rdy = int(((claims["Target_Boundary"] != "MULTI_BOUNDARY") & (claims["Claim_QA"] == "READY")).sum())
    assert (mb_all, mb_rdy, sb_all, sb_rdy) == (472, 425, 112, 105)

    rows.append({
        "RQ": "RQ1", "Group": "Boundary_Scope", "Stratum": "Multi_Boundary_Claims",
        "All_Count": mb_all, "READY_Count": mb_rdy,
        "All_Pct_or_p50_ms": round(mb_all / len(claims) * 100, 1),
        "READY_Pct_or_p50_ms": round(mb_rdy / 530 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "472/584 (80.8%) all claims; 425/530 (80.2%) READY claims"
    })
    rows.append({
        "RQ": "RQ1", "Group": "Boundary_Scope", "Stratum": "Single_Boundary_Claims",
        "All_Count": sb_all, "READY_Count": sb_rdy,
        "All_Pct_or_p50_ms": round(sb_all / len(claims) * 100, 1),
        "READY_Pct_or_p50_ms": round(sb_rdy / 530 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "B1=1, B2=25, B3=55, B4=31"
    })

    b_Counts = {}
    for b in ["B1", "B2", "B3", "B4"]:
        has_b = claims["Boundary_Codes"].fillna("").apply(lambda s: b in [x.strip() for x in s.split(";")])
        b_all = int(has_b.sum())
        b_rdy = int((has_b & (claims["Claim_QA"] == "READY")).sum())
        s_all = int(claims.loc[has_b, "Source_Record_ID"].nunique())
        s_rdy = int(claims.loc[has_b & (claims["Claim_QA"] == "READY"), "Source_Record_ID"].nunique())
        b_Counts[b] = (b_all, b_rdy, s_all, s_rdy)
        rows.append({
            "RQ": "RQ1", "Group": "Boundary_Incidence", "Stratum": b,
            "All_Count": b_all, "READY_Count": b_rdy,
            "All_Pct_or_p50_ms": round(b_all / len(claims) * 100, 1),
            "READY_Pct_or_p50_ms": round(b_rdy / 530 * 100, 1),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": f"Non-exclusive boundary involvement ({s_all}/442 All reports; {s_rdy}/406 READY reports)"
        })

    # --------------------------------------------------------------------------
    # 2. RQ2 SUMMARY TABLE METRICS (FIXED P0-1 WITH EXPLICIT ASSERTIONS)
    # --------------------------------------------------------------------------
    formal_types = ["TOOL_SUPPORTED_VERIFICATION", "SECURITY_REDUCTION", "LOGICAL_AXIOMS_WITH_PROOF"]
    f_all = int(claims["Formal_Evidence_Type"].isin(formal_types).sum())
    f_rdy = int((claims["Formal_Evidence_Type"].isin(formal_types) & (claims["Claim_QA"] == "READY")).sum())
    assert (f_all, f_rdy) == (29, 27), f"P0-1 assertion failed: got {(f_all, f_rdy)}"

    rows.append({
        "RQ": "RQ2", "Group": "Formal_Verification", "Stratum": "Machine_Checked_or_Crypto_Reduction_or_Axiomatic_Total",
        "All_Count": f_all, "READY_Count": f_rdy,
        "All_Pct_or_p50_ms": round(f_all / len(claims) * 100, 1),
        "READY_Pct_or_p50_ms": round(f_rdy / 530 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "TOOL_SUPPORTED_VERIFICATION (15/13 READY) + SECURITY_REDUCTION (11/11 READY) + LOGICAL_AXIOMS_WITH_PROOF (3/3 READY)"
    })

    for ft in [
        "INFORMAL_ARGUMENT", "NONE", "FORMAL_MODEL", "THEORETIC_PROOF",
        "TOOL_SUPPORTED_VERIFICATION", "SECURITY_REDUCTION", "LOGICAL_AXIOMS_WITH_PROOF"
    ]:
        sub_ft = claims[claims["Formal_Evidence_Type"] == ft]
        ft_a = len(sub_ft)
        ft_r = int((sub_ft["Claim_QA"] == "READY").sum())
        rows.append({
            "RQ": "RQ2", "Group": "Formal_Evidence_Type_Breakdown", "Stratum": ft,
            "All_Count": ft_a, "READY_Count": ft_r,
            "All_Pct_or_p50_ms": round(ft_a / len(claims) * 100, 1),
            "READY_Pct_or_p50_ms": round(ft_r / 530 * 100, 1),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": "Exact Formal_Evidence_Type category count in data/claims.csv"
        })

    for lim in ["AD", "DG", "UG"]:
        has_l = claims["Limitation_Codes_DG_AD_UG_NG"].fillna("").apply(lambda s: lim in [x.strip() for x in s.split(";")])
        l_all = int(has_l.sum())
        l_rdy = int((has_l & (claims["Claim_QA"] == "READY")).sum())
        rows.append({
            "RQ": "RQ2", "Group": "Limitation_Codes", "Stratum": lim,
            "All_Count": l_all, "READY_Count": l_rdy,
            "All_Pct_or_p50_ms": round(l_all / len(claims) * 100, 1),
            "READY_Pct_or_p50_ms": round(l_rdy / 530 * 100, 1),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": "Methodological limitation incidence"
        })

    # --------------------------------------------------------------------------
    # 3. RQ3 SUMMARY TABLE METRICS (P1-1: DYNAMIC POOLING DISPOSITIONS + FAMILIES + L1-L4)
    # --------------------------------------------------------------------------
    for disp, grp_d in rq3_cw.groupby("Pooling_Eligibility_v35"):
        d_all = len(grp_d)
        d_rdy = int((grp_d["Claim_QA"] == "READY").sum())
        rows.append({
            "RQ": "RQ3", "Group": "Pooling_Eligibility_v35", "Stratum": disp,
            "All_Count": d_all, "READY_Count": d_rdy,
            "All_Pct_or_p50_ms": round(d_all / len(rq3_cw) * 100, 1),
            "READY_Pct_or_p50_ms": round(d_rdy / int((rq3_cw["Claim_QA"] == "READY").sum()) * 100, 1),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": f"Crosswalk disposition ({d_all}/454 All; {d_rdy}/414 READY)"
        })

    el = rq3_cw[rq3_cw["Pooling_Eligibility_v35"] == "ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS"].copy()
    el["Adjudicated_Latency_ms_v35"] = el["Adjudicated_Latency_ms_v35"].astype(float)
    el_rdy = el[el["Claim_QA"] == "READY"].copy()
    assert (len(el), len(el_rdy)) == (399, 362)

    for fam in sorted(el["Reclassified_Mechanism_Family"].unique()):
        sub_all = el[el["Reclassified_Mechanism_Family"] == fam]["Adjudicated_Latency_ms_v35"]
        sub_r = el_rdy[el_rdy["Reclassified_Mechanism_Family"] == fam]
        rep_meds = sub_r.groupby("Source_Record_ID")["Adjudicated_Latency_ms_v35"].median()
        rows.append({
            "RQ": "RQ3", "Group": "Mechanism_Family_Latency", "Stratum": fam,
            "All_Count": len(sub_all), "READY_Count": len(sub_r),
            "All_Pct_or_p50_ms": round(float(sub_all.median()), 4),
            "READY_Pct_or_p50_ms": round(float(sub_r["Adjudicated_Latency_ms_v35"].median()), 4),
            "Report_Clustered_READY_p50_ms": round(float(rep_meds.median()), 4),
            "Notes": f"{sub_r['Source_Record_ID'].nunique()} canonical READY reports"
        })

    for est in sorted(el["Reclassified_Estimand_Level"].unique()):
        sub_all = el[el["Reclassified_Estimand_Level"] == est]["Adjudicated_Latency_ms_v35"]
        sub_r = el_rdy[el_rdy["Reclassified_Estimand_Level"] == est]
        rep_meds = sub_r.groupby("Source_Record_ID")["Adjudicated_Latency_ms_v35"].median()
        rows.append({
            "RQ": "RQ3", "Group": "Estimand_Level_Latency", "Stratum": est,
            "All_Count": len(sub_all), "READY_Count": len(sub_r),
            "All_Pct_or_p50_ms": round(float(sub_all.median()), 4),
            "READY_Pct_or_p50_ms": round(float(sub_r["Adjudicated_Latency_ms_v35"].median()), 4),
            "Report_Clustered_READY_p50_ms": round(float(rep_meds.median()), 4),
            "Notes": f"{sub_r['Source_Record_ID'].nunique()} canonical READY reports"
        })

    # --------------------------------------------------------------------------
    # 4. RQ4 SUMMARY TABLE METRICS (266 ACTIVE CRYPTO [222 CONCRETE + 44 SUITE NR] + 17 EXCLUDED = 283; 0 HOLD)
    # --------------------------------------------------------------------------
    excl_mask = rq4_dep["Denominator_Status_v35"].str.startswith("EXCLUDED_")
    nr_mask = rq4_dep["Adjudicated_Exposure_Tier_v35"] == "Unspecified Algorithm / Generic Scheme (Suite NR)"
    act_all = int((~excl_mask).sum())
    act_rdy = int(((~excl_mask) & (rq4_dep["Claim_QA"] == "READY")).sum())
    conc_all = int(((~excl_mask) & (~nr_mask)).sum())
    conc_rdy = int(((~excl_mask) & (~nr_mask) & (rq4_dep["Claim_QA"] == "READY")).sum())
    nr_all = int(nr_mask.sum())
    nr_rdy = int((nr_mask & (rq4_dep["Claim_QA"] == "READY")).sum())
    ex_all = int(excl_mask.sum())
    ex_rdy = int((excl_mask & (rq4_dep["Claim_QA"] == "READY")).sum())
    assert (act_all, act_rdy, conc_all, conc_rdy, nr_all, nr_rdy, ex_all, ex_rdy) == (266, 224, 222, 188, 44, 36, 17, 17)

    rows.append({
        "RQ": "RQ4", "Group": "Population_Partition", "Stratum": "Active_Crypto_Attestation_Dependencies_Total",
        "All_Count": act_all, "READY_Count": act_rdy,
        "All_Pct_or_p50_ms": round(act_all / len(rq4_dep) * 100, 1),
        "READY_Pct_or_p50_ms": round(act_rdy / 241 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "266 active records (231 claims / 228 reports; 224 READY across 197 READY claims / 195 READY reports) = 222 concrete (188 READY) + 44 Suite=NR (36 READY)"
    })
    rows.append({
        "RQ": "RQ4", "Group": "Population_Partition", "Stratum": "Active_Concrete_Algorithm_Protocol_Enclave_Subset",
        "All_Count": conc_all, "READY_Count": conc_rdy,
        "All_Pct_or_p50_ms": round(conc_all / len(rq4_dep) * 100, 1),
        "READY_Pct_or_p50_ms": round(conc_rdy / 241 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "222 concrete records (189 claims / 186 reports; 188 READY across 162 READY claims / 160 READY reports), excluding 44 Suite=NR"
    })
    rows.append({
        "RQ": "RQ4", "Group": "Population_Partition", "Stratum": "Excluded_Non_Crypto_Baselines_and_Rejected_Labels",
        "All_Count": ex_all, "READY_Count": ex_rdy,
        "All_Pct_or_p50_ms": round(ex_all / len(rq4_dep) * 100, 1),
        "READY_Pct_or_p50_ms": round(ex_rdy / 241 * 100, 1),
        "Report_Clustered_READY_p50_ms": np.nan,
        "Notes": "17 excluded non-crypto records (17 READY claims / 17 READY reports) = 8 EXCLUDED_OWN_NON_CRYPTO + 7 REJECT_CLASS + 2 explicit baselines"
    })

    for tier, grp in rq4_dep.groupby("Adjudicated_Exposure_Tier_v35"):
        t_all = len(grp)
        t_rdy = int((grp["Claim_QA"] == "READY").sum())
        rows.append({
            "RQ": "RQ4", "Group": "Quantum_Exposure_Tier", "Stratum": tier,
            "All_Count": t_all, "READY_Count": t_rdy,
            "All_Pct_or_p50_ms": round(t_all / len(rq4_dep) * 100, 1),
            "READY_Pct_or_p50_ms": round(t_rdy / 241 * 100, 1),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": f"{grp['Claim_ID'].nunique()} unique claims ({grp.loc[grp['Claim_QA']=='READY', 'Claim_ID'].nunique()} READY) / {grp['Source_Record_ID'].nunique()} canonical reports ({grp.loc[grp['Claim_QA']=='READY', 'Source_Record_ID'].nunique()} READY)"
        })

    for stg, grp in claims.groupby("PQC_Migration_Stage"):
        s_all = len(grp)
        s_rdy = int((grp["Claim_QA"] == "READY").sum())
        rows.append({
            "RQ": "RQ4", "Group": "Claim_Level_PQC_Stage", "Stratum": stg,
            "All_Count": s_all, "READY_Count": s_rdy,
            "All_Pct_or_p50_ms": round(s_all / len(claims) * 100, 2),
            "READY_Pct_or_p50_ms": round(s_rdy / 530 * 100, 2),
            "Report_Clustered_READY_p50_ms": np.nan,
            "Notes": "Claim-level PQC migration readiness"
        })

    out_df = pd.DataFrame(rows)
    out_path = RESULTS / "summary_tables.csv"
    out_df.to_csv(out_path, index=False)
    generate_reporting(RESULTS)

    # --------------------------------------------------------------------------
    # 5. REGENERATE ALL FOUR 300-DPI FIGURES FROM data/*.csv (P1-4)
    # --------------------------------------------------------------------------
    generate_figure_1(claims)
    generate_figure_2(claims)
    generate_figure_3(claims, rq3_m, rq3_cw, el, el_rdy)
    generate_figure_4(claims, rq4_dep)

    print(f"[SUCCESS] Wrote {len(out_df)} summary rows to {out_path} and regenerated all 4 300-DPI figures in {FIGS}")

def generate_figure_1(claims: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(18.5, 13.0), dpi=300)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "Figure 1. RQ1: Trust Boundary Coverage Across Units & Roles, Exact Combination Lattice, and Lifecycle Matrix (n = 584 Claims, 442 Studies)",
        fontsize=13.2, fontweight="bold", color="#1B365D", y=0.98
    )

    # Panel (a): Non-Exclusive Boundary Involvement Across Units of Analysis
    ax_a = axes[0, 0]
    b_codes = ["B1", "B2", "B3", "B4"]
    b_labels = ["B1: Intent ->\nDelegation", "B2: Delegation ->\nRequest", "B3: Request ->\nExecution", "B4: Execution ->\nAudit"]
    c_all, c_rdy, s_all, s_rdy = [], [], [], []
    for b in b_codes:
        has_b = claims["Boundary_Codes"].fillna("").apply(lambda s: b in [x.strip() for x in s.split(";")])
        c_all.append(int(has_b.sum()) / 584 * 100)
        c_rdy.append(int((has_b & (claims["Claim_QA"] == "READY")).sum()) / 530 * 100)
        s_all.append(int(claims.loc[has_b, "Source_Record_ID"].nunique()) / 442 * 100)
        s_rdy.append(int(claims.loc[has_b & (claims["Claim_QA"] == "READY"), "Source_Record_ID"].nunique()) / 406 * 100)
    raw_counts = [
        (int(round(c_all[i]*584/100)), int(round(c_rdy[i]*530/100)), int(round(s_all[i]*442/100)), int(round(s_rdy[i]*406/100)))
        for i in range(4)
    ]
    x = np.arange(4)
    w = 0.19
    bars1 = ax_a.bar(x - 1.5*w, c_all, w, color="#1B365D", label="All Claims (n=584)")
    bars2 = ax_a.bar(x - 0.5*w, c_rdy, w, color="#159A6E", label="READY Claims (n=530)")
    bars3 = ax_a.bar(x + 0.5*w, s_all, w, color="#D97706", label="All Canonical Reports (n=442)")
    bars4 = ax_a.bar(x + 1.5*w, s_rdy, w, color="#4A607A", label="Reports with READY Claims (n=406)")
    for idx_b, (b1_i, b2_i, b3_i, b4_i) in enumerate(zip(bars1, bars2, bars3, bars4)):
        rc = raw_counts[idx_b]
        for bar, cnt in zip([b1_i, b2_i, b3_i, b4_i], rc):
            h = bar.get_height()
            ax_a.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}%\n({cnt})", ha="center", va="bottom", fontsize=6.8, fontweight="bold")
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(b_labels, fontsize=9.5, fontweight="bold")
    ax_a.set_ylim(0, 108)
    ax_a.set_ylabel("Percentage of Unit Population (%)", fontsize=9.5, fontweight="bold")
    ax_a.set_title("(a) Non-Exclusive Boundary Involvement Across Units of Analysis", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_a.grid(axis="y", linestyle="--", alpha=0.45)
    ax_a.legend(loc="upper left", fontsize=8, frameon=True)

    # Panel (b): Boundary Involvement Stratified by Claim Role (n=584)
    ax_b = axes[0, 1]
    def role_of(cat):
        if cat in ["DEFENSIVE_MECHANISM", "FORMAL_FRAMEWORK", "SYSTEM_PROTOTYPE"]:
            return "Def"
        elif cat == "EMPIRICAL_BENCHMARK":
            return "Bench"
        return "Atk"
    roles = claims["Claim_Category"].apply(role_of)
    def_c, ben_c, atk_c = [], [], []
    for b in b_codes:
        has_b = claims["Boundary_Codes"].fillna("").apply(lambda s: b in [x.strip() for x in s.split(";")])
        def_c.append(int((has_b & (roles == "Def")).sum()))
        ben_c.append(int((has_b & (roles == "Bench")).sum()))
        atk_c.append(int((has_b & (roles == "Atk")).sum()))
    w_b = 0.25
    rb1 = ax_b.bar(x - w_b, def_c, w_b, color="#159A6E", label="Defensive / Formal / Prototype (n=346)")
    rb2 = ax_b.bar(x, ben_c, w_b, color="#4A607A", label="Empirical Benchmark (n=126)")
    rb3 = ax_b.bar(x + w_b, atk_c, w_b, color="#C0392B", label="Attack / Vulnerability Surface (n=112)")
    for bars, denom in [(rb1, 346), (rb2, 126), (rb3, 112)]:
        for bar in bars:
            h = int(bar.get_height())
            ax_b.text(bar.get_x() + bar.get_width()/2, h + 4, f"{h}\n({h/denom*100:.0f}%)", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(b_labels, fontsize=9.5, fontweight="bold")
    ax_b.set_ylim(0, 345)
    ax_b.set_ylabel("Number of Claims (and % Within Role)", fontsize=9.5, fontweight="bold")
    ax_b.set_title("(b) Boundary Involvement Stratified by Claim Role (n = 584)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_b.grid(axis="y", linestyle="--", alpha=0.45)
    ax_b.legend(loc="upper right", fontsize=8.2, frameon=True)

    # Panel (c): Exact Boundary Combination Lattice (Multi=472 [80.8%]; Single=112 [19.2%])
    ax_c = axes[1, 0]
    comb_vc = claims["Boundary_Codes"].value_counts()
    comb_names = list(comb_vc.index)
    comb_vals = list(comb_vc.values)
    xc = np.arange(len(comb_names))
    colors_c = ["#1B365D" if ";" in k else "#D97706" for k in comb_names]
    bars_c = ax_c.bar(xc, comb_vals, color=colors_c, width=0.65)
    for bar, v in zip(bars_c, comb_vals):
        ax_c.text(bar.get_x() + bar.get_width()/2, v + 3, f"{v}\n({v/584*100:.1f}%)", ha="center", va="bottom", fontsize=7.2, fontweight="bold")
    ax_c.set_xticks(xc)
    ax_c.set_xticklabels(comb_names, rotation=38, ha="right", fontsize=8, fontweight="bold")
    ax_c.set_ylim(0, 210)
    ax_c.set_ylabel("Number of Claims (n = 584)", fontsize=9.5, fontweight="bold")
    ax_c.set_title("(c) Exact Boundary Combinations (Multi = 472 [80.8%]; Single = 112 [19.2%])", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_c.grid(axis="y", linestyle="--", alpha=0.45)

    # Panel (d): Lifecycle Stage x Boundary Matrix (Cell Count & Row %)
    ax_d = axes[1, 1]
    lc_order = [
        ("TOOL_INVOCATION", "Tool Invocation (361)"),
        ("EXECUTION", "Execution (61)"),
        ("POST_EXECUTION_AUDIT", "Post-Exec Audit (45)"),
        ("INTER_AGENT_COMMS", "Inter-Agent Comms (35)"),
        ("AGENT_DISCOVERY", "Agent Discovery (26)"),
        ("NEGOTIATION_ORCHESTRATION", "Negotiation/Orch. (19)"),
        ("PLANNING_REASONING", "Planning/Reasoning (14)"),
        ("MEMORY_PERSISTENCE", "Memory Persistence (14)"),
        ("PROMPT_INGESTION", "Prompt Ingestion (9)"),
    ]
    mat_cnt = np.zeros((len(lc_order), 4), dtype=int)
    mat_pct = np.zeros((len(lc_order), 4), dtype=float)
    for r_idx, (lc_k, _) in enumerate(lc_order):
        sub_lc = claims[claims["Lifecycle_Stage"] == lc_k]
        tot_lc = len(sub_lc)
        for c_idx, b in enumerate(b_codes):
            cnt_b = int(sub_lc["Boundary_Codes"].fillna("").apply(lambda s: b in [x.strip() for x in s.split(";")]).sum())
            mat_cnt[r_idx, c_idx] = cnt_b
            mat_pct[r_idx, c_idx] = (cnt_b / tot_lc * 100.0) if tot_lc > 0 else 0.0
    im = ax_d.imshow(mat_pct, cmap="YlGnBu", aspect="auto", vmin=0, vmax=100)
    ax_d.set_xticks(np.arange(4))
    ax_d.set_xticklabels(["B1", "B2", "B3", "B4"], fontsize=9.5, fontweight="bold")
    ax_d.set_yticks(np.arange(len(lc_order)))
    ax_d.set_yticklabels([lbl for _, lbl in lc_order], fontsize=8.8, fontweight="bold")
    for r_idx in range(len(lc_order)):
        for c_idx in range(4):
            val_c = mat_cnt[r_idx, c_idx]
            val_p = mat_pct[r_idx, c_idx]
            txt_col = "white" if val_p >= 55 else "#1B365D"
            ax_d.text(c_idx, r_idx, f"{val_c} ({val_p:.0f}%)", ha="center", va="center", fontsize=8, fontweight="bold", color=txt_col)
    ax_d.set_title("(d) Lifecycle Stage x Boundary Matrix (Cell Count & Row %)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    plt.colorbar(im, ax=ax_d, fraction=0.046, pad=0.04, label="Row % Within Lifecycle Stage")

    plt.tight_layout(rect=[0.01, 0.01, 0.99, 0.94])
    fig.savefig(FIGS / "figure_1_rq1.png", dpi=300, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def generate_figure_2(claims: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(18.5, 13.0), dpi=300)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "Figure 2. RQ2: Evidence Strength, Support Status vs. Unproved Generalization (UG), and Forensic QA Release Gate (n = 584 Claims)",
        fontsize=13.2, fontweight="bold", color="#1B365D", y=0.98
    )

    # Panel (a): Formal Evidence Type by Support & Release Status (n=584)
    ax_a = axes[0, 0]
    fe_items = [
        ("INFORMAL_ARGUMENT", "Informal Argument"),
        ("NONE", "None (Empirical/Arch Only)"),
        ("FORMAL_MODEL", "Formal Model (Unproved)"),
        ("THEORETIC_PROOF", "Hand-Written Theoretic Proof"),
        ("TOOL_SUPPORTED_VERIFICATION", "Tool-Supported Verification*"),
        ("SECURITY_REDUCTION", "Cryptographic Reduction*"),
        ("LOGICAL_AXIOMS_WITH_PROOF", "Logical Axioms with Proof*"),
    ][::-1]
    sws_r, ps_r, flg_all, tot_fe, rdy_fe = [], [], [], [], []
    for k, _ in fe_items:
        sub = claims[claims["Formal_Evidence_Type"] == k]
        s_r = int(((sub["Claim_Support_Status"] == "SUPPORTED_WITHIN_SCOPE") & (sub["Claim_QA"] == "READY")).sum())
        p_r = int(((sub["Claim_Support_Status"] == "PARTIALLY_SUPPORTED") & (sub["Claim_QA"] == "READY")).sum())
        fl = int((sub["Claim_QA"] == "FLAGGED").sum())
        sws_r.append(s_r)
        ps_r.append(p_r)
        flg_all.append(fl)
        tot_fe.append(len(sub))
        rdy_fe.append(s_r + p_r)
    y_a = np.arange(len(fe_items))
    ax_a.barh(y_a, sws_r, height=0.55, color="#159A6E", label="Supported Within Scope (READY)")
    ax_a.barh(y_a, ps_r, left=sws_r, height=0.55, color="#D97706", label="Partially Supported (READY)")
    left_flg = np.array(sws_r) + np.array(ps_r)
    ax_a.barh(y_a, flg_all, left=left_flg, height=0.55, color="#C0392B", label="FLAGGED (PS=52, SWS=1, NS=1)")
    for i, (t_v, r_v) in enumerate(zip(tot_fe, rdy_fe)):
        ax_a.text(t_v + 3, y_a[i], f"{t_v} ({t_v/584*100:.1f}%) [{r_v} READY]", va="center", fontsize=8.2, fontweight="bold", color="#1B365D")
    ax_a.set_yticks(y_a)
    ax_a.set_yticklabels([lbl for _, lbl in fe_items], fontsize=8.8, fontweight="bold")
    ax_a.set_xlim(0, 265)
    ax_a.set_xlabel("Recorded categories (* = focused group: 29 All / 27 READY)\nIncluding theoretic proofs: 83 All / 80 READY; no independent proof replay", fontsize=8.5, fontweight="bold")
    ax_a.set_title("(a) Formal Evidence Type by Support & Release Status (n = 584)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_a.grid(axis="x", linestyle="--", alpha=0.45)
    ax_a.legend(loc="lower right", fontsize=8, frameon=True)

    # Panel (b): Reconciling Support Status (82.5% Supported) vs. UG Incidence (38.0%)
    ax_b = axes[0, 1]
    has_ug = claims["Limitation_Codes_DG_AD_UG_NG"].fillna("").apply(lambda s: "UG" in [x.strip() for x in s.split(";")])
    sup_groups = ["Supported Within Scope\n(n=482 [82.5%]; 481 READY)", "Partially Supported\n(n=101 [17.3%]; 49 READY)", "Not Supported\n(n=1 [0.2%]; 0 READY)"]
    sup_keys = ["SUPPORTED_WITHIN_SCOPE", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED"]
    no_ug_c = [int(((claims["Claim_Support_Status"] == k) & (~has_ug)).sum()) for k in sup_keys]
    ug_rdy_c = [int(((claims["Claim_Support_Status"] == k) & has_ug & (claims["Claim_QA"] == "READY")).sum()) for k in sup_keys]
    ug_flg_c = [int(((claims["Claim_Support_Status"] == k) & has_ug & (claims["Claim_QA"] == "FLAGGED")).sum()) for k in sup_keys]
    xb = np.arange(3)
    wb = 0.25
    b_noug = ax_b.bar(xb - wb, no_ug_c, wb, color="#1B365D", label="No UG Code (n=362)")
    b_ugr = ax_b.bar(xb, ug_rdy_c, wb, color="#D97706", label="Has UG — READY (n=169)")
    b_ugf = ax_b.bar(xb + wb, ug_flg_c, wb, color="#C0392B", label="Has UG — FLAGGED (n=53)")
    for bars in [b_noug, b_ugr, b_ugf]:
        for bar in bars:
            h = int(bar.get_height())
            if h > 0:
                ax_b.text(bar.get_x() + bar.get_width()/2, h + 6, f"{h}\n({h/584*100:.1f}%)", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax_b.set_xticks(xb)
    ax_b.set_xticklabels(sup_groups, fontsize=8.8, fontweight="bold")
    ax_b.set_ylim(0, 415)
    ax_b.set_ylabel("Number of Claims (Total UG = 222 [38.0%])", fontsize=9.5, fontweight="bold")
    ax_b.set_title("(b) Reconciling Support Status (82.5% Supported) vs. UG Incidence (38.0%)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_b.grid(axis="y", linestyle="--", alpha=0.45)
    ax_b.legend(loc="upper right", fontsize=8.2, frameon=True)

    # Panel (c): Methodological Limitation Combinations (AD=515, DG=240, UG=222, NG=0)
    ax_c = axes[1, 0]
    lim_order = [
        ("AD", "AD only"),
        ("AD;UG", "AD;UG"),
        ("DG;AD", "DG;AD"),
        ("DG;AD;UG", "DG;AD;UG"),
        ("DG", "DG only"),
        ("DG;UG", "DG;UG"),
        ("UG", "UG only"),
        ("NG", "NG (No Gap)"),
    ][::-1]
    l_all, l_rdy = [], []
    for lk, _ in lim_order:
        sub_l = claims[claims["Limitation_Codes_DG_AD_UG_NG"] == lk]
        l_all.append(len(sub_l))
        l_rdy.append(int((sub_l["Claim_QA"] == "READY").sum()))
    yc = np.arange(len(lim_order))
    hc = 0.36
    ax_c.barh(yc + hc/2, l_all, height=hc, color="#4A607A", label="All Claims (n=584)")
    ax_c.barh(yc - hc/2, l_rdy, height=hc, color="#159A6E", label="READY Claims (n=530)")
    for i, (va, vr) in enumerate(zip(l_all, l_rdy)):
        ax_c.text(va + 3, yc[i] + hc/2, f"{va} ({va/584*100:.1f}%)", va="center", fontsize=8, fontweight="bold", color="#2B3A42")
        ax_c.text(vr + 3, yc[i] - hc/2, f"{vr} ({vr/530*100:.1f}%)", va="center", fontsize=8, fontweight="bold", color="#159A6E")
    ax_c.set_yticks(yc)
    ax_c.set_yticklabels([lbl for _, lbl in lim_order], fontsize=8.8, fontweight="bold")
    ax_c.set_xlim(0, 260)
    ax_c.set_xlabel("Number of Claims (0 Claims Coded NG)", fontsize=9.2, fontweight="bold")
    ax_c.set_title("(c) Methodological Limitation Combinations (AD=515, DG=240, UG=222, NG=0)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_c.grid(axis="x", linestyle="--", alpha=0.45)
    ax_c.legend(loc="lower right", fontsize=8.2, frameon=True)

    # Panel (d): Forensic Release Gate (Paket B, n=107): 53 Promoted vs. 54 Retained FLAGGED
    ax_d = axes[1, 1]
    studies = pd.read_csv(DATA / "studies.csv")
    pb_items = qa_zones(claims, studies)[::-1]
    yd = np.arange(len(pb_items))
    vals_d = [d[1] for d in pb_items]
    cols_d = [d[2] for d in pb_items]
    ax_d.barh(yd, vals_d, height=0.55, color=cols_d)
    for i, v in enumerate(vals_d):
        ax_d.text(v + 0.8, yd[i], f"{v} ({v/107*100:.1f}%)", va="center", fontsize=8.5, fontweight="bold", color="#1B365D")
    ax_d.set_yticks(yd)
    ax_d.set_yticklabels([d[0] for d in pb_items], fontsize=8.2, fontweight="bold")
    ax_d.set_xlim(0, 62)
    ax_d.set_xlabel("Number of Audited Claims in Paket B (n = 107 Candidates)", fontsize=9.2, fontweight="bold")
    ax_d.set_title("(d) Forensic Release Gate (Paket B, n=107): 53 Promoted vs. 54 Retained FLAGGED", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_d.grid(axis="x", linestyle="--", alpha=0.45)

    plt.tight_layout(rect=[0.01, 0.01, 0.99, 0.94])
    fig.savefig(FIGS / "figure_2_rq2.png", dpi=300, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def generate_figure_3(claims: pd.DataFrame, rq3_m: pd.DataFrame, rq3_cw: pd.DataFrame, el: pd.DataFrame, el_rdy: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(18.5, 13.0), dpi=300)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "Figure 3 (v3.5 Adjudicated). RQ3: Implementation Maturity (n=584), Disjoint Unit Partition (n=1,111),\n"
        "and Post-Adjudication Deduplicated Latency Across Mechanism Families & Estimands (n=399 All / n=362 READY)",
        fontsize=13.2, fontweight="bold", color="#1B365D", y=0.98
    )

    # Panel (a): Implementation Maturity Profile computed from claims.csv
    ax_a = axes[0, 0]
    mat_map = [
        ("CONTROLLED_BENCHMARK", "Controlled Benchmark"),
        ("PROOF_OF_CONCEPT", "Proof of Concept (PoC)"),
        ("RESEARCH_PROTOTYPE_SIMULATOR", "Research Simulator"),
        ("CONCEPTUAL_ARCHITECTURE", "Conceptual Architecture"),
        ("DEPLOYMENT_LIKE_EVALUATION", "Deployment-Like Eval."),
        ("FORMAL_MODEL_ONLY", "Formal Model Only"),
        ("PRODUCTION_DEPLOYED", "Production Deployed"),
    ][::-1]
    mat_all, mat_rdy = [], []
    for mk, _ in mat_map:
        sub_m = claims[claims["Implementation_Maturity"] == mk]
        mat_all.append(len(sub_m))
        mat_rdy.append(int((sub_m["Claim_QA"] == "READY").sum()))
    y_a = np.arange(len(mat_map))
    h_a = 0.36
    ax_a.barh(y_a + h_a/2, mat_all, height=h_a, color="#5C6B73", label="All Extracted Claims (n = 584)")
    ax_a.barh(y_a - h_a/2, mat_rdy, height=h_a, color="#1D8A73", label="QA-Released READY Claims (n = 530)")
    for i, (va, vr) in enumerate(zip(mat_all, mat_rdy)):
        ax_a.text(va + 3, y_a[i] + h_a/2, f"{va} ({va/584*100:.1f}%)", va="center", fontsize=8.5, fontweight="bold", color="#2B3A42")
        ax_a.text(vr + 3, y_a[i] - h_a/2, f"{vr} ({vr/530*100:.1f}%)", va="center", fontsize=8.5, fontweight="bold", color="#1D8A73")
    ax_a.set_yticks(y_a)
    ax_a.set_yticklabels([lbl for _, lbl in mat_map], fontsize=9, fontweight="bold")
    ax_a.set_xlim(0, 310)
    ax_a.set_xlabel("Number of Claims", fontsize=9.5, fontweight="bold")
    ax_a.set_title("(a) Implementation Maturity Profile (All n=584 vs. READY n=530)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_a.grid(axis="x", linestyle="--", alpha=0.45)
    ax_a.legend(loc="lower right", fontsize=8.5, frameon=True)

    # Panel (b): Disjoint Unit Accounting (n=1,111)
    ax_b = axes[0, 1]
    unit_labels = [
        "percent (%)", "ms (milliseconds)", "s (seconds)", "tokens",
        "fraction (0-1)", "NOT_REPORTED (NR)", "KB / bytes", "ops/s / TPS / s/token", "USD / gas"
    ][::-1]
    groups = unit_groups(rq3_m)
    unit_all = [int(groups.eq(label).sum()) for label in unit_labels]
    unit_rdy = [int((groups.eq(label) & rq3_m.Claim_QA.eq("READY")).sum()) for label in unit_labels]
    y_b = np.arange(len(unit_labels))
    ax_b.barh(y_b + h_a/2, unit_all, height=h_a, color="#4A607A", label="All RQ3 Records (n = 1,111)")
    ax_b.barh(y_b - h_a/2, unit_rdy, height=h_a, color="#159A6E", label="QA-Released READY (n = 1,020; 1,008 numeric)")
    for i, (va, vr) in enumerate(zip(unit_all, unit_rdy)):
        ax_b.text(va + 4, y_b[i] + h_a/2, f"{va} ({va/1111*100:.1f}%)", va="center", fontsize=8.5, fontweight="bold", color="#2B3A42")
        ax_b.text(vr + 4, y_b[i] - h_a/2, f"{vr}", va="center", fontsize=8.5, fontweight="bold", color="#159A6E")
    ax_b.set_yticks(y_b)
    ax_b.set_yticklabels(unit_labels, fontsize=9, fontweight="bold")
    ax_b.set_xlim(0, 455)
    ax_b.set_xlabel("Number of RQ3 Observations (Exact Sum = 1,111; 25 Regex Fixes -> 15 Unique Obs.)", fontsize=9.2, fontweight="bold")
    ax_b.set_title("(b) Disjoint Unit Accounting (n=1,111; 454 Time Rows = 312 ms + 142 s)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_b.grid(axis="x", linestyle="--", alpha=0.45)
    ax_b.legend(loc="lower right", fontsize=8.5, frameon=True)

    # Panel (c): Mechanism Family Latency computed dynamically from el_rdy
    ax_c = axes[1, 0]
    fam_meta = [
        ("1. Classical Crypto / Token Gate", "1. Classical Crypto / Token Gate\n(n=110 READY dedup, 55 reports)", "5.39"),
        ("2. PQC / Quantum Primitives", "2. PQC / Quantum (n=3 READY*)\n(2 reports; small-sample caveat)", "0.082"),
        ("3. Deterministic Policy / Kernel", "3. Deterministic Policy / Kernel\n(n=18 READY dedup, 14 reports)", "79.50"),
        ("4. End-to-End Agent Workflows", "4. End-to-End Agent Workflows\n(n=130 READY dedup, 62 reports)", "335.00"),
        ("5. Blockchain / Consensus Ledger", "5. Blockchain / Consensus Ledger\n(n=32 READY dedup, 11 reports)", "1700.00"),
        ("6. Hardware TEE / ORAM Enclave", "6. Hardware TEE / ORAM Enclave\n(n=31 READY dedup, 6 reports)", "1565.00"),
        ("7. LLM-Judge / Quorum / FHE", "7. LLM-Judge / Quorum / FHE / ZKP\n(n=38 READY dedup, 17 reports)", "1694.50"),
    ][::-1]
    y_c = np.arange(len(fam_meta))
    fam_lbls, fam_obs, fam_rep, fam_v34 = [], [], [], []
    for fk, flbl, v34_s in fam_meta:
        sub_r = el_rdy[el_rdy["Reclassified_Mechanism_Family"] == fk]
        fam_lbls.append(flbl)
        fam_obs.append(float(sub_r["Adjudicated_Latency_ms_v35"].median()))
        fam_rep.append(float(sub_r.groupby("Source_Record_ID")["Adjudicated_Latency_ms_v35"].median().median()))
        fam_v34.append(v34_s)
    ax_c.barh(y_c + h_a/2, fam_obs, height=h_a, color="#158F76", label="Median of READY extracted values (n=362)")
    ax_c.barh(y_c - h_a/2, fam_rep, height=h_a, color="#2D74DA", label="Median of within-report medians")
    ax_c.set_xscale("log")
    ax_c.set_xlim(1e-2, 5e7)
    for i, (vo, vr, v34) in enumerate(zip(fam_obs, fam_rep, fam_v34)):
        vo_text = f"{vo:,.3f}".rstrip("0").rstrip(".")
        ax_c.text(vo * 1.35, y_c[i] + h_a/2, f"Value median={vo_text} ms", va="center", fontsize=8, fontweight="bold", color="#1A3038")
        ax_c.text(vr * 1.35, y_c[i] - h_a/2, f"Report median={vr:.2f} ms", va="center", fontsize=8, fontweight="bold", color="#2D74DA")
    ax_c.set_yticks(y_c)
    ax_c.set_yticklabels(fam_lbls, fontsize=8.5, fontweight="bold")
    ax_c.set_ylim(-1.15, 6.55)
    ax_c.set_xlabel("Reported time (ms, log scale); mixed workloads and source statistics\nFamily medians do not isolate incremental component overhead", fontsize=8.5, fontweight="bold")
    ax_c.set_title("(c) Mechanism Families: Extracted-Value and Report Medians", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_c.grid(axis="x", linestyle="--", alpha=0.45)
    ax_c.legend(loc="lower right", fontsize=8, frameon=True)

    # Panel (d): Operational Estimands computed dynamically from el_rdy
    ax_d = axes[1, 1]
    est_meta = [
        ("L1: Primitive / Crypto Micro-Op", "L1: Primitive / Crypto Micro-Op\n(n=78 READY dedup, 33 reports)", "1.81"),
        ("L2: Per-Request Policy / Gate Check", "L2: Per-Request Policy / Gate Check\n(n=51 READY dedup, 32 reports)", "9.85"),
        ("L3: Session / Enclave / Consensus / Proof Setup", "L3: Session / Enclave / Proof Setup\n(n=40 READY dedup, 17 reports)", "1691.73"),
        ("L4: End-to-End Agent Workflow Runtime", "L4: End-to-End Agent Workflow\n(n=193 READY dedup, 96 reports)", "1315.00"),
    ][::-1]
    y_d = np.arange(len(est_meta))
    est_lbls, est_obs, est_rep, est_v34 = [], [], [], []
    for ek, elbl, v34_s in est_meta:
        sub_r = el_rdy[el_rdy["Reclassified_Estimand_Level"] == ek]
        est_lbls.append(elbl)
        est_obs.append(float(sub_r["Adjudicated_Latency_ms_v35"].median()))
        est_rep.append(float(sub_r.groupby("Source_Record_ID")["Adjudicated_Latency_ms_v35"].median().median()))
        est_v34.append(v34_s)
    ax_d.barh(y_d + h_a/2, est_obs, height=h_a, color="#D97706", label="Median of READY extracted values (n=362)")
    ax_d.barh(y_d - h_a/2, est_rep, height=h_a, color="#1B365D", label="Median of within-report medians")
    ax_d.set_xscale("log")
    ax_d.set_xlim(1e-1, 5e7)
    for i, (vo, vr, v34) in enumerate(zip(est_obs, est_rep, est_v34)):
        ax_d.text(vo * 1.35, y_d[i] + h_a/2, f"Value median={vo:.2f} ms", va="center", fontsize=8.5, fontweight="bold", color="#B45309")
        ax_d.text(vr * 1.35, y_d[i] - h_a/2, f"Report median={vr:.2f} ms", va="center", fontsize=8.5, fontweight="bold", color="#1B365D")
    ax_d.set_yticks(y_d)
    ax_d.set_yticklabels(est_lbls, fontsize=8.8, fontweight="bold")
    ax_d.set_xlabel("Reported time (ms, log scale); not pooled runtime quantiles\nREADY inputs: 337 mean/point, 17 median, 7 p95, 1 p99", fontsize=8.5, fontweight="bold")
    ax_d.set_title("(d) Operational Estimands (L1-L4; v3.5 Dedup n=399 All / n=362 READY)", fontsize=10.8, fontweight="bold", color="#1B365D", pad=10)
    ax_d.grid(axis="x", linestyle="--", alpha=0.45)
    ax_d.legend(loc="upper right", fontsize=8, frameon=True)

    plt.tight_layout(rect=[0.01, 0.01, 0.99, 0.94])
    fig.savefig(FIGS / "figure_3_rq3.png", dpi=300, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def generate_figure_4(claims: pd.DataFrame, rq4_dep: pd.DataFrame):
    fig4, axes4 = plt.subplots(2, 2, figsize=(19.0, 13.2), dpi=300)
    fig4.patch.set_facecolor("white")
    fig4.suptitle(
        "Figure 4. RQ4: PQC Readiness by Record Linkage (584 Claims: 231 Active-Dependency-Linked + 353 Without Active Links),\n"
        "Dependency Records (n=283 Records across 248 Claims / 245 Reports: 266 Active [231 Clm / 228 Rep] + 17 Excluded [17 Clm / 17 Rep]), Exposure Tiers & Wire Sizes",
        fontsize=13.0, fontweight="bold", color="#1B365D", y=0.98
    )

    # Panel (a): PQC Migration Stage by Claim-Level Join computed from claims & rq4_dep
    ax4_a = axes4[0, 0]
    active_cids = set(rq4_dep.loc[~rq4_dep["Denominator_Status_v35"].str.startswith("EXCLUDED_"), "Claim_ID"])
    stg_meta = [
        ("NOT_DISCUSSED", "Not Discussed (408)"),
        ("STAGE_0_PRE_QUANTUM_ONLY", "Stage 0: Pre-Quantum Only (152)"),
        ("STAGE_1_SUGGESTED_MIGRATION", "Stage 1: Suggested Migration (11)"),
        ("STAGE_5_AGENT_WORKLOAD_BENCHMARK", "Stage 5: Agent Workload Bench (5)"),
        ("STAGE_3_SIMULATION_OR_EMULATION", "Stage 3: Simulation / Emulation (4)"),
        ("STAGE_2_ANALYTICAL_PROPOSAL", "Stage 2: Analytical Proposal (2)"),
        ("STAGE_4_PRIMITIVE_IMPLEMENTED", "Stage 4: Primitive Implemented (2)"),
    ][::-1]
    c_rdy_crypto, c_flg_crypto, c_rdy_non, c_flg_non = [], [], [], []
    for sk, _ in stg_meta:
        sub_s = claims[claims["PQC_Migration_Stage"] == sk]
        in_act = sub_s["Claim_ID"].isin(active_cids)
        is_rdy = sub_s["Claim_QA"] == "READY"
        c_rdy_crypto.append(int((in_act & is_rdy).sum()))
        c_flg_crypto.append(int((in_act & (~is_rdy)).sum()))
        c_rdy_non.append(int(((~in_act) & is_rdy).sum()))
        c_flg_non.append(int(((~in_act) & (~is_rdy)).sum()))
    y4_a = np.arange(len(stg_meta))
    h4 = 0.48
    ax4_a.barh(y4_a, c_rdy_crypto, height=h4, color="#1B365D", label=f"Active dependency linked, READY (n={sum(c_rdy_crypto)})")
    left2 = np.array(c_rdy_crypto)
    ax4_a.barh(y4_a, c_flg_crypto, left=left2, height=h4, color="#D62828", label=f"Active dependency linked, FLAGGED (n={sum(c_flg_crypto)})")
    left3 = left2 + np.array(c_flg_crypto)
    ax4_a.barh(y4_a, c_rdy_non, left=left3, height=h4, color="#2A9D8F", label=f"No active dependency link, READY (n={sum(c_rdy_non)})")
    left4 = left3 + np.array(c_rdy_non)
    ax4_a.barh(y4_a, c_flg_non, left=left4, height=h4, color="#E76F51", label=f"No active dependency link, FLAGGED (n={sum(c_flg_non)})")
    totals_4a = left4 + np.array(c_flg_non)
    for i, tot in enumerate(totals_4a):
        cr_tot = c_rdy_crypto[i] + c_flg_crypto[i]
        ax4_a.text(tot + 6, y4_a[i], f"Total={tot} (Linked={cr_tot}: {c_rdy_crypto[i]}R/{c_flg_crypto[i]}F)", va="center", fontsize=8.2, fontweight="bold", color="#1F2937")
    ax4_a.set_yticks(y4_a)
    ax4_a.set_yticklabels([lbl for _, lbl in stg_meta], fontsize=8.8, fontweight="bold")
    ax4_a.set_xlim(0, 695)
    ax4_a.set_xlabel("Extracted claims; an absent link does not mean non-cryptographic", fontsize=8.8, fontweight="bold")
    ax4_a.set_title("(a) PQC Migration Stage by v3.5 Claim Join (4/530 [0.8%] READY in Stage 4-5)", fontsize=10.6, fontweight="bold", color="#1B365D", pad=10)
    ax4_a.grid(axis="x", linestyle="--", alpha=0.45)
    ax4_a.legend(loc="lower right", fontsize=7.8, frameon=True)

    # Panel (b): v3.5 Adjudicated RQ4 Dependency Categories (n=283 All / n=241 READY)
    ax4_b = axes4[0, 1]
    cat_summary = rq4_dep.groupby(["Adjudicated_Category_v35", "Claim_QA"]).size().unstack(fill_value=0)
    cat_summary["Total"] = cat_summary.sum(axis=1)
    cat_summary = cat_summary.sort_values("Total", ascending=True)
    y4_b = np.arange(len(cat_summary))
    h4_b = 0.36
    cat_names = [
        c.replace("3. Explicit ECC & Classical Signatures (Ed25519/ECDSA/RSA)", "3. Explicit ECC & Signatures (Ed25519/ECDSA)")
         .replace("10a-i. Unspecified Signed / Generic ZKP / HE (Suite NR)", "10a-i. Unspecified Signed / Generic ZK/HE (NR)")
         .replace("1. Cryptographic Hashes, Merkle Trees & Hash-STARKs", "1. Hashes, Merkle Trees & Hash-STARKs")
         .replace("10b. Excluded Non-Crypto Own Mechanism (8 E08-E09 + 2 Baselines)", "10b. Excluded Non-Crypto (8 Own + 2 Baselines)")
         .replace("10a-ii. Rejected False Crypto Label / Unspecified Context (7 REJECT_CLASS)", "10a-ii. Rejected False Crypto Label (7 REJECT)")
         .replace("10c. Held Pending Source Suite/Backend Verification (4 HOLD)", "10c. Held Pending Source Suite Locator (4 HOLD)")
        for c in cat_summary.index
    ]
    tot_b = cat_summary["Total"].values
    rdy_b = cat_summary["READY"].values
    ax4_b.barh(y4_b + h4_b/2, tot_b, height=h4_b, color="#3D5A80", label="All RQ4 Records (n = 283)")
    ax4_b.barh(y4_b - h4_b/2, rdy_b, height=h4_b, color="#159A6E", label="QA-Released READY Records (n = 241)")
    for i, (vt, vr) in enumerate(zip(tot_b, rdy_b)):
        ax4_b.text(vt + 0.6, y4_b[i] + h4_b/2, f"{vt} ({vt/283*100:.1f}%)", va="center", fontsize=8, fontweight="bold", color="#1F2937")
        ax4_b.text(vr + 0.6, y4_b[i] - h4_b/2, f"{vr} READY", va="center", fontsize=8, fontweight="bold", color="#159A6E")
    ax4_b.set_yticks(y4_b)
    ax4_b.set_yticklabels(cat_names, fontsize=8.2, fontweight="bold")
    ax4_b.set_xlim(0, 54)
    ax4_b.set_xlabel("Inventory: 266 active (222 concrete-class + 44 NR) + 17 excluded\n283 records; 0 HOLD", fontsize=8.5, fontweight="bold")
    ax4_b.set_title("(b) RQ4 Dependency Categories (283 Rec [248 Clm/245 Rep] | 241 READY [214 Clm/212 Rep])", fontsize=10.2, fontweight="bold", color="#1B365D", pad=10)
    ax4_b.grid(axis="x", linestyle="--", alpha=0.45)
    ax4_b.legend(loc="lower right", fontsize=8, frameon=True)

    # Panel (c): v3.5 Quantum Exposure Certainty Tiers computed from rq4_dep
    ax4_c = axes4[1, 0]
    exp_meta = [
        ("Tier A: Direct Mathematical Shor Exposure", "Tier A: Direct Mathematical Shor Exposure\n(ECC=42, ZKP=22, RSA/BLS=18)", 2),
        ("Grover / Symmetric / Lattice FHE / STARK", "Grover / Symmetric / Lattice FHE / STARK\n(Hashes/STARK=36, HMAC=24, FHE/AES=13)", 1),
        ("Unspecified Algorithm / Generic Scheme (Suite NR)", "Unspecified Algorithm / Generic Scheme (Suite NR)\n(40 initial + 4 finalized Suite=NR; n=44)", 1),
        ("Tier B: Conditional Protocol / Token Wrappers", "Tier B: Conditional Protocol / Token Wrappers\n(OAuth/JWT/DID/VC/mTLS; suite dependent)", 0),
        ("Tier C: Conditional Hardware Enclave Roots", "Tier C: Conditional Hardware Enclave Roots\n(SGX/TDX/SEV-SNP/Nitro/TPM attestation)", 1),
        ("Non-Cryptographic Baselines & Excluded Own Non-Crypto", "Non-Crypto Baselines & Excluded/Rejected\n(2 DEP-0005/0006 + 8 EXCLUDE + 7 REJECT)", 0),
        ("Evaluated or Proposed PQC / Quantum Constructions", "Evaluated or Proposed PQC / Quantum\n(ML-KEM, ML-DSA, XMSS, QRNG, hybrid proposals)", 10),
    ][::-1]
    y4_c = np.arange(len(exp_meta))
    exp_lbls, exp_all, exp_rdy, exp_src = [], [], [], []
    for ek, elbl, src_n in exp_meta:
        sub_e = rq4_dep[rq4_dep["Adjudicated_Exposure_Tier_v35"] == ek]
        exp_lbls.append(elbl)
        exp_all.append(len(sub_e))
        exp_rdy.append(int((sub_e["Claim_QA"] == "READY").sum()))
        exp_src.append(int(sub_e["Exposure_Provenance_Class"].eq("SOURCE_STATED_OR_EVALUATED").sum()))
    ax4_c.barh(y4_c + h4_b/2, exp_all, height=h4_b, color="#E63946", label=f"All inventory records (n={sum(exp_all)})")
    ax4_c.barh(y4_c - h4_b/2, exp_rdy, height=h4_b, color="#1D4ED8", label=f"READY inventory records (n={sum(exp_rdy)})")
    for i, (va, vr, vs) in enumerate(zip(exp_all, exp_rdy, exp_src)):
        ax4_c.text(va + 1.2, y4_c[i] + h4_b/2, f"All={va} ({va/283*100:.1f}%) [Src={vs}]", va="center", fontsize=8, fontweight="bold", color="#B91C1C")
        ax4_c.text(vr + 1.2, y4_c[i] - h4_b/2, f"READY={vr}", va="center", fontsize=8, fontweight="bold", color="#1D4ED8")
    ax4_c.set_yticks(y4_c)
    ax4_c.set_yticklabels(exp_lbls, fontsize=8.2, fontweight="bold")
    ax4_c.set_xlim(0, 128)
    ax4_c.set_ylim(-1.4, 6.6)
    ax4_c.set_xlabel("Inventory records (Src = source stated/evaluated: 15/283; 152 NE)\nDirect and conditional classes do not measure deployment failure rates", fontsize=8.5, fontweight="bold")
    ax4_c.set_title("(c) v3.5 Quantum Exposure Certainty Tiers (82 Direct Shor + 51 Conditional)", fontsize=10.6, fontweight="bold", color="#1B365D", pad=10)
    ax4_c.grid(axis="x", linestyle="--", alpha=0.45)
    ax4_c.legend(loc="lower right", fontsize=8, frameon=True)

    # Panel (d): Post-Quantum Wire Artifact Expansion
    ax4_d = axes4[1, 1]
    wire_items = [
        ("Ed25519 (Baseline)\n[RFC 8032]", 32, 64, "PK=32 B + Sig=64 B = 96 B (1.0x)"),
        ("X25519 (Baseline)\n[RFC 7748]", 32, 32, "Two public values: 32 B + 32 B = 64 B"),
        ("ML-KEM-768*\n[FIPS 203 / QSC]", 1184, 1088, "PK=1,184 B + CT=1,088 B = 2,272 B"),
        ("XMSS Root CA*\n[RFC 8391 / MAGIQ]", 64, 2500, "PK=64 B + Sig=2,500 B = 2,564 B (39.1x sig)"),
        ("ML-DSA-44\n[FIPS 204 Ref.]", 1312, 2420, "PK=1,312 B + Sig=2,420 B = 3,732 B (37.8x sig)"),
        ("ML-DSA-65*\n[FIPS 204 / QSC]", 1952, 3309, "PK=1,952 B + Sig=3,309 B = 5,261 B (51.7x sig)"),
        ("ML-DSA-87\n[FIPS 204 Ref.]", 2592, 4627, "PK=2,592 B + Sig=4,627 B = 7,219 B (72.3x sig)"),
        ("SLH-DSA-128s\n[FIPS 205 Ref.]", 32, 7856, "PK=32 B + Sig=7,856 B = 7,888 B (122.8x sig)"),
    ][::-1]
    y4_d = np.arange(len(wire_items))
    w_lbls = [d[0] for d in wire_items]
    w_pk = np.array([d[1] for d in wire_items])
    w_sig = np.array([d[2] for d in wire_items])
    w_txt = [d[3] for d in wire_items]
    ax4_d.barh(y4_d, w_pk, height=0.48, color="#0F766E", label="Public Key Size (Bytes)")
    ax4_d.barh(y4_d, w_sig, left=w_pk, height=0.48, color="#D97706", label="Second Wire Artifact (Bytes)")
    for i, (pk_v, sig_v, t_s) in enumerate(zip(w_pk, w_sig, w_txt)):
        ax4_d.text(pk_v + sig_v + 160, y4_d[i], t_s, va="center", fontsize=8.0, fontweight="bold", color="#1F2937")
    ax4_d.set_yticks(y4_d)
    ax4_d.set_yticklabels(w_lbls, fontsize=8.5, fontweight="bold")
    ax4_d.set_xlim(0, 16500)
    ax4_d.set_xlabel("Reference sizes (bytes); * = corpus-reported QSC/MAGIQ input\nExplicit plotting inputs; not computed from the five CSVs", fontsize=8.5, fontweight="bold")
    ax4_d.set_title("(d) Post-Quantum Wire Artifact Expansion (37.8x-72.3x for ML-DSA-44/65/87)", fontsize=10.6, fontweight="bold", color="#1B365D", pad=10)
    ax4_d.grid(axis="x", linestyle="--", alpha=0.45)
    ax4_d.legend(loc="upper right", fontsize=8.2, frameon=True)

    plt.tight_layout(rect=[0.01, 0.01, 0.99, 0.94])
    fig4.savefig(FIGS / "figure_4_rq4.png", dpi=300, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig4)


if __name__ == "__main__":
    main()
