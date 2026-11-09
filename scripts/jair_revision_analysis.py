"""R3 descriptive checks; reads the unchanged release 3.6.3 canonical CSVs.

Run from any directory with Python 3 and pandas. Outputs are post hoc
sensitivities, not new source adjudication or estimates for a common workload.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
c = pd.read_csv(DATA / 'claims.csv').fillna('')
w = pd.read_csv(DATA / 'rq3_latency_crosswalk.csv').fillna('')
mechanism = c.Claim_Category.isin(['DEFENSIVE_MECHANISM', 'FORMAL_FRAMEWORK', 'SYSTEM_PROTOTYPE'])
role_results = {}
for label, mask in [('mechanism', mechanism), ('attack_benchmark', ~mechanism)]:
    d = c.loc[mask].copy()
    d['supported'] = d.Claim_Support_Status.eq('SUPPORTED_WITHIN_SCOPE')
    report_rates = d.groupby('Source_Record_ID').supported.mean()
    role_results[label] = {'claims': len(d), 'reports': len(report_rates),
                          'supported_claims': int(d.supported.sum()),
                          'claim_support_percent': 100*d.supported.mean(),
                          'mean_within_report_support_percent': 100*report_rates.mean()}

discordant = ['R1-E03-MET-027', 'R1-E05-MET-063', 'R1-E05-MET-064']
eligible = w.loc[w.Pooling_Eligibility_v35.eq('ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS')
                 & w.Claim_QA.eq('READY')].copy()
eligible['value_ms'] = pd.to_numeric(eligible.Adjudicated_Latency_ms_v35)
latency = []
for level, d in eligible.groupby('Reclassified_Estimand_Level'):
    clean = d.loc[~d.Metric_ID.isin(discordant)]
    mean_point = d.loc[d.Dim4_Statistic_Type.eq('MEAN_OR_POINT_REPORTED')]
    latency.append({'level': level[:2], 'rows': len(d), 'reports': d.Source_Record_ID.nunique(),
                    'q1_ms': d.value_ms.quantile(.25), 'median_ms': d.value_ms.median(),
                    'q3_ms': d.value_ms.quantile(.75),
                    'report_median_ms': d.groupby('Source_Record_ID').value_ms.median().median(),
                    'mean_point_rows': len(mean_point), 'mean_point_median_ms': mean_point.value_ms.median(),
                    'excluding_discordant_rows': len(clean),
                    'excluding_discordant_median_ms': clean.value_ms.median()})

per_report = c.groupby('Source_Record_ID').size()
all_four = c.loc[c.Boundary_Codes.eq('B1;B2;B3;B4')]
report = {'revision': 'R3', 'date': '2026-11-04', 'analysis_status': 'post hoc descriptive',
          'canonical_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.glob('*.csv'))},
          'claims_per_report_distribution': {str(k): int(v) for k, v in per_report.value_counts().sort_index().items()},
          'role_support_weighting': role_results, 'latency': latency,
          'excluded_timer_sensitivity_ids': discordant,
          'all_four_boundaries': {'claims': len(all_four),
              'supported': int(all_four.Claim_Support_Status.eq('SUPPORTED_WITHIN_SCOPE').sum()),
              'UG': int(all_four.Limitation_Codes_DG_AD_UG_NG.str.split(';').map(lambda x: 'UG' in x).sum()),
              'supported_and_UG': int((all_four.Claim_Support_Status.eq('SUPPORTED_WITHIN_SCOPE') &
                      all_four.Limitation_Codes_DG_AD_UG_NG.str.split(';').map(lambda x: 'UG' in x)).sum())}}
(ROOT / 'results/jair_revision_analysis.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
pd.DataFrame(latency).to_csv(ROOT / 'results/jair_latency_sensitivity.csv', index=False)
print(json.dumps({k: v for k, v in report.items() if k != 'canonical_sha256'}, indent=2))
