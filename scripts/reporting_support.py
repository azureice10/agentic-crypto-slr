"""Derived reporting views of the canonical CSVs; never modifies data/*.csv."""
from pathlib import Path
import csv
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
RELEASE = '3.6.3'


def load_tables():
    return {p.stem: pd.read_csv(p) for p in sorted(DATA.glob('*.csv'))}


def unit_groups(metrics):
    """NR takes precedence over Unit; unit text is preserved in canonical data."""
    def group(row):
        if row['Data_Status'] == 'NOT_REPORTED':
            return 'NOT_REPORTED (NR)'
        unit = row['Unit']
        return {'percent':'percent (%)','ms':'ms (milliseconds)', 's':'s (seconds)',
                'tokens':'tokens','fraction':'fraction (0-1)',
                'KB':'KB / bytes','bytes':'KB / bytes',
                'ops/s':'ops/s / TPS / s/token','TPS':'ops/s / TPS / s/token',
                's/token':'ops/s / TPS / s/token','USD':'USD / gas','gas':'USD / gas'}[unit]
    return metrics.apply(group, axis=1)


def qa_zones(claims, studies):
    """Only the four groups recoverable from distributed record-level fields."""
    years=claims.Source_Record_ID.map(studies.set_index('Source_Record_ID').Year)
    green=(years == 2027) & (claims.Claim_QA == 'READY') & (claims.Claim_Support_Status == 'SUPPORTED_WITHIN_SCOPE')
    partial=(claims.Claim_QA == 'READY') & (claims.Claim_Support_Status == 'PARTIALLY_SUPPORTED')
    conditional=claims.Adjudication_ID_v35.fillna('').str.contains('HUM-P3-')
    red=claims.QA_Adjudication_Disposition.eq('RETAINED_FLAGGED_RED_ZONE')
    assert int(green.sum()+partial.sum()+conditional.sum()+red.sum()) == 107
    return [
        ('P1: Online-First Eligibility Recorded\n[READY]', int(green.sum()), '#159A6E'),
        ('P2: Partially Supported, Scope Fenced\n[READY]', int(partial.sum()), '#159A6E'),
        ('P3: Conditional Scope / Metric Limits\n[FLAGGED]', int(conditional.sum()), '#D97706'),
        ('R1-R4: Red-Zone Claims\n[FLAGGED; subgroup history in manuscript]', int(red.sum()), '#C0392B'),
    ]


def adjudication_register(tables):
    rows=[]
    configs=[('claims','Claim_ID','QA_Adjudication_Disposition','Assessed_Claim_Scope','Evidence_Quote_and_Page'),
             ('rq3_metrics','Metric_ID','Adjudicated_Action_v35','Adjudicated_Rationale_v35','Evidence_Location'),
             ('rq4_dependencies','Dependency_ID','Adjudicated_Action_v35','Adjudicated_Reason_v35','Evidence_Location')]
    for table,key,action,rationale,locator in configs:
        for _,r in tables[table].fillna('').iterrows():
            for decision in str(r['Adjudication_ID_v35']).split(';'):
                decision=decision.strip()
                if not decision:
                    continue
                rows.append({'Adjudication_ID':decision,'Table':table+'.csv','Record_ID':r[key],
                             'Claim_ID':r['Claim_ID'],'Source_Record_ID':r['Source_Record_ID'],
                             'Claim_QA':r['Claim_QA'],'Recorded_Action':r[action],
                             'Recorded_Rationale':r[rationale],'Evidence_Locator':r[locator],
                             'Source_PDF_SHA256':r['Source_PDF_SHA256'],
                             'Recorded_Sign_Off':r['Human_Sign_Off_v35']})
    result=pd.DataFrame(rows).sort_values('Adjudication_ID')
    assert len(result)==220 and result.Adjudication_ID.nunique()==220
    return result


def latency_statistics(crosswalk):
    eligible=crosswalk[crosswalk.Pooling_Eligibility_v35.eq('ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS')]
    rows=[]
    for axis in ['Reclassified_Estimand_Level','Reclassified_Mechanism_Family']:
        for group,all_rows in eligible.groupby(axis):
            for stratum,sub in [('All',all_rows),('READY',all_rows[all_rows.Claim_QA.eq('READY')])]:
                q=sub.Adjudicated_Latency_ms_v35.quantile([.25,.5,.75])
                rows.append({'Axis':axis,'Stratum':group,'Claim_QA_Stratum':stratum,
                             'Observations':len(sub),'Claims':sub.Claim_ID.nunique(),
                             'Reports':sub.Source_Record_ID.nunique(),'p25_ms':q.loc[.25],
                             'p50_ms':q.loc[.5],'p75_ms':q.loc[.75],'IQR_ms':q.loc[.75]-q.loc[.25],
                             'Report_Clustered_p50_ms':sub.groupby('Source_Record_ID').Adjudicated_Latency_ms_v35.median().median()})
    return pd.DataFrame(rows)


def category_statistics(dependencies):
    rows=[]
    for category,group in dependencies.groupby('Adjudicated_Category_v35'):
        for stratum,sub in [('All',group),('READY',group[group.Claim_QA.eq('READY')])]:
            rows.append({'Category':category,'Claim_QA_Stratum':stratum,'Records':len(sub),
                         'Claims':sub.Claim_ID.nunique(),'Reports':sub.Source_Record_ID.nunique(),
                         'Exposure_Tier':group.Adjudicated_Exposure_Tier_v35.iloc[0]})
    return pd.DataFrame(rows)


def sensitivity_statistics(claims,studies,dependencies):
    claims=claims.merge(studies[['Source_Record_ID','Evidence_Tier']],on='Source_Record_ID',validate='many_to_one')
    rows=[]
    strict=['TOOL_SUPPORTED_VERIFICATION','SECURITY_REDUCTION','LOGICAL_AXIOMS_WITH_PROOF']
    for tier,group in [('Tier 1',claims[claims.Evidence_Tier.eq('TIER_1_PEER_REVIEWED')]),
                       ('Tier 2',claims[claims.Evidence_Tier.eq('TIER_2_ARXIV_PREPRINT')]),('Combined',claims)]:
        metrics={'MULTI_BOUNDARY':group.Target_Boundary.eq('MULTI_BOUNDARY'),
                 'SUPPORTED_WITHIN_SCOPE':group.Claim_Support_Status.eq('SUPPORTED_WITHIN_SCOPE'),
                 'READY':group.Claim_QA.eq('READY'),'Strict_Formal':group.Formal_Evidence_Type.isin(strict),
                 'AD':group.Limitation_Codes_DG_AD_UG_NG.str.split(';').apply(lambda x:'AD' in x),
                 'Benchmark_PoC_Deployment':group.Implementation_Maturity.isin(['CONTROLLED_BENCHMARK','PROOF_OF_CONCEPT','DEPLOYMENT_LIKE_EVALUATION','PRODUCTION_DEPLOYED']),
                 'No_Demonstrated_PQC_Migration':group.PQC_Migration_Stage.isin(['NOT_DISCUSSED','STAGE_0_PRE_QUANTUM_ONLY'])}
        for b in ['B1','B2','B3','B4']:
            metrics[b]=group.Boundary_Codes.str.split(';').apply(lambda x:b in x)
        for indicator,mask in metrics.items():
            rows.append({'Tier':tier,'Indicator':indicator,'Unit':'claims','Numerator':int(mask.sum()),'Denominator':len(group),'Percent':100*mask.mean()})
        reports=set(group.Source_Record_ID)
        inv=set(dependencies.Source_Record_ID)&reports
        active=set(dependencies.loc[~dependencies.Denominator_Status_v35.str.startswith('EXCLUDED_'),'Source_Record_ID'])&reports
        for indicator,n in [('Reports_with_RQ4_Inventory',len(inv)),('Reports_with_Active_Crypto_Dependency',len(active))]:
            rows.append({'Tier':tier,'Indicator':indicator,'Unit':'reports','Numerator':n,'Denominator':len(reports),'Percent':100*n/len(reports)})
    return pd.DataFrame(rows)


def md_table(frame):
    def cell(v):
        if pd.isna(v): return ''
        if isinstance(v,float): return f'{v:.6g}'
        return str(v).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(frame.columns)+' |\n| '+' | '.join(['---']*len(frame.columns))+' |\n'+ '\n'.join('| '+' | '.join(cell(v) for v in row)+' |' for row in frame.itertuples(index=False,name=None))


def generate_reporting(results):
    results=Path(results); results.mkdir(parents=True,exist_ok=True)
    tables=load_tables(); c=tables['claims'];s=tables['studies'];m=tables['rq3_metrics'];w=tables['rq3_latency_crosswalk'];d=tables['rq4_dependencies']
    register=adjudication_register(tables);latency=latency_statistics(w);cats=category_statistics(d);sens=sensitivity_statistics(c,s,d)
    for name,frame in [('adjudication_register',register),('latency_statistics',latency),('rq4_category_statistics',cats),('tier_sensitivity',sens)]:
        frame.to_csv(results/(name+'.csv'),index=False)
    sections=['# Computed manuscript reporting tables',
              f'Release {RELEASE}; generated from the unchanged v3.5 canonical CSV baseline. No primary-PDF or screening-register verification is performed.',
              '## Table 3.10 numerical view: eligible latency strata',md_table(latency),
              '## Table 3.12 numerical view: RQ4 construction categories',md_table(cats),
              '## Table 3.14 numerical view: tier sensitivity indicators',md_table(sens)]
    (results/'manuscript_tables.md').write_text('\n\n'.join(sections)+'\n',encoding='utf-8')
    pool=w.groupby(['Pooling_Eligibility_v35','Claim_QA']).size().unstack(fill_value=0).reset_index()
    pool['All']=pool.READY+pool.FLAGGED
    pool=pool[['Pooling_Eligibility_v35','All','READY','FLAGGED']]
    totals=pd.DataFrame([{'Table':name+'.csv','Rows':len(frame),'Columns':len(frame.columns)} for name,frame in tables.items()])
    states=m.Audit_Verification_State.value_counts().rename_axis('State').reset_index(name='Rows')
    med=latency[latency.Claim_QA_Stratum.eq('READY')][['Stratum','Observations','Reports','p50_ms','Report_Clustered_p50_ms']]
    audit=['# Reconciled audit summary',f'**Release:** {RELEASE} (3 November 2026). **Analytical baseline:** v3.5; recorded CSV sign-off 2 November 2026. Generated by `scripts/reporting_support.py`.',
           '## Scope and provenance limits','This report summarizes the five canonical Stage 3 CSVs. Normalized Stage 1/2 registers and reviewer rows are now supplied in screening/; screening flow and agreement are recomputed in results/screening_audit.md. Human-review identities, primary PDF contents, and the complete four-platform raw search yield are not independently authenticated. A recorded APPROVED_FINAL string is preserved data, not a new sign-off for this editorial revision.',
           '## Canonical tables',md_table(totals),
           f'Claims: {len(c)} = {int(c.Claim_QA.eq("READY").sum())} READY + {int(c.Claim_QA.eq("FLAGGED").sum())} FLAGGED. Reports with at least one READY claim: {c.loc[c.Claim_QA.eq("READY"),"Source_Record_ID"].nunique()}.',
           f'RQ3: {len(m)} rows = {int(m.Numeric_Value.notna().sum())} numeric + {int(m.Data_Status.eq("NOT_REPORTED").sum())} NR; {int(m.Claim_QA.eq("READY").sum())} attached to READY claims, including 12 NR rows. NR rows are not numeric latency observations.',
           '## Complete final time-row partition',md_table(pool),
           'All 454 time rows are classified: 399 eligible + 26 sibling duplicates + 3 quarantined source conflicts + 26 other strata; no active HOLD disposition.',
           'Human comparison baselines: R1-E02-MET-137 = 2,700 s and R1-E02-MET-138 = 4,200 s (REC-016/017). Synthetic-zero exclusions: REC-044/052. Bound/model strata: MemLineage REC-045 (<1 ms) and SAGA REC-049 (220 ms model). PILOT-MET-007 is a duplicate of R1-E05-MET-006. NiyamAI quarantined rows belong to CLM-0003.',
           '## READY latency medians',md_table(med),
           'Examples retained in the adjudicated data: Poseidon CLM-0069, REC-042/043, 91.25/79.50 ms; AegisMCP CLM-0493, REC-053, GraphSAGE inference 0.69 ms. These examples do not replace the stratified workload definitions.',
           '## RQ4 inventory and construction categories','283 inventory records (248 claims / 245 reports) = 266 active dependencies (231 claims / 228 reports; 224 READY) + 17 excluded non-cryptographic records (17 claims / 17 reports; all READY). Active = 222 concrete algorithm/protocol/enclave-class records + 44 Suite NR records. An absent claim-to-dependency link is not evidence of a non-cryptographic mechanism.',
           md_table(cats),
           'Stage 4-5: 7 claims across 4 reports; 4 READY claims across 2 reports. QSC CLM-0392/0394 are supported/READY; CLM-0393 is partially supported/FLAGGED.',
           '## Adjudication: decisions versus affected rows','220 unique decisions = 86 RQ3 (25 BUG + 61 REC) + 123 RQ4 + 11 P3. The 86 RQ3 decisions affect 77 metric rows: 76 time rows with 85 decisions and one USD row (R12-E07-MET-081 / HUM-RQ3-BUG-025). Some rows have multiple decisions. The crosswalk mirrors time decisions and is not counted a second time.',
           'The complete flattened decision-to-record register is `results/adjudication_register.csv`, derived from the original ID, action/disposition, rationale, locator, hash, and recorded sign-off columns. The internal 21-non-time-row description and REC-062..072 range are not part of this baseline.',
           'RQ3 audit-state counts:',md_table(states),
           '## Reproducibility boundaries','`summary_tables.csv`, the three numerical reporting views, and the figures use canonical CSV aggregations. Figure 4d retains explicitly labeled reference-size constants in plotting code. Screening decisions, full-text exclusions, review rows, and arXiv occurrence/gate-pass provenance are supplied as normalized exports. Original XLSX files, primary PDFs, historical crosswalks, and the internal 107-candidate matrix are not distributed. Four arXiv expressions match the archived pipeline; ACM expressions are author-supplied with original UI settings unverified. NOT_DISCUSSED and Stage 0 are preserved historical codes and combined analytically as no demonstrated PQC migration.']
    (results/'audit_summary.md').write_text('\n\n'.join(audit)+'\n',encoding='utf-8')
    if (ROOT/'screening/stage1_register.csv').exists():
        from screening_support import generate
        generate(results)


COMMON = {
 'Claim_ID':'Unique claim identifier; primary key in claims.csv and foreign key elsewhere.',
 'Source_Record_ID':'Canonical included-report identifier; foreign key to studies.csv.',
 'Study_Family_ID':'Canonical report cluster, SF-<Source_Record_ID>; not independent validation of a study family.',
 'Study_Title':'Title of the parent canonical report.', 'Title':'Bibliographic title of the included report.',
 'Evidence_Tier':'Recorded peer-reviewed or arXiv-preprint tier.',
 'Claim_QA':'Claim-level release stratum READY or FLAGGED; inherited by linked observations, not a metric-level eligibility decision.',
 'Claim_Support_Status':'Support for the assessed claim scope: SUPPORTED_WITHIN_SCOPE, PARTIALLY_SUPPORTED, or NOT_SUPPORTED; independent of release status.',
 'Source_PDF_SHA256':'Recorded SHA-256 identity of the assessed primary PDF; the PDF is not distributed or rehashed by these scripts.',
 'Source_Version_ID':'Recorded source filename or pinned bibliographic/preprint version.',
 'Verification_Status':'Recorded verification workflow state; does not authenticate independent human review.',
 'Adjudication_ID_v35':'Semicolon-delimited adjudication decision IDs; one row may receive multiple decisions. Blank means no v3.5 decision ID recorded.',
 'Human_Sign_Off_v35':'Recorded 2 November 2026 sign-off and review/decision references; preserved provenance, not a new editorial approval.',
 'Audit_Verification_State':'Recorded final workflow state; use observed CSV values and counts rather than infer Claim_QA from this field name.',
 'Public_Adjudication_Status':'Public text of final disposition or unchanged Stage 3 verification.',
 'Reviewer1_Decision_v35':'Recorded reviewer decision; semicolon-delimited when multiple decisions affect the row.',
 'Adjudicated_Action_v35':'Recorded enacted action(s); may combine multiple decisions on one row.',
 'Evidence_Location':'Recorded primary-source page/table/figure locator.',
 'PQC_Migration_Stage':'Original migration evidence label. Analyze NOT_DISCUSSED and STAGE_0 jointly because batch coding differed; do not infer quantum safety from either label.',
 'Implementation_Maturity':'Recorded implementation/evaluation category, distinct from formal evidence and release QA.',
 'Metric_ID':'Unique metric-row identifier; crosswalk foreign key to rq3_metrics.csv.',
 'Metric_Name':'Name of the metric/configuration/statistic as extracted.',
 'Target_Configuration':'System/algorithm/configuration measured by the observation.',
 'Workload':'Recorded unit of work or benchmark context; free text, not a normalized batch-size enum.',
 'Hardware_Runtime':'Hardware/software/runtime context as reported; NR records absent reporting.',
 'Data_Status':'Observation reporting/resolution state; NOT_REPORTED identifies nonnumeric omission rows regardless of Unit.',
 'Unit':'Source-unit label. For disjoint reporting, first map Data_Status=NOT_REPORTED to NR, then group remaining Unit values. Raw fraction has 98 rows; two are NR, leaving 96 numeric fractions.',
 'Numeric_Value':'Extracted numeric value; blank for NR. For adjudicated analysis prefer nonblank Adjudicated_Numeric_Value_v35.',
 'Adjudicated_Numeric_Value_v35':'Final numeric value in Adjudicated_Unit_v35. Blank for excluded synthetic-zero/non-time rows is not a zero latency.',
 'Adjudicated_Unit_v35':'Unit of final adjudicated value; do not pool unlike units.',
 'Canonical_Observation_ID':'Recorded source-observation identity used to identify sibling-claim repetitions; blank is not evidence of uniqueness.',
 'Canonical_Observation_ID_v35':'Final source-observation identity, mirrored as Canonical_Observation_ID in metrics.',
 'Adjudicated_Latency_ms_v35':'Final normalized milliseconds. Primary latency synthesis additionally requires Pooling_Eligibility_v35=ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS. Never impute missing values as zero.',
 'Pooling_Eligibility_v35':'Final latency disposition. READY is claim QA and does not override duplicate, quarantine, bound, batch, or other exclusion/stratification decisions.',
 'Reclassified_Estimand_Level':'Final operational latency level L1 primitive, L2 request gate, L3 setup, L4 end-to-end workflow, or separately stratified scope.',
 'Reclassified_Mechanism_Family':'Final latency mechanism family; used for grouping eligible rows, not a ranking of comparable security mechanisms.',
 'Denominator_Status_v35':'Final RQ4 membership; EXCLUDED_* rows are outside the active cryptographic denominator. All other rows are active, including Suite NR.',
 'Adjudicated_Category_v35':'Final RQ4 construction class; preferred over original forensic category fields.',
 'Adjudicated_Exposure_Tier_v35':'Final RQ4 exposure-certainty tier; preferred over original Shor/forensic labels.',
 'Parameters_As_Reported':'Source-reported construction parameters; NR means no concrete parameters reported, not a verified suite.',
 'Original_Quantum_Exposure_Assessment':'Archived extracted source/reviewer assessment before final reconciliation; prefixes distinguish origin and missingness.',
 'Exposure_Provenance_Class':'Origin of exposure assessment; SOURCE_STATED_OR_EVALUATED versus reviewer/batch inference or non-applicability.',
 'Protection_Lifetime_As_Reported':'Source-reported required protection lifetime; do not invent a lifetime when NR.',
 'Migration_Alternative_As_Reported':'Migration option attributed to the primary source.',
 'Reviewer_Proposed_Alternative':'Reviewer migration suggestion; not evidence of implementation in the primary study.',
 'Claim_Text_As_Reported':'Extracted source claim wording; assess together with its locator and scope.',
 'Assessed_Claim_Scope':'Review-fenced scope to which support is assigned.',
 'Boundary_Codes':'Semicolon-delimited set B1 intent-to-delegation, B2 delegation-to-request, B3 request-to-execution, B4 execution-to-audit.',
 'Target_Boundary':'Single-boundary classification or MULTI_BOUNDARY; must agree with Boundary_Codes cardinality.',
 'Limitation_Codes_DG_AD_UG_NG':'Non-exclusive DG demonstrated gap, AD assumption dependence, UG unsupported generalization. NG is exclusive; absence of NG does not establish universal insecurity.',
 'QA_Adjudication_Disposition':'Recorded claim release/retention disposition. Red-zone subgroups are not separately encoded in this field.',
}

SPECIFIC={
 'Stage3_ID':'Unique Stage 3 report-row identifier.', 'Screening_ID':'Recorded upstream screening identifier; full screening register not distributed.',
 'Year':'Bibliographic year; two 2027 issue-date records have recorded pre-cutoff eligibility. Year alone is not an online-first date.',
 'Doc_Type':'Recorded publication/document type.', 'Authors':'Bibliographic authors.', 'Venue':'Publication venue.',
 'DOI':'DOI as recorded in the included-report metadata.', 'URL':'Recorded bibliographic/source URL.',
 'Confirmed_Stream':'Recorded evidence stream A, M, or M_AND_A; hybrid counts once.',
 'Target_Boundaries':'Report-level boundary metadata; claim synthesis uses Boundary_Codes in claims.csv.',
 'Architecture_Type':'Recorded report-level architecture description.', 'Interaction_Type':'Recorded actor interaction topology; may contain multiple actors.',
 'Architecture_Evidence_Location':'Primary-source locator supporting architecture metadata.', 'Extraction_Status':'Recorded report-level extraction/release grouping.',
 'Claim_Category':'Recorded functional role of claim: defense, formal framework, prototype, benchmark, attack finding, or vulnerability surface.',
 'Lifecycle_Stage':'Single primary operational lifecycle stage assigned to a claim.',
 'Threat_Attacker_Model':'Extracted adversary capabilities and threat-model scope.',
 'Cryptographic_Primitive_or_Mechanism':'Full claim-level construction/mechanism description.',
 'Enforcement_Point_Location':'Component or runtime location that enforces the assessed guarantee.',
 'Security_Property_Guaranteed':'Security property asserted within the stated assumptions and assessed scope.',
 'Trust_Assumptions':'Extracted trusted components and system/adversary assumptions.',
 'Formal_Evidence_Type':'Recorded formal-evidence category. Strict subset: TOOL_SUPPORTED_VERIFICATION, SECURITY_REDUCTION, LOGICAL_AXIOMS_WITH_PROOF.',
 'Performance_Overhead_Reported':'Free-text extracted performance description; numeric synthesis uses linked metric rows and final adjudication values.',
 'Exposed_Security_Function':'Claim-level security function relevant to quantum exposure.',
 'Artifact_Protection_Lifetime':'Claim-level source-reported artifact lifetime.',
 'Residual_Gap_and_Limitations':'Recorded limitation explanation, not necessarily an exploited vulnerability.',
 'Primary_RQ_Addressed':'Research question(s) addressed by the extracted claim.',
 'Evidence_Quote_and_Page':'Recorded quotation/locator anchor; primary PDFs are not distributed.',
 'Mechanism_ID':'Mechanism/attack identifier; not a study-family identifier.',
 'Protected_Object':'Object or representation for which the assessed property is claimed.',
 'Composition_Evidence':'Evidence and limits of composing mechanisms or boundaries.',
 'Extraction_Date':'Recorded extraction date.', 'Coding_Rationale':'Reviewer explanation of coding choices.',
 'Required_Additional_Evidence':'Evidence needed to resolve or extend the assessed claim.',
 'Baseline_Value':'Extracted comparable baseline value when reported; interpret with Baseline_Unit and scope.',
 'Baseline_Unit':'Unit of the baseline; must not be assumed equal to metric Unit.',
 'Measurement_Level':'Original extracted metric measurement scope.', 'Repetitions':'Reported repetitions/sample count or missingness text.',
 'Uncertainty':'Source-reported interval/variation or missingness text.', 'Audit_Date':'Recorded source-audit date.',
 'Source_Note':'Extracted source-context and qualification note.', 'Adjudication_Status':'Final metric adjudication status text.',
 'Adjudicated_Rationale_v35':'Final reviewer rationale for metric value/scope/disposition; may cite historical errors being corrected.',
 'Dependency_ID':'Unique RQ4 inventory-row identifier, including excluded non-cryptographic records.',
 'Protected_Asset':'Asset protected by the recorded dependency.', 'Security_Function':'Function of the dependency, such as authentication, confidentiality, or evidence integrity.',
 'Original_Construction_Algorithm_90char':'Archived 90-character construction description; use full mechanism and final adjudication fields for interpretation.',
 'Was_Truncated_At_90_Chars':'Flag for truncation of the original short construction field.',
 'Full_Untruncated_Claim_Mechanism':'Full parent-claim mechanism description.',
 'Reviewer_Inference_Status':'Recorded reviewer inference/review state, separate from source-reported evidence.',
 'Analysis_Status':'Recorded dependency analysis state.', 'Adjudicated_Estimand_v35':'Final dependency scope/estimand qualification.',
 'Adjudicated_Mechanism_v35':'Final mechanism qualification.', 'Adjudicated_Reason_v35':'Final dependency-adjudication rationale.',
 'Forensic_Exposure_Certainty':'Archived pre-final certainty classification; final analysis uses Adjudicated_Exposure_Tier_v35.',
 'Shor_Exposure_Tier':'Archived pre-final Shor exposure label; final analysis uses Adjudicated_Exposure_Tier_v35.',
 'Forensic_10Category_Class':'Archived pre-final construction classification; final analysis uses Adjudicated_Category_v35.',
 'Forensic_7Class_Group':'Archived pre-final grouped construction class.', 'Multi_Label_Classes':'Archived multilabel mechanism classes.',
 'Multi_Label_Count':'Count of archived multilabel mechanism classes.',
 'Original_Measurement_Level':'Archived extraction-level measurement scope before final reclassification.',
 'Original_Raw_Numeric_Value':'Original extracted numeric value retained for audit; not preferred for final latency analysis.',
 'Original_Raw_Unit':'Original extracted unit before corrections.', 'Original_Normalized_Latency_ms':'Archived original unit conversion to ms.',
 'Regex_Transcription_Bug_Flag':'Flag for detected shorthand/percentile transcription corruption.',
 'Regex_Bug_Type':'Recorded transcription-error category.', 'Corrected_Raw_Numeric_Value':'Intermediate corrected value; final analysis uses adjudicated fields.',
 'Corrected_Raw_Unit':'Unit of intermediate correction.', 'Corrected_Normalized_Latency_ms':'Intermediate corrected milliseconds; final analysis uses adjudicated milliseconds.',
 'Correction_Rationale_and_Quote':'Recorded intermediate correction rationale and source anchor.',
 'Is_Sibling_Claim_Duplicate':'Recorded sibling duplication indicator; final pooling follows Pooling_Eligibility_v35.',
 'Legacy_Inclusion_Status_436':'Historical exploratory 436-observation inclusion label; not current pooling eligibility.',
 'Legacy_Mechanism_Family_Table310':'Historical mechanism-family assignment.', 'Legacy_Estimand_Level_Table310b':'Historical estimand-level assignment.',
 'Forensic_Inclusion_Disposition':'Intermediate forensic disposition before final adjudication.',
 'Reclassification_Changed_L':'Recorded flag indicating change in operational latency level.',
 'Reclassification_Changed_Family':'Recorded flag indicating change in mechanism family.',
 'Reclassification_Rationale':'Recorded operational reclassification rationale.',
 'Adjudicated_Value_v35':'Final adjudicated value text in Adjudicated_Unit_v35; normalized latency is in Adjudicated_Latency_ms_v35.',
 'Adjudicated_Estimand_Scope_v35':'Final text qualifying the timer/operation scope.',
 'Dim1_Timer_Boundary':'Recorded timer-boundary operational dimension.',
 'Dim2_Recurrence_Lifecycle':'Recorded recurrence/lifecycle operational dimension.',
 'Dim3_Online_Offline_Mode':'Recorded online/offline operational dimension.',
 'Dim4_Statistic_Type':'Recorded statistic-type operational dimension. Workload and mechanism fields hold the other operation-context descriptions.',
}


def generate_dictionary():
    rows=[]
    for table,frame in load_tables().items():
        for col in frame.columns:
            description=COMMON.get(col,SPECIFIC.get(col))
            if description is None:
                raise ValueError(f'Missing column description: {table}.{col}')
            dtype='number' if pd.api.types.is_numeric_dtype(frame[col]) else 'string'
            rows.append({'Table_Name':table+'.csv','Column_Name':col,'Data_Type':dtype,'Description':description})
    assert len(rows)==188
    pd.DataFrame(rows).to_csv(ROOT/'protocol/data_dictionary.csv',index=False)


if __name__=='__main__':
    generate_dictionary()
    generate_reporting(ROOT/'results')
    print('Generated complete 188-column dictionary, derived reporting tables, and 220-decision register.')
