"""Recompute screening flow and agreement from normalized source-register exports."""
from pathlib import Path
from collections import Counter
from datetime import date
import hashlib,json,re
import pandas as pd

ROOT=Path(__file__).resolve().parent.parent
SCREEN=ROOT/'screening'

def read(name):return pd.read_csv(SCREEN/name,dtype=str,keep_default_na=False)

def agreement(left,right,binary=False):
    x=list(left);y=list(right)
    if binary:x=[v=='ADVANCE_FULLTEXT' for v in x];y=[v=='ADVANCE_FULLTEXT' for v in y]
    n=len(x);matches=sum(a==b for a,b in zip(x,y));cx=Counter(x);cy=Counter(y)
    pe=sum(cx[k]*cy[k] for k in set(cx)|set(cy))/(n*n)
    return {'n':n,'matching_decisions':matches,'disagreements':n-matches,
            'observed_agreement':matches/n,'kappa':(matches/n-pe)/(1-pe)}

def compute():
    s1=read('stage1_register.csv');s2=read('stage2_register.csv')
    reviews=read('stage2_fulltext_reviews.csv');rigor=read('stage2_rigor_reviews.csv')
    canonical=pd.read_csv(ROOT/'data/studies.csv',dtype=str,keep_default_na=False)
    assert len(s1)==s1.Source_Record_ID.nunique()==s1.Screening_ID.nunique()==926
    assert len(s2)==s2.Source_Record_ID.nunique()==610
    assert set(s1.loc[s1.FINAL_Decision.eq('ADVANCE_FULLTEXT'),'Source_Record_ID'])==set(s2.Source_Record_ID)
    included=s2[s2.Fulltext_Eligibility.eq('ELIGIBLE_INCLUDED')]
    assert set(included.Source_Record_ID)==set(canonical.Source_Record_ID)
    assert canonical.Source_PDF_SHA256.eq(canonical.Source_Record_ID.map(included.set_index('Source_Record_ID').Source_PDF_SHA256)).all()
    assert len(reviews)==1220 and reviews.groupby('Source_Record_ID').Reviewer_ID.nunique().eq(2).all()
    assert set(reviews.Source_Record_ID)==set(s2.Source_Record_ID)
    assert len(rigor)==694 and rigor.groupby('Source_Record_ID').Reviewer_ID.nunique().eq(2).all()
    flow=s1.FINAL_Decision.value_counts().to_dict()
    assert flow=={'ADVANCE_FULLTEXT':610,'EXCLUDE_STAGE1':236,'CONTEXT_ONLY':78,'LINK_REPORT_VERSION':2}
    outcome=s2.Fulltext_Eligibility.value_counts().to_dict()
    assert outcome=={'ELIGIBLE_INCLUDED':442,'EXCLUDED_FULLTEXT':166,'MERGED_STUDY_FAMILY':2}
    excluded=s2[s2.Fulltext_Eligibility.eq('EXCLUDED_FULLTEXT')]
    assert excluded.Exclusion_Code.ne('').all()
    five=agreement(s1.R1_Decision,s1.R2_Decision);binary=agreement(s1.R1_Decision,s1.R2_Decision,True)
    assert five['matching_decisions']==646 and abs(five['kappa']-.41721473236562084)<1e-12
    assert abs(binary['kappa']-.4446313651906011)<1e-12
    occurrences=read('arxiv_query_occurrences.csv');gate=read('arxiv_gate_pass_register.csv')
    assert len(occurrences)==4142 and occurrences.arxiv_id_base.nunique()==3894
    assert len(gate)==gate.arxiv_id_base.nunique()==529
    assert gate.cross_db_status.value_counts().to_dict()=={'NEW_ARXIV_PREPRINT':494,'SUPERSEDED_BY_PEER_REVIEWED':35}
    seed_refs={'2607.21325':3,'2504.21034':4,'2605.06933':5,'2605.03213':13}
    seed_rows=[]
    for key,ref in seed_refs.items():
        raw=occurrences[occurrences.arxiv_id_base.eq(key)]
        assert len(raw)>0 and not raw.query_source.eq('SEED_CHECK').any()
        seed_rows.append({'arxiv_id_base':key,'current_manuscript_reference':ref,
                          'query_sources':sorted(raw.query_source.unique()),'version':raw.arxiv_id_versioned.iloc[0]})
    dates=[]
    for _,r in s1.iterrows():
        value=r.R2_Decision_Date
        try:
            parsed=date.fromisoformat(value)
            state='PRE_SEARCH_DATE' if parsed<date(2026,10,15) else None
        except ValueError:state='INVALID_DATE_TEXT'
        if state:dates.append({'Source_Record_ID':r.Source_Record_ID,'Screening_ID':r.Screening_ID,'Field':'R2_Decision_Date','Recorded_Value':value,'Issue':state})
    assert not dates, 'Active screening dates still contain anomalies'
    corrections=pd.read_csv(ROOT/'protocol/screening_date_corrections.csv',dtype=str,keep_default_na=False)
    assert len(corrections)==corrections.Source_Record_ID.nunique()==104
    assert corrections.Corrected_Value.eq('2026-10-16').all()
    assert corrections.Correction_Basis.eq('USER_CONFIRMED_DATE').all()
    assert corrections.Original_Value.ne(corrections.Corrected_Value).all()
    assert corrections.Corrected_Value.eq(corrections.Source_Record_ID.map(s1.set_index('Source_Record_ID').R2_Decision_Date)).all()
    manifest=json.loads((ROOT/'protocol/search_sources/source_manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['normalized_exports']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    for entry in manifest['editorial_corrections']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    summary={'release':'3.6.3','stage1_records':len(s1),'stage1_final_decisions':flow,
             'stage1_five_class':five,'stage1_binary':binary,
             'stage1_tiers':s1.Evidence_Tier.value_counts().to_dict(),
             'stage2_records':len(s2),'stage2_tiers':s2.Evidence_Tier.value_counts().to_dict(),
             'stage2_retrieval':s2.Retrieval_Status.value_counts().to_dict(),
             'stage2_eligibility':outcome,'stage2_rigor_gate':s2.Preprint_Rigor_Gate_Status.value_counts().to_dict(),
             'fulltext_exclusions':excluded.Exclusion_Code.value_counts().to_dict(),
             'fulltext_review_rows':len(reviews),'fulltext_review_completion':reviews.Review_Completion.value_counts().to_dict(),
             'rigor_review_rows':len(rigor),'canonical_report_join':'442/442 source IDs and recorded hashes match',
             'historical_stage2_extraction_states':s2.Extraction_Status.value_counts().to_dict(),
             'arxiv_raw_occurrences':len(occurrences),'arxiv_unique_ids':occurrences.arxiv_id_base.nunique(),
             'arxiv_query_counts':occurrences.query_source.value_counts().to_dict(),
             'arxiv_gate_status':gate.cross_db_status.value_counts().to_dict(),
             'arxiv_seed_queries':seed_rows,'date_issues':dict(Counter(r['Issue'] for r in dates)),
             'confirmed_date_corrections':{'rows':104,'corrected_date':'2026-10-16','confirmed_on':'2026-11-03','ledger':'protocol/screening_date_corrections.csv'},
             'limits':'Agreement is computed from recorded labels and does not authenticate reviewer independence. The 104 date corrections follow explicit user confirmation; primary PDF contents are not replicated.'}
    return summary,dates

def generate(results=None):
    results=Path(results) if results else ROOT/'results';results.mkdir(exist_ok=True,parents=True)
    summary,dates=compute()
    (results/'screening_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    pd.DataFrame(dates,columns=['Source_Record_ID','Screening_ID','Field','Recorded_Value','Issue']).to_csv(results/'screening_date_issues.csv',index=False)
    five=summary['stage1_five_class'];binary=summary['stage1_binary']
    content=f'''# Screening and query-provenance audit

Release 3.6.3. Computed from normalized register exports in `screening/`. Original XLSX files were read without editing or recalculating their formulas. The normalized Stage 1 register incorporates 104 user-confirmed R2 date corrections, with original values retained separately. Final decisions use ADJUDIKASI; reviewer labels use IMPORT_R1/IMPORT_R2; Stage 2 uses DAFTAR_STUDI_STAGE2_610.

## Selection flow

Stage 1: 926 records = 610 ADVANCE_FULLTEXT + 236 EXCLUDE_STAGE1 + 78 CONTEXT_ONLY + 2 LINK_REPORT_VERSION. Tier split: 432 peer-reviewed / 494 preprint records.

Stage 2: all 610 advanced IDs match the Stage 2 register. Tier split: 263 / 347. Final eligibility: 442 included + 166 excluded + 2 merged. Rigor: 331 PASS, 14 FAIL, 2 merged/not assessed, plus 263 Tier 1 exempt from the additional preprint gate. The 442 included source IDs and recorded PDF hashes match studies.csv exactly. The 1,220 full-text review records contain two reviewer IDs for each of 610 reports; 694 rigor records cover two reviewer IDs for each of 347 preprints. Row presence and completed labels do not authenticate independent human review.

The Stage 2 workbook retains pilot extraction states (45 CLAIMS_EXTRACTED / 565 NOT_STARTED). Those historical extraction states are not the current Stage 3 completion denominator. Final Stage 3 reporting continues to use the five unchanged canonical CSVs. Two merged rows retain PENDING_REVIEW in Confirmed_Stream, but their eligibility is MERGED_STUDY_FAMILY, not an unresolved eligibility decision.

## Recomputed agreement

Five-class labels: {five['matching_decisions']}/{five['n']} match ({100*five['observed_agreement']:.4f}%); {five['disagreements']} differ; Cohen kappa = {five['kappa']:.10f}.

Binary ADVANCE_FULLTEXT versus all other labels: {binary['matching_decisions']}/{binary['n']} match; Cohen kappa = {binary['kappa']:.10f}. These are pre-adjudication label statistics, not post-adjudication consensus or claim-extraction reliability.

## Confirmed date corrections

The user confirmed 2026-10-16 as the correct date for all 104 previously flagged Reviewer 2 entries (100 pre-search dates and four non-date strings). The active R2_Decision_Date values are corrected to 2026-10-16. Original values, source IDs, and confirmation provenance are retained in protocol/screening_date_corrections.csv. The active date-issue export contains zero rows. All 926 final adjudication dates remain 2026-10-17. Decision labels and agreement are unchanged. User confirmation resolves the recorded date errors; it does not independently authenticate reviewer identities.

## arXiv query provenance

The compact raw-occurrence export contains 4,142 query returns / 3,894 base IDs. The 529 gate-passing IDs partition into 494 new preprints and 35 superseded versions. Four arXiv query strings match the archived pipeline constants. Raw occurrences resolve the seed-query assignments by stable arXiv ID; historical seed reference numbers are translated to the manuscript numbering. No live API rerun was performed.

The three supplied ACM strings are documented as author-supplied Boolean expressions. They do not contain the proximity operator mentioned in earlier narrative descriptions. Exact historical UI settings are not recovered from the supplied strings; original yield reproduction is not claimed.

## Source identity

Source-workbook and export SHA-256 values, selected sheet names, normalized export identities, and the archived arXiv pipeline identity are recorded in protocol/search_sources/source_manifest.json. The Stage 1 inventory CSV had 926 blank final-decision fields and was used only for bibliographic metadata. Final decisions were recovered from the administrator workbook instead. Formula QA caches were not freshly recalculated.
'''
    (results/'screening_audit.md').write_text(content,encoding='utf-8')
    return summary

if __name__=='__main__':
    summary=generate()
    print('PASS: screening flow and agreement reproduced; 104 user-confirmed R2 date corrections applied; 0 active date issues.')
