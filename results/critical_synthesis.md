# Post hoc critical synthesis

Post hoc descriptive synthesis; no primary-source recoding, causal estimates, or new human sign-off. Canonical data release: 3.6.3. Derived analysis revision: CS1 (3 November 2026).

Units are claims nested within canonical reports. Role uses Claim_Category; stream uses report-level Confirmed_Stream. These are different axes. Counts are descriptive; no significance or equivalence tests are performed.

## Claim-role sensitivity

| role | qa | claims | reports | ready | supported | DG | AD | UG | focused_formal | broad_proof_including_theoretic | deployment | stage45 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mechanism/framework/prototype | All | 346 | 328 | 298 | 256 | 81 | 343 | 141 | 26 | 73 | 14 | 4 |
| Mechanism/framework/prototype | READY | 298 | 285 | 298 | 256 | 69 | 296 | 94 | 25 | 71 | 14 | 2 |
| Attack/benchmark/attack-surface | All | 238 | 218 | 232 | 226 | 159 | 172 | 81 | 3 | 10 | 12 | 3 |
| Attack/benchmark/attack-surface | READY | 232 | 214 | 232 | 225 | 157 | 167 | 75 | 2 | 9 | 11 | 2 |

## Evidence streams

| stream | qa | claims | reports | ready | supported | DG | AD | UG | focused_formal | broad_proof_including_theoretic | deployment | stage45 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M | All | 129 | 107 | 104 | 90 | 27 | 127 | 51 | 8 | 20 | 7 | 3 |
| M | READY | 104 | 87 | 104 | 90 | 20 | 102 | 26 | 8 | 20 | 7 | 2 |
| A | All | 290 | 228 | 275 | 250 | 153 | 231 | 123 | 7 | 25 | 11 | 0 |
| A | READY | 275 | 221 | 275 | 250 | 148 | 218 | 109 | 7 | 24 | 11 | 0 |
| M_AND_A | All | 165 | 107 | 151 | 142 | 60 | 157 | 48 | 14 | 38 | 8 | 4 |
| M_AND_A | READY | 151 | 98 | 151 | 141 | 58 | 143 | 34 | 12 | 36 | 7 | 2 |

## Support and QA selection

| qa | claims | reports | ready | supported | DG | AD | UG | focused_formal | broad_proof_including_theoretic | deployment | stage45 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| READY | 530 | 406 | 530 | 481 | 226 | 463 | 169 | 27 | 80 | 25 | 4 |
| FLAGGED | 54 | 50 | 0 | 1 | 14 | 52 | 53 | 2 | 3 | 1 | 3 |

| support | claims | reports | ready | supported | DG | AD | UG | focused_formal | broad_proof_including_theoretic | deployment | stage45 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SUPPORTED_WITHIN_SCOPE | 482 | 377 | 481 | 482 | 210 | 416 | 125 | 25 | 73 | 23 | 4 |
| PARTIALLY_SUPPORTED | 101 | 94 | 49 | 0 | 29 | 99 | 96 | 4 | 10 | 3 | 3 |
| NOT_SUPPORTED | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |

## Formal-evidence definitions

Focused categories comprise TOOL_SUPPORTED_VERIFICATION, SECURITY_REDUCTION and LOGICAL_AXIOMS_WITH_PROOF. The broader sensitivity includes THEORETIC_PROOF. Neither category set establishes machine checking or proof correctness.

## Composition coding

```json
{
  "field_type": "Free-text appraisal, not a standardized composition-proof verdict; no count of end-to-end verified systems can be inferred.",
  "four_boundaries": {
    "claims": 80,
    "reports": 78,
    "ready": 71,
    "supported": 61,
    "DG": 40,
    "AD": 80,
    "UG": 56,
    "focused_formal": 7,
    "broad_proof_including_theoretic": 18,
    "deployment": 3,
    "stage45": 0
  },
  "four_boundaries_ready": {
    "claims": 71,
    "reports": 69,
    "ready": 71,
    "supported": 61,
    "DG": 35,
    "AD": 71,
    "UG": 47,
    "focused_formal": 6,
    "broad_proof_including_theoretic": 17,
    "deployment": 3,
    "stage45": 0
  }
}
```

## Latency clustering and statistic mixture

For each report and level, take its median first, then the median across reports (equal report weight). Neither median is a pooled treatment effect or an estimate of incremental overhead. The distribution mixes source statistic types; see timer/statistic counts in the JSON. Three eligible READY records have Dim1/final-level discrepancies (R1-E03-MET-027, R1-E05-MET-063 and R1-E05-MET-064). Use Reclassified_Estimand_Level as defined in the dictionary; canonical fields are preserved.

| level | qa | n | reports | observation_median_ms | report_median_ms | largest_report_n | top3_reports_n | mean_point_n | mean_point_median_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L2: Per-Request Policy / Gate Check | All | 61 | 38 | 12.4 | 16.3 | 9 | 17 | 51 | 15.1 |
| L2: Per-Request Policy / Gate Check | READY | 51 | 32 | 10.8 | 11.15 | 9 | 17 | 43 | 14.2 |
| L3: Session / Enclave / Consensus / Proof Setup | All | 42 | 19 | 262.88 | 100 | 6 | 16 | 41 | 173.86 |
| L3: Session / Enclave / Consensus / Proof Setup | READY | 40 | 17 | 262.88 | 100 | 6 | 16 | 39 | 173.86 |
| L4: End-to-End Agent Workflow Runtime | All | 206 | 105 | 1125 | 351 | 16 | 37 | 193 | 1700 |
| L4: End-to-End Agent Workflow Runtime | READY | 193 | 96 | 1700 | 432.655 | 16 | 37 | 180 | 2035 |
| L1: Primitive / Crypto Micro-Op | All | 90 | 39 | 1.7995 | 3.8 | 8 | 22 | 87 | 1.82 |
| L1: Primitive / Crypto Micro-Op | READY | 78 | 33 | 1.7645 | 4.3 | 8 | 22 | 75 | 1.82 |

## PQC linkage and missingness

No dependency is copied to sibling claims. Report-level membership asks only whether the same report has an active dependency and a Stage 4–5 claim, without upgrading other claims. Lifetimes are original text labels; no numeric years or threat dates are imputed.

```json
{
  "All": {
    "active_records": 266,
    "active_claims": 231,
    "active_reports": 228,
    "stage45": {
      "claims": 7,
      "reports": 4,
      "ready": 4,
      "supported": 4,
      "DG": 0,
      "AD": 7,
      "UG": 5,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 2,
      "stage45": 7
    },
    "stage45_direct_link": {
      "claims": 4,
      "reports": 4,
      "ready": 2,
      "supported": 2,
      "DG": 0,
      "AD": 4,
      "UG": 3,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 1,
      "stage45": 4
    },
    "stage45_in_crypto_reports": {
      "claims": 7,
      "reports": 4,
      "ready": 4,
      "supported": 4,
      "DG": 0,
      "AD": 7,
      "UG": 5,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 2,
      "stage45": 7
    },
    "lifetime_exact_missing": 150,
    "active_lifetime": {
      "EPHEMERAL_SESSION": 8,
      "NOT_REPORTED": 26,
      "Example sessionkey validity2h/1h/5min by configuration": 1,
      "Session-key validity per Auth configuration": 1,
      "NR": 124,
      "Long-term audit purpose; exact retention NR": 1,
      "Short-lived; concrete TTL NR": 1,
      "Short-lived; exact TTL NR": 1,
      "Audit retention policy-dependent; exact duration NR": 1,
      "Identity lifetime NR": 1,
      "Long-term security is stated as motivation p.6; exact retention NR": 1,
      "Ephemeralworkload/shortlivedtokens;TTLNR": 1,
      "Session-scoped": 1,
      "Longlivedidentity with ephemeralsessions": 1,
      "Publishedartifact;retentionNR": 1,
      "Longlivedsealedsecrets and shortlivedIETtokens": 1,
      "ShortlivedSVID/JITcredentials": 1,
      "Sessionnonce and persistentauthorizeddefinition": 1,
      "Token<=15min": 1,
      "Shortlivedaccess-token;TTLNR": 1,
      "Registrationrenewal/certificaterevocationpolicy": 1,
      "Archivedauditlogsyears as authorstates": 1,
      "Shorttrafficconfidentialityhalf-life as authorstates": 1,
      "Memory/session;retentionNR": 1,
      "SSH30days/API14days;additivewindow5min,prune0min": 1,
      "Approval timeout10min standard /3min HIGH-CRITICAL;single use": 1,
      "LonglivedDID;VCvaliditydependingissuer": 1,
      "Shortliveddecisiontoken;examplemitigationbundle60s": 1,
      "Snapshotretentionpolicy;offlinefreshnessoptional": 1,
      "Shortvaliditywindow,TTLNR": 1,
      "Short time windows specified by protocol": 1,
      "Expiry/use budget caveats": 1,
      "Session key lifetime NR": 1,
      "EAAI TTL300s illustrative pipeline": 1,
      "Task estimate plus20%; short-livedtasktokens": 1,
      "90day retention; assurance anchored to trustedloghead": 1,
      "30s freshness window": 1,
      "ExistingUMA/RPTexpiry plus delegation constraints; durationNR": 1,
      "Authorasset horizons p2:identity3-5y/servercert5-10y/root20-30y": 1,
      "Tokenexp; replaycache600s config": 1,
      "JWT-SVID2 min;accessTTLboundedcache": 1,
      "Expiringgrants;cache freshness policy": 1,
      "1hourcertificateTTL;30 minrotation": 1,
      "5mintokenTTL;not absolute anti-replay": 1,
      "Default token expiry24h; shorter lifetimes suggested p.8": 1,
      "Example delta_h10s,Wmax30s; bounded validity is not a PQ protection-horizon measurement": 1,
      "PERMANENT_AUDIT": 27,
      "LONG_TERM_IDENTITY": 6,
      "SHORT_LIVED_TOKEN": 24,
      "LONG_TERM_CREDENTIAL": 8
    },
    "active_source_provenance": {
      "NOT_EVALUATED_IN_SOURCE_REVIEWER_CLASSIFIED": 152,
      "SOURCE_STATED_OR_EVALUATED": 15,
      "REVIEWER_CONDITIONAL_INFERENCE": 9,
      "BATCH_E06_E09_AUTO_INFERRED_FROM_STAGE0": 90
    },
    "active_exposure": {
      "Grover / Symmetric / Lattice FHE / STARK": 73,
      "Tier A: Direct Mathematical Shor Exposure": 82,
      "Unspecified Algorithm / Generic Scheme (Suite NR)": 44,
      "Tier B: Conditional Protocol / Token Wrappers": 33,
      "Tier C: Conditional Hardware Enclave Roots": 18,
      "Evaluated or Proposed PQC / Quantum Constructions": 16
    }
  },
  "READY": {
    "active_records": 224,
    "active_claims": 197,
    "active_reports": 195,
    "stage45": {
      "claims": 4,
      "reports": 2,
      "ready": 4,
      "supported": 4,
      "DG": 0,
      "AD": 4,
      "UG": 2,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 1,
      "stage45": 4
    },
    "stage45_direct_link": {
      "claims": 2,
      "reports": 2,
      "ready": 2,
      "supported": 2,
      "DG": 0,
      "AD": 2,
      "UG": 1,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 1,
      "stage45": 2
    },
    "stage45_in_crypto_reports": {
      "claims": 4,
      "reports": 2,
      "ready": 4,
      "supported": 4,
      "DG": 0,
      "AD": 4,
      "UG": 2,
      "focused_formal": 0,
      "broad_proof_including_theoretic": 0,
      "deployment": 1,
      "stage45": 4
    },
    "lifetime_exact_missing": 121,
    "active_lifetime": {
      "EPHEMERAL_SESSION": 6,
      "NOT_REPORTED": 24,
      "Example sessionkey validity2h/1h/5min by configuration": 1,
      "Session-key validity per Auth configuration": 1,
      "NR": 97,
      "Long-term audit purpose; exact retention NR": 1,
      "Short-lived; concrete TTL NR": 1,
      "Short-lived; exact TTL NR": 1,
      "Audit retention policy-dependent; exact duration NR": 1,
      "Identity lifetime NR": 1,
      "Long-term security is stated as motivation p.6; exact retention NR": 1,
      "Ephemeralworkload/shortlivedtokens;TTLNR": 1,
      "Session-scoped": 1,
      "Longlivedidentity with ephemeralsessions": 1,
      "Publishedartifact;retentionNR": 1,
      "Longlivedsealedsecrets and shortlivedIETtokens": 1,
      "Sessionnonce and persistentauthorizeddefinition": 1,
      "Shortlivedaccess-token;TTLNR": 1,
      "Registrationrenewal/certificaterevocationpolicy": 1,
      "Archivedauditlogsyears as authorstates": 1,
      "Shorttrafficconfidentialityhalf-life as authorstates": 1,
      "Memory/session;retentionNR": 1,
      "SSH30days/API14days;additivewindow5min,prune0min": 1,
      "Approval timeout10min standard /3min HIGH-CRITICAL;single use": 1,
      "LonglivedDID;VCvaliditydependingissuer": 1,
      "Shortliveddecisiontoken;examplemitigationbundle60s": 1,
      "Snapshotretentionpolicy;offlinefreshnessoptional": 1,
      "Shortvaliditywindow,TTLNR": 1,
      "Short time windows specified by protocol": 1,
      "Expiry/use budget caveats": 1,
      "Session key lifetime NR": 1,
      "EAAI TTL300s illustrative pipeline": 1,
      "30s freshness window": 1,
      "ExistingUMA/RPTexpiry plus delegation constraints; durationNR": 1,
      "Tokenexp; replaycache600s config": 1,
      "JWT-SVID2 min;accessTTLboundedcache": 1,
      "Expiringgrants;cache freshness policy": 1,
      "1hourcertificateTTL;30 minrotation": 1,
      "5mintokenTTL;not absolute anti-replay": 1,
      "Default token expiry24h; shorter lifetimes suggested p.8": 1,
      "Example delta_h10s,Wmax30s; bounded validity is not a PQ protection-horizon measurement": 1,
      "PERMANENT_AUDIT": 25,
      "LONG_TERM_IDENTITY": 4,
      "SHORT_LIVED_TOKEN": 22,
      "LONG_TERM_CREDENTIAL": 8
    },
    "active_source_provenance": {
      "NOT_EVALUATED_IN_SOURCE_REVIEWER_CLASSIFIED": 126,
      "SOURCE_STATED_OR_EVALUATED": 6,
      "REVIEWER_CONDITIONAL_INFERENCE": 9,
      "BATCH_E06_E09_AUTO_INFERRED_FROM_STAGE0": 83
    },
    "active_exposure": {
      "Grover / Symmetric / Lattice FHE / STARK": 63,
      "Tier A: Direct Mathematical Shor Exposure": 77,
      "Unspecified Algorithm / Generic Scheme (Suite NR)": 36,
      "Tier B: Conditional Protocol / Token Wrappers": 25,
      "Tier C: Conditional Hardware Enclave Roots": 15,
      "Evaluated or Proposed PQC / Quantum Constructions": 8
    }
  }
}
```

## Reproduction

Run `node scripts/critical_synthesis.mjs`. The JSON includes input SHA-256, diagnostic category counts, and key claim IDs. Original evidence labels remain unchanged.
