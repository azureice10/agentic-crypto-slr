"""Independent nominal-agreement calculations from supplied pre-adjudication CSVs.

No worksheet is modified. Output pairs, contingency cells and input hashes make
the chosen first-row and order-paired comparisons inspectable. Agreement does
not establish semantic claim equivalence or human sign-off of draft rows.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv,hashlib,json,importlib.util,math
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'stage3_irr'
OUT=ROOT/'results'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def stats(pairs):
    n=len(pairs);c1=Counter(a for a,b in pairs);c2=Counter(b for a,b in pairs)
    cats=sorted(c1.keys()|c2.keys());a=sum(x==y for x,y in pairs);po=a/n
    pe=sum(c1[c]*c2[c] for c in cats)/n**2
    k=(po-pe)/(1-pe) if pe<1 else None
    pbar=[(c1[c]+c2[c])/(2*n) for c in cats]
    pe_ac=sum(p*(1-p) for p in pbar)/(len(cats)-1) if len(cats)>1 else None
    ac=(po-pe_ac)/(1-pe_ac) if pe_ac is not None else None
    return dict(N=n,Agree=a,Po_percent=100*po,Kappa=k,AC1=ac,Categories=len(cats)),c1,c2,Counter(pairs)
def features(r):
    lim=set(r['Limitation_Codes_DG_AD_UG_NG'].strip().split(';'))
    d={k:r[k].strip() for k in ['Target_Boundary','Claim_Support_Status','Claim_Category','Lifecycle_Stage','Formal_Evidence_Type','Implementation_Maturity','PQC_Migration_Stage','Source_PDF_SHA256']}
    assert all(d.values())
    d['Boundary_Multi_Single']='MULTI' if d['Target_Boundary']=='MULTI_BOUNDARY' else 'SINGLE'
    d['Boundary_Set']=';'.join(sorted(x.strip() for x in r['Boundary_Codes'].split(';') if x.strip()))
    assert d['Boundary_Set']
    d['Support_Binary']='SUPPORTED' if d['Claim_Support_Status']=='SUPPORTED_WITHIN_SCOPE' else 'OTHER_RECORDED_CODE'
    d['PQC_Grouped']='PRE_OR_ND' if d['PQC_Migration_Stage'] in ['NOT_DISCUSSED','STAGE_0_PRE_QUANTUM_ONLY'] else 'STAGE_1_TO_5'
    d['Focused_Formal']='YES' if d['Formal_Evidence_Type'] in ['TOOL_SUPPORTED_VERIFICATION','SECURITY_REDUCTION','LOGICAL_AXIOMS_WITH_PROOF'] else 'NO'
    for code in ['AD','DG','UG']:d[code]='YES' if code in lim else 'NO'
    return d
groups=[];input_hashes={};metadata=[];batch_for={};batch_counts=[]
for reviewer,folder in [(1,'raw_reviewer_1_herman_kabetta'),(2,'raw_reviewer_2_i_komang_setia_buana')]:
    g=defaultdict(list)
    for p in sorted((PKG/folder).glob('LEMBAR*.csv')):
        rows=read(p);batch=p.name.split('BATCH_')[1][:3]
        input_hashes[str(p.relative_to(PKG))]=hashlib.sha256(p.read_bytes()).hexdigest()
        batch_counts.append({'Reviewer':reviewer,'Batch':batch,'Rows':len(rows),'Reports':len({r['Source_Record_ID'] for r in rows})})
        for i,r in enumerate(rows,2):
            sid=r['Source_Record_ID'].strip();r['_file']=str(p.relative_to(PKG));r['_csv_line']=i
            g[sid].append(r);batch_for[sid]=batch
    groups.append(g)
    flat=[r for rows in g.values() for r in rows]
    metadata.append({'reviewer':reviewer,'rows':len(flat),'reports':len(g),
                     'extractor_labels':dict(Counter(r['Extractor_Reviewer'] for r in flat)),
                     'verification_labels':dict(Counter(r['Verification_Status'] for r in flat)),
                     'AI_draft_rationale_rows':sum('Draft AI' in r['Coding_Rationale'] for r in flat),
                     'human_identity_not_assigned_rationale_rows':sum('Identity reviewer manusia belum ditetapkan' in r['Coding_Rationale'] for r in flat),
                     'maturity_categories':dict(Counter(r['Implementation_Maturity'] for r in flat))})
g1,g2=groups
canonical=read(ROOT/'data/studies.csv')
canonical_ids={r['Source_Record_ID'] for r in canonical}
assert set(g1)==set(g2)==canonical_ids and len(g1)==442
assert [sum(map(len,g.values())) for g in groups]==[533,508]
assert all(len({r['Source_PDF_SHA256'] for r in g1[s]+g2[s]})==1 for s in g1)
methods={
    'Primary442':[(s,g1[s][0],g2[s][0]) for s in sorted(g1)],
    'Single319':[(s,g1[s][0],g2[s][0]) for s in sorted(g1) if len(g1[s])==len(g2[s])==1],
    'Order474':[(s,a,b) for s in sorted(g1) for a,b in zip(g1[s],g2[s])]
}
summary=[];cells=[];pair_rows=[]
for method,triples in methods.items():
    for s,a,b in triples:
        pair_rows.append({'Method':method,'Source_Record_ID':s,'R1_Claim_ID':a['Claim_ID'],'R2_Claim_ID':b['Claim_ID'],
                         'R1_File':a['_file'],'R1_CSV_Line':a['_csv_line'],'R2_File':b['_file'],'R2_CSV_Line':b['_csv_line']})
    for dim in features(triples[0][1]):
        pairs=[(features(a)[dim],features(b)[dim]) for _,a,b in triples]
        st,c1,c2,table=stats(pairs);summary.append({'Method':method,'Dimension':dim,**st})
        for (a,b),n in sorted(table.items()):cells.append({'Method':method,'Dimension':dim,'R1':a,'R2':b,'Count':n})
mult,c1,c2,cells_mult=stats([(str(len(g1[s])),str(len(g2[s]))) for s in sorted(g1)])
complete_cases=[]
for dim,missing in [('Claim_Support_Status',{'NOT_EVALUATED','NE','NR',''}),('Implementation_Maturity',{'NE','NR','NOT_EVALUATED',''})]:
    pairs=[(a[dim].strip(),b[dim].strip()) for _,a,b in methods['Primary442'] if a[dim].strip() not in missing and b[dim].strip() not in missing]
    st,_,_,_=stats(pairs);complete_cases.append({'Dimension':dim,**st})
write_csv(OUT/'stage3_irr_complete_case_sensitivity.csv',complete_cases)
write_csv(OUT/'stage3_irr_reproduced.csv',summary)
write_csv(OUT/'stage3_irr_contingency.csv',cells)
write_csv(OUT/'stage3_irr_pairs.csv',pair_rows)
write_csv(OUT/'stage3_irr_batch_counts.csv',batch_counts)

# Execute supplied author script only after inspection, redirecting its output.
spec=importlib.util.spec_from_file_location('author_irr',PKG/'scripts/compute_stage3_irr_agreement.py')
author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
author.RES_DIR=str(OUT/'stage3_author_script_reproduction');author.main()
provided=read(PKG/'results/stage3_irr_by_method.csv')
rerun=read(Path(author.RES_DIR)/'stage3_irr_by_method.csv')
assert provided==rerun,'Supplied author table does not equal rerun'
mapping={'Target_Boundary':'Target_Boundary_5Class','Boundary_Multi_Single':'Target_Boundary_Binary',
         'Boundary_Set':'Boundary_Set_Exact','PQC_Grouped':'PQC_Migration_Stage_Collapsed',
         'PQC_Migration_Stage':'PQC_Migration_Stage_Exact','Focused_Formal':'Strict_Formal_Proof_Binary',
         'AD':'Limitation_AD_Binary','DG':'Limitation_DG_Binary','UG':'Limitation_UG_Binary'}
matches=0
for row in summary:
    if row['Dimension']=='Support_Binary':continue
    target=next(r for r in rerun if r['Dimension']==mapping.get(row['Dimension'],row['Dimension']))
    pre={'Primary442':'Rule1','Single319':'Rule3A','Order474':'Rule3B'}[row['Method']]
    for k in ['Kappa','AC1']:
        if row[k] is not None:assert f'{row[k]:.4f}'==target[f'{pre}_{k}'],(row,target)
    matches+=1
rank_missing={}
for label,key,rank in [('maturity','Implementation_Maturity',author.IM_RANK),('formal','Formal_Evidence_Type',author.FE_RANK),('pqc','PQC_Migration_Stage',author.PQC_RANK)]:
    vals=Counter(r[key] for g in groups for rows in g.values() for r in rows)
    rank_missing[label]={k:n for k,n in vals.items() if k not in rank}
out={'input_sha256':input_hashes,'reviewer_metadata':metadata,'canonical_ID_sets_match':True,'all_report_hashes_match_between_reviewers':True,
 'claim_count_agreement':mult,'multiplicity_cells':[{'R1_count':a,'R2_count':b,'Reports':n} for (a,b),n in sorted(cells_mult.items())],
 'paired_claims':474,'unmatched_R1':59,'unmatched_R2':34,'author_script_summary_reproduced':True,
 'independent_method_dimension_matches':matches,'author_aggregation_rank_unmapped_values':rank_missing,
 'limits':['first-row and ordinal pairing do not independently establish semantic claim equivalence',
           'similarity matching optimizes some evaluated attributes and cannot independently validate their reliability',
           'author confirms Herman checked and approved supplied R1 worksheets before adjudication; legacy metadata remain and approval notes are being located',
           'single-claim subset excludes all reports with different or multiple selections; no generalization without qualification',
           'original author script does not regenerate supplied per-batch and alignment result files']}
(OUT/'stage3_irr_reproduction_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
