/** Post hoc descriptive analyses. Reads canonical CSVs without changing them.
 * Run: node scripts/critical_synthesis.mjs (from any working directory).
 * CSV decoding supports quoted commas, escaped quotes, and multiline fields.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export function parseCSV(text) {
  text = text.replace(/^\uFEFF/, '');
  const rows=[]; let row=[], field='', quoted=false;
  for (let i=0;i<text.length;i++) {
    const ch=text[i];
    if (ch==='"') {
      if (quoted && text[i+1]==='"') { field+='"';i++; }
      else quoted=!quoted;
    } else if (ch===',' && !quoted) {row.push(field);field='';}
    else if ((ch==='\n'||ch==='\r') && !quoted) {
      if (ch==='\r' && text[i+1]==='\n') i++;
      row.push(field); if(row.some(v=>v!==''))rows.push(row);row=[];field='';
    } else field+=ch;
  }
  assert.equal(quoted,false,'Unclosed CSV quote');
  if(field!==''||row.length){row.push(field);rows.push(row);}
  const headers=rows.shift(); assert.equal(new Set(headers).size,headers.length);
  return rows.map((cells,i)=>{assert.equal(cells.length,headers.length,`CSV row ${i+2}`);return Object.fromEntries(headers.map((h,j)=>[h,cells[j]]));});
}
export const readCSV = rel => parseCSV(fs.readFileSync(path.join(root,rel),'utf8'));
export const countBy = (rows,key) => rows.reduce((a,r)=>{const k=typeof key==='function'?key(r):r[key];a[k]=(a[k]||0)+1;return a;},{});
export const groups = (rows,key) => Object.groupBy(rows,typeof key==='function'?key:r=>r[key]);
export const unique = (rows,key='Source_Record_ID') => [...new Set(rows.map(r=>r[key]))];
export const median = values => { const s=[...values].sort((a,b)=>a-b),n=s.length;return n? (s[Math.floor(n/2)]+s[Math.floor((n-1)/2)])/2:null; };
const formal=['TOOL_SUPPORTED_VERIFICATION','SECURITY_REDUCTION','LOGICAL_AXIOMS_WITH_PROOF'];
const mechanism=['DEFENSIVE_MECHANISM','FORMAL_FRAMEWORK','SYSTEM_PROTOTYPE'];
const stage45 = r => /^STAGE_[45]_/.test(r.PQC_Migration_Stage);
const has = (r,code) => r.Limitation_Codes_DG_AD_UG_NG.split(';').includes(code);
const pop = rows => ({claims:rows.length,reports:unique(rows).length,ready:rows.filter(r=>r.Claim_QA==='READY').length,
  supported:rows.filter(r=>r.Claim_Support_Status==='SUPPORTED_WITHIN_SCOPE').length,
  DG:rows.filter(r=>has(r,'DG')).length,AD:rows.filter(r=>has(r,'AD')).length,UG:rows.filter(r=>has(r,'UG')).length,
  focused_formal:rows.filter(r=>formal.includes(r.Formal_Evidence_Type)).length,
  broad_proof_including_theoretic:rows.filter(r=>[...formal,'THEORETIC_PROOF'].includes(r.Formal_Evidence_Type)).length,
  deployment:rows.filter(r=>['DEPLOYMENT_LIKE_EVALUATION','PRODUCTION_DEPLOYED'].includes(r.Implementation_Maturity)).length,
  stage45:rows.filter(stage45).length});

export function calculate() {
  const c=readCSV('data/claims.csv'),s=readCSV('data/studies.csv'),w=readCSV('data/rq3_latency_crosswalk.csv'),d=readCSV('data/rq4_dependencies.csv');
  const sm=new Map(s.map(r=>[r.Source_Record_ID,r]));
  const claims=c.map(r=>({...r,stream:sm.get(r.Source_Record_ID).Confirmed_Stream,tier:sm.get(r.Source_Record_ID).Evidence_Tier,
    role:mechanism.includes(r.Claim_Category)?'Mechanism/framework/prototype':'Attack/benchmark/attack-surface'}));
  const active=d.filter(r=>!r.Denominator_Status_v35.startsWith('EXCLUDED_'));
  const activeClaims=new Set(unique(active,'Claim_ID')),activeReports=new Set(unique(active));
  const byRole={};for(const [k,rows] of Object.entries(groups(claims,'role')))byRole[k]={All:pop(rows),READY:pop(rows.filter(r=>r.Claim_QA==='READY'))};
  const byStream={};for(const [k,rows] of Object.entries(groups(claims,'stream')))byStream[k]={All:pop(rows),READY:pop(rows.filter(r=>r.Claim_QA==='READY'))};
  const byTierRole={};for(const [k,rows] of Object.entries(groups(claims,r=>`${r.tier} / ${r.role}`)))byTierRole[k]=pop(rows);
  const full=claims.filter(r=>r.Boundary_Codes.split(';').length===4);
  const supportQA=Object.entries(groups(claims,'Claim_QA')).map(([qa,rows])=>({qa,...pop(rows)}));
  const supportUG=Object.entries(groups(claims,'Claim_Support_Status')).map(([support,rows])=>({support,...pop(rows)}));
  const eligible=w.filter(r=>r.Pooling_Eligibility_v35==='ELIGIBLE_PRIMARY_STRATIFIED_SYNTHESIS');
  const lat=[];
  for(const [level,rows] of Object.entries(groups(eligible,'Reclassified_Estimand_Level')))for(const [qa,rr] of [['All',rows],['READY',rows.filter(r=>r.Claim_QA==='READY')]]){
    const gr=groups(rr,'Source_Record_ID'),sizes=Object.values(gr).map(x=>x.length).sort((a,b)=>b-a);
    lat.push({level,qa,n:rr.length,reports:Object.keys(gr).length,observation_median_ms:median(rr.map(r=>Number(r.Adjudicated_Latency_ms_v35))),
      report_median_ms:median(Object.values(gr).map(a=>median(a.map(r=>Number(r.Adjudicated_Latency_ms_v35))))),
      largest_report_n:sizes[0],top3_reports_n:sizes.slice(0,3).reduce((a,b)=>a+b,0),
      mean_point_n:rr.filter(r=>r.Dim4_Statistic_Type==='MEAN_OR_POINT_REPORTED').length,
      mean_point_median_ms:median(rr.filter(r=>r.Dim4_Statistic_Type==='MEAN_OR_POINT_REPORTED').map(r=>Number(r.Adjudicated_Latency_ms_v35))),
      timer:countBy(rr,'Dim1_Timer_Boundary'),statistic:countBy(rr,'Dim4_Statistic_Type'),
      timer_field_discrepancies:rr.filter(r=>r.Dim1_Timer_Boundary!==r.Reclassified_Estimand_Level).map(r=>({Metric_ID:r.Metric_ID,recorded_Dim1:r.Dim1_Timer_Boundary,final_level:r.Reclassified_Estimand_Level}))});
  }
  const pqc={};for(const [qa,cc,dd] of [['All',claims,active],['READY',claims.filter(r=>r.Claim_QA==='READY'),active.filter(r=>r.Claim_QA==='READY')]]){
    const dc=new Set(unique(dd,'Claim_ID')),dr=new Set(unique(dd)),p=cc.filter(stage45),pDirect=p.filter(r=>dc.has(r.Claim_ID));
    pqc[qa]={active_records:dd.length,active_claims:dc.size,active_reports:dr.size,stage45:pop(p),
      stage45_direct_link:pop(pDirect),stage45_in_crypto_reports:pop(p.filter(r=>dr.has(r.Source_Record_ID))),
      lifetime_exact_missing:dd.filter(r=>['NR','NOT_REPORTED',''].includes(r.Protection_Lifetime_As_Reported.trim())).length,
      active_lifetime:countBy(dd,'Protection_Lifetime_As_Reported'),active_source_provenance:countBy(dd,'Exposure_Provenance_Class'),
      active_exposure:countBy(dd,'Adjudicated_Exposure_Tier_v35')};
  }
  const mechanismRows=claims.filter(r=>mechanism.includes(r.Claim_Category));
  const reportIndicators={};
  for(const [qa,cc] of [['All',claims],['READY',claims.filter(r=>r.Claim_QA==='READY')]]){
    const gg=groups(cc,'Source_Record_ID');
    reportIndicators[qa]={reports:Object.keys(gg).length,any_UG:Object.values(gg).filter(a=>a.some(r=>has(r,'UG'))).length,
      any_focused_formal:Object.values(gg).filter(a=>a.some(r=>formal.includes(r.Formal_Evidence_Type))).length};
  }
  const result={analysis:'Post hoc descriptive synthesis; no primary-source recoding, causal estimates, or new human sign-off',
    source_sha256:Object.fromEntries(['studies','claims','rq3_metrics','rq3_latency_crosswalk','rq4_dependencies'].map(n=>[n,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'data',n+'.csv'))).digest('hex')])),
    corpus:pop(claims),byRole,byStream,byTierRole,supportQA,supportUG,reportIndicators,
    composition:{field_type:'Free-text appraisal, not a standardized composition-proof verdict; no count of end-to-end verified systems can be inferred.',four_boundaries:pop(full),
      four_boundaries_ready:pop(full.filter(r=>r.Claim_QA==='READY'))},latency:lat,pqc,
    tool_supported_records:claims.filter(r=>r.Formal_Evidence_Type==='TOOL_SUPPORTED_VERIFICATION').map(r=>({Claim_ID:r.Claim_ID,Claim_QA:r.Claim_QA,Study_Title:r.Study_Title,Composition_Evidence:r.Composition_Evidence,Security_Property_Guaranteed:r.Security_Property_Guaranteed,Evidence_Quote_and_Page:r.Evidence_Quote_and_Page})),
    record_ids:{four_boundary:full.map(r=>r.Claim_ID),focused_formal:claims.filter(r=>formal.includes(r.Formal_Evidence_Type)).map(r=>r.Claim_ID),
      pqc_stage45:claims.filter(stage45).map(r=>({Claim_ID:r.Claim_ID,Source_Record_ID:r.Source_Record_ID,QA:r.Claim_QA,direct_active_link:activeClaims.has(r.Claim_ID),report_active_link:activeReports.has(r.Source_Record_ID)}))}};
  assert.equal(c.length,584);assert.equal(s.length,442);assert.equal(w.length,454);assert.equal(d.length,283);
  assert.equal(eligible.length,399);assert.equal(active.length,266);
  return result;
}
const table=(rows)=>{const keys=Object.keys(rows[0]);return '| '+keys.join(' | ')+' |\n| '+keys.map(()=>'---').join(' | ')+' |\n'+rows.map(r=>'| '+keys.map(k=>String(r[k]).replaceAll('|','/')).join(' | ')+' |').join('\n');};
export function report(r){
 const roleRows=Object.entries(r.byRole).flatMap(([role,qs])=>Object.entries(qs).map(([qa,v])=>({role,qa,...v})));
 return '# Post hoc critical synthesis\n\n'+r.analysis+'. Canonical data release: 3.6.3. Derived analysis revision: CS1 (3 November 2026).\n\n'+
 'Units are claims nested within canonical reports. Role uses Claim_Category; stream uses report-level Confirmed_Stream. These are different axes. Counts are descriptive; no significance or equivalence tests are performed.\n\n'+
 '## Claim-role sensitivity\n\n'+table(roleRows)+'\n\n## Evidence streams\n\n'+table(Object.entries(r.byStream).flatMap(([stream,qs])=>Object.entries(qs).map(([qa,v])=>({stream,qa,...v}))))+
 '\n\n## Support and QA selection\n\n'+table(r.supportQA)+'\n\n'+table(r.supportUG)+
 '\n\n## Formal-evidence definitions\n\nFocused categories comprise TOOL_SUPPORTED_VERIFICATION, SECURITY_REDUCTION and LOGICAL_AXIOMS_WITH_PROOF. The broader sensitivity includes THEORETIC_PROOF. Neither category set establishes machine checking or proof correctness.\n\n'+
 '## Composition coding\n\n```json\n'+JSON.stringify(r.composition,null,2)+'\n```\n\n'+
 '## Latency clustering and statistic mixture\n\nFor each report and level, take its median first, then the median across reports (equal report weight). Neither median is a pooled treatment effect or an estimate of incremental overhead. The distribution mixes source statistic types; see timer/statistic counts in the JSON. Three eligible READY records have Dim1/final-level discrepancies (R1-E03-MET-027, R1-E05-MET-063 and R1-E05-MET-064). Use Reclassified_Estimand_Level as defined in the dictionary; canonical fields are preserved.\n\n'+table(r.latency.map(({timer,statistic,timer_field_discrepancies,...v})=>v))+
 '\n\n## PQC linkage and missingness\n\nNo dependency is copied to sibling claims. Report-level membership asks only whether the same report has an active dependency and a Stage 4–5 claim, without upgrading other claims. Lifetimes are original text labels; no numeric years or threat dates are imputed.\n\n```json\n'+JSON.stringify(r.pqc,null,2)+'\n```\n\n'+
 '## Reproduction\n\nRun `node scripts/critical_synthesis.mjs`. The JSON includes input SHA-256, diagnostic category counts, and key claim IDs. Original evidence labels remain unchanged.\n';
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const r=calculate();fs.mkdirSync(path.join(root,'results'),{recursive:true});
 fs.writeFileSync(path.join(root,'results/critical_synthesis.json'),JSON.stringify(r,null,2)+'\n');
 fs.writeFileSync(path.join(root,'results/critical_synthesis.md'),report(r));
 console.log(JSON.stringify({claims:r.corpus.claims,role_strata:Object.keys(r.byRole).length,latency_strata:r.latency.length,outputs:['critical_synthesis.json','critical_synthesis.md']}));
}
