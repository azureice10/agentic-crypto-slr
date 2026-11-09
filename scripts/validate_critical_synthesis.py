"""Independent pandas verification of the Node CS1 aggregates and manuscript tables."""
from pathlib import Path
import hashlib
import json
import re
import pandas as pd

ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parent

def main():
    result=json.loads((ROOT/'results/critical_synthesis.json').read_text(encoding='utf-8'))
    frames={p.stem:pd.read_csv(p,keep_default_na=False) for p in (ROOT/'data').glob('*.csv')}
    for name,digest in result['source_sha256'].items():
        assert hashlib.sha256((ROOT/'data'/f'{name}.csv').read_bytes()).hexdigest()==digest
    c=frames['claims'].merge(frames['studies'][['Source_Record_ID','Confirmed_Stream','Evidence_Tier']],on='Source_Record_ID',validate='many_to_one')
    formal={'TOOL_SUPPORTED_VERIFICATION','SECURITY_REDUCTION','LOGICAL_AXIOMS_WITH_PROOF'}
    roles={'DEFENSIVE_MECHANISM','FORMAL_FRAMEWORK','SYSTEM_PROTOTYPE'}
    c['role']=c.Claim_Category.map(lambda v:'Mechanism/framework/prototype' if v in roles else 'Attack/benchmark/attack-surface')
    def pop(g):
        return dict(claims=len(g),reports=g.Source_Record_ID.nunique(),ready=int(g.Claim_QA.eq('READY').sum()),
                    supported=int(g.Claim_Support_Status.eq('SUPPORTED_WITHIN_SCOPE').sum()),
                    **{k:int(g.Limitation_Codes_DG_AD_UG_NG.str.split(';').map(lambda x:k in x).sum()) for k in ['DG','AD','UG']},
                    focused_formal=int(g.Formal_Evidence_Type.isin(formal).sum()),
                    broad_proof_including_theoretic=int(g.Formal_Evidence_Type.isin(formal|{'THEORETIC_PROOF'}).sum()),
                    deployment=int(g.Implementation_Maturity.isin(['DEPLOYMENT_LIKE_EVALUATION','PRODUCTION_DEPLOYED']).sum()),
                    stage45=int(g.PQC_Migration_Stage.str.match('STAGE_[45]_').sum()))
    assert result['corpus']==pop(c)
    for key,field in [('byRole','role'),('byStream','Confirmed_Stream')]:
        for category,g in c.groupby(field):
            assert result[key][category]['All']==pop(g)
            assert result[key][category]['READY']==pop(g[g.Claim_QA.eq('READY')])
    for (tier,role),g in c.groupby(['Evidence_Tier','role']):
        assert result['byTierRole'][f'{tier} / {role}']==pop(g)
    for key,field,label in [('supportQA','Claim_QA','qa'),('supportUG','Claim_Support_Status','support')]:
        for r in result[key]: assert {k:v for k,v in r.items() if k!=label}==pop(c[c[field].eq(r[label])])
    four=c[c.Boundary_Codes.str.split(';').map(len).eq(4)]
    assert result['composition']['four_boundaries']==pop(four)
    assert result['composition']['four_boundaries_ready']==pop(four[four.Claim_QA.eq('READY')])
    w=frames['rq3_latency_crosswalk'];w=w[w.Pooling_Eligibility_v35.eq('ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS')]
    for r in result['latency']:
        g=w[w.Reclassified_Estimand_Level.eq(r['level'])]
        if r['qa']=='READY':g=g[g.Claim_QA.eq('READY')]
        values=pd.to_numeric(g.Adjudicated_Latency_ms_v35)
        assert len(g)==r['n'] and g.Source_Record_ID.nunique()==r['reports']
        assert abs(values.median()-r['observation_median_ms'])<1e-9
        group_medians=g.assign(value=values).groupby('Source_Record_ID').value.median()
        assert abs(group_medians.median()-r['report_median_ms'])<1e-9
        sizes=g.Source_Record_ID.value_counts()
        assert int(sizes.max())==r['largest_report_n'] and int(sizes.head(3).sum())==r['top3_reports_n']
        point=g[g.Dim4_Statistic_Type.eq('MEAN_OR_POINT_REPORTED')]
        assert len(point)==r['mean_point_n']
        assert abs(pd.to_numeric(point.Adjudicated_Latency_ms_v35).median()-r['mean_point_median_ms'])<1e-9
        assert g.Dim4_Statistic_Type.value_counts().to_dict()==r['statistic']
        assert g.Dim1_Timer_Boundary.value_counts().to_dict()==r['timer']
        discrepant=g[g.Dim1_Timer_Boundary.ne(g.Reclassified_Estimand_Level)]
        expected_discrepancies=[dict(Metric_ID=x.Metric_ID,recorded_Dim1=x.Dim1_Timer_Boundary,final_level=x.Reclassified_Estimand_Level) for x in discrepant.itertuples()]
        assert r['timer_field_discrepancies']==expected_discrepancies
    d=frames['rq4_dependencies'];d=d[~d.Denominator_Status_v35.str.startswith('EXCLUDED_')]
    for qa in ['All','READY']:
        cc=c if qa=='All' else c[c.Claim_QA.eq('READY')]
        dd=d if qa=='All' else d[d.Claim_QA.eq('READY')]
        p=cc[cc.PQC_Migration_Stage.str.match('STAGE_[45]_')];r=result['pqc'][qa]
        assert (len(dd),dd.Claim_ID.nunique(),dd.Source_Record_ID.nunique())==(r['active_records'],r['active_claims'],r['active_reports'])
        assert r['stage45']==pop(p)
        assert r['stage45_direct_link']==pop(p[p.Claim_ID.isin(dd.Claim_ID)])
        assert r['stage45_in_crypto_reports']==pop(p[p.Source_Record_ID.isin(dd.Source_Record_ID)])
        assert r['lifetime_exact_missing']==int(dd.Protection_Lifetime_As_Reported.str.strip().isin(['NR','NOT_REPORTED','']).sum())
        for field,key in [('Protection_Lifetime_As_Reported','active_lifetime'),('Exposure_Provenance_Class','active_source_provenance'),('Adjudicated_Exposure_Tier_v35','active_exposure')]:
            assert dd[field].value_counts().to_dict()==r[key]
        ug=cc.Limitation_Codes_DG_AD_UG_NG.str.split(';').map(lambda a:'UG' in a)
        assert result['reportIndicators'][qa]==dict(reports=cc.Source_Record_ID.nunique(),any_UG=cc.loc[ug,'Source_Record_ID'].nunique(),any_focused_formal=cc.loc[cc.Formal_Evidence_Type.isin(formal),'Source_Record_ID'].nunique())
    manuscript=REPO/'manuscript_slr.md'
    checks={'input_hashes':'5/5 match','independent_aggregations':'Pandas agrees with Node for roles, streams, tiers, QA, formal definitions, four-boundary subset, latency and PQC joins'}
    if manuscript.exists():
        text=manuscript.read_text(encoding='utf-8')
        for role,qa,prefix in [('Mechanism/framework/prototype','All','Mechanism/framework/prototype, All'),('Mechanism/framework/prototype','READY','Mechanism/framework/prototype, READY'),('Attack/benchmark/attack-surface','All','Attack/benchmark/attack-surface, All'),('Attack/benchmark/attack-surface','READY','Attack/benchmark/attack-surface, READY')]:
            r=result['byRole'][role][qa]
            cells=[prefix,str(r['claims']),str(r['reports'])]+[f"{r[k]} ({100*r[k]/r['claims']:.1f}%)" for k in ['supported','DG','UG','focused_formal','broad_proof_including_theoretic']]
            assert '| '+' | '.join(cells)+' |' in text
        for tier,caption in [('TIER_1_PEER_REVIEWED','Tier 1'),('TIER_2_ARXIV_PREPRINT','Tier 2')]:
            r=result['byTierRole'][f'{tier} / Mechanism/framework/prototype']
            cells=[caption,str(r['claims'])]+[f"{r[k]} ({100*r[k]/r['claims']:.1f}%)" for k in ['supported','DG','UG','focused_formal']]
            assert '| '+' | '.join(cells)+' |' in text
        tables=re.findall(r'(?m)^\| L[1-4] \|.*$',text)
        assert len(tables)==4
        for line in tables:
            cells=[x.strip() for x in line.strip('|').split('|')]
            r=next(r for r in result['latency'] if r['level'].startswith(cells[0]+':') and r['qa']=='READY')
            assert [float(x.replace(',','')) for x in cells[1:]]==[r['n'],r['observation_median_ms'],r['mean_point_n'],r['mean_point_median_ms']]
        expected=None
        for n,line in enumerate(text.splitlines(),1):
            if line.startswith('|'):
                count=len(re.split(r'(?<!\\)\|',line))-2
                if expected is None:expected=count
                assert count==expected,f'Malformed Markdown table at line {n}'
            else:expected=None
        assert text.count('```')%2==0
        for mermaid in re.findall(r'```mermaid\n(.*?)```',text,re.S):
            assert r'\--\>' not in mermaid and r'\<br' not in mermaid
        for target in re.findall(r'!?\[[^\n\]]*\]\(([^\s)]+)\)',text):
            if not target.startswith(('http:','https:','#')):assert (REPO/target).exists(),target
        assert 'MS-S1S5-v3.6.3-CS1-critical-synthesis' in text
        checks['manuscript']='Tables 3.10b, 3.15 and 3.16 match computations; Markdown table widths, fences, Mermaid escapes and local links checked'
        out=REPO/'audit_output/critical_synthesis_verification.json'
        out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print('PASS: '+ '; '.join(checks.values()))

if __name__=='__main__':main()
