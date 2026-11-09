"""Arithmetic audit of an author-supplied summary, NOT a raw-data replication.

Binary feasibility enumerates all 2x2 tables with the supplied N and agreement
count. Compatible marginals are not evidence that a particular table was used.
"""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'results/author_reported_stage3_agreement.csv').open(encoding='utf-8')))
out=[]
for r in rows:
    n=int(r['Report_Denominator']);agree=int(r['Exact_Agreements']);po=agree/n
    result={'dimension':r['Dimension'],'computed_Po_percent':100*po,
            'Po_rounding_matches':round(100*po,2)==float(r['Reported_Po_percent']),
            'raw_pair_replication':False}
    if int(r['Classes'])==2:
        feasible=0
        nearest=None
        kappa_matches=0
        ac1_matches=0
        for a in range(agree+1):
            for b in range(n-agree+1):
                c=n-agree-b;d=agree-a
                p1=(a+b)/n;p2=(a+c)/n;pbar=(p1+p2)/2
                pe=p1*p2+(1-p1)*(1-p2)
                pe1=2*pbar*(1-pbar)
                if pe==1:continue
                k=(po-pe)/(1-pe);ac1=(po-pe1)/(1-pe1)
                k_match=round(k,4)==float(r['Reported_Kappa'])
                a_match=round(ac1,4)==float(r['Reported_AC1'])
                kappa_matches+=int(k_match)
                ac1_matches+=int(a_match)
                distance=abs(k-float(r['Reported_Kappa']))+abs(ac1-float(r['Reported_AC1']))
                if nearest is None or distance<nearest['distance']:
                    nearest={'distance':distance,'kappa':k,'AC1':ac1}
                if k_match and a_match:
                    feasible+=1
        result['binary_2x2_tables_compatible_with_rounded_coefficients']=feasible
        result['tables_compatible_with_kappa_alone']=kappa_matches
        result['tables_compatible_with_AC1_alone']=ac1_matches
        result['nearest_feasible_coefficient_pair_not_a_correction']=nearest
    out.append(result)
(ROOT/'results/author_agreement_arithmetic_check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
