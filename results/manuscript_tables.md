# Computed manuscript reporting tables

Release 3.6.3; generated from the unchanged v3.5 canonical CSV baseline. No primary-PDF or screening-register verification is performed.

## Table 3.10 numerical view: eligible latency strata

| Axis | Stratum | Claim_QA_Stratum | Observations | Claims | Reports | p25_ms | p50_ms | p75_ms | IQR_ms | Report_Clustered_p50_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reclassified_Estimand_Level | L1: Primitive / Crypto Micro-Op | All | 90 | 40 | 39 | 0.217719 | 1.7995 | 13.4095 | 13.1918 | 3.8 |
| Reclassified_Estimand_Level | L1: Primitive / Crypto Micro-Op | READY | 78 | 34 | 33 | 0.264792 | 1.7645 | 18.275 | 18.0102 | 4.3 |
| Reclassified_Estimand_Level | L2: Per-Request Policy / Gate Check | All | 61 | 38 | 38 | 2.83 | 12.4 | 36.2 | 33.37 | 16.3 |
| Reclassified_Estimand_Level | L2: Per-Request Policy / Gate Check | READY | 51 | 32 | 32 | 2.15 | 10.8 | 32.55 | 30.4 | 11.15 |
| Reclassified_Estimand_Level | L3: Session / Enclave / Consensus / Proof Setup | All | 42 | 20 | 19 | 10.04 | 262.88 | 8375 | 8364.96 | 100 |
| Reclassified_Estimand_Level | L3: Session / Enclave / Consensus / Proof Setup | READY | 40 | 18 | 17 | 12.42 | 262.88 | 8977.5 | 8965.08 | 100 |
| Reclassified_Estimand_Level | L4: End-to-End Agent Workflow Runtime | All | 206 | 107 | 105 | 42.5397 | 1125 | 9586.75 | 9544.21 | 351 |
| Reclassified_Estimand_Level | L4: End-to-End Agent Workflow Runtime | READY | 193 | 98 | 96 | 80 | 1700 | 10900 | 10820 | 432.655 |
| Reclassified_Mechanism_Family | 1. Classical Crypto / Token Gate | All | 119 | 63 | 62 | 0.374 | 4.6 | 32.45 | 32.076 | 7.212 |
| Reclassified_Mechanism_Family | 1. Classical Crypto / Token Gate | READY | 110 | 56 | 55 | 0.317 | 4.6 | 43.515 | 43.198 | 7.3 |
| Reclassified_Mechanism_Family | 2. PQC / Quantum Primitives | All | 13 | 5 | 4 | 2 | 3.2 | 20.33 | 18.33 | 11.565 |
| Reclassified_Mechanism_Family | 2. PQC / Quantum Primitives | READY | 3 | 3 | 2 | 0.081 | 0.082 | 10.206 | 10.125 | 10.2055 |
| Reclassified_Mechanism_Family | 3. Deterministic Policy / Kernel | All | 22 | 15 | 15 | 0.975 | 12.35 | 396.975 | 396 | 250 |
| Reclassified_Mechanism_Family | 3. Deterministic Policy / Kernel | READY | 18 | 14 | 14 | 8.65 | 50.5 | 838 | 829.35 | 300.95 |
| Reclassified_Mechanism_Family | 4. End-to-End Agent Workflows | All | 141 | 74 | 72 | 15.6 | 250 | 10900 | 10884.4 | 105.5 |
| Reclassified_Mechanism_Family | 4. End-to-End Agent Workflows | READY | 130 | 64 | 62 | 16.175 | 354 | 13450 | 13433.8 | 172.5 |
| Reclassified_Mechanism_Family | 5. Blockchain / Consensus Ledger | All | 35 | 12 | 12 | 92.125 | 944 | 3274.55 | 3182.43 | 615.25 |
| Reclassified_Mechanism_Family | 5. Blockchain / Consensus Ledger | READY | 32 | 11 | 11 | 88.3125 | 872 | 4152.9 | 4064.59 | 600 |
| Reclassified_Mechanism_Family | 6. Hardware TEE / ORAM Enclave | All | 31 | 6 | 6 | 12.85 | 1800 | 5870 | 5857.15 | 297.942 |
| Reclassified_Mechanism_Family | 6. Hardware TEE / ORAM Enclave | READY | 31 | 6 | 6 | 12.85 | 1800 | 5870 | 5857.15 | 297.942 |
| Reclassified_Mechanism_Family | 7. LLM-Judge / Quorum / FHE | All | 38 | 17 | 17 | 98.69 | 1110.4 | 8992.5 | 8893.81 | 3700 |
| Reclassified_Mechanism_Family | 7. LLM-Judge / Quorum / FHE | READY | 38 | 17 | 17 | 98.69 | 1110.4 | 8992.5 | 8893.81 | 3700 |

## Table 3.12 numerical view: RQ4 construction categories

| Category | Claim_QA_Stratum | Records | Claims | Reports | Exposure_Tier |
| --- | --- | --- | --- | --- | --- |
| 1. Cryptographic Hashes, Merkle Trees & Hash-STARKs | All | 36 | 36 | 36 | Grover / Symmetric / Lattice FHE / STARK |
| 1. Cryptographic Hashes, Merkle Trees & Hash-STARKs | READY | 32 | 32 | 32 | Grover / Symmetric / Lattice FHE / STARK |
| 10a-i. Unspecified Signed / Generic ZKP / HE (Suite NR) | All | 44 | 44 | 44 | Unspecified Algorithm / Generic Scheme (Suite NR) |
| 10a-i. Unspecified Signed / Generic ZKP / HE (Suite NR) | READY | 36 | 36 | 36 | Unspecified Algorithm / Generic Scheme (Suite NR) |
| 10a-ii. Rejected False Crypto Label / Unspecified Context (7 REJECT_CLASS) | All | 7 | 7 | 7 | Non-Cryptographic Baselines & Excluded Own Non-Crypto |
| 10a-ii. Rejected False Crypto Label / Unspecified Context (7 REJECT_CLASS) | READY | 7 | 7 | 7 | Non-Cryptographic Baselines & Excluded Own Non-Crypto |
| 10b. Excluded Non-Crypto Own Mechanism (8 E08-E09 + 2 Baselines) | All | 10 | 10 | 10 | Non-Cryptographic Baselines & Excluded Own Non-Crypto |
| 10b. Excluded Non-Crypto Own Mechanism (8 E08-E09 + 2 Baselines) | READY | 10 | 10 | 10 | Non-Cryptographic Baselines & Excluded Own Non-Crypto |
| 2. Identity & Transport Protocols (OAuth/JWT/DID/mTLS) | All | 33 | 33 | 33 | Tier B: Conditional Protocol / Token Wrappers |
| 2. Identity & Transport Protocols (OAuth/JWT/DID/mTLS) | READY | 25 | 25 | 25 | Tier B: Conditional Protocol / Token Wrappers |
| 3. Explicit ECC & Classical Signatures (Ed25519/ECDSA/RSA) | All | 42 | 40 | 40 | Tier A: Direct Mathematical Shor Exposure |
| 3. Explicit ECC & Classical Signatures (Ed25519/ECDSA/RSA) | READY | 41 | 39 | 39 | Tier A: Direct Mathematical Shor Exposure |
| 4. Symmetric MACs & Capability Tokens (HMAC/PRF) | All | 24 | 24 | 24 | Grover / Symmetric / Lattice FHE / STARK |
| 4. Symmetric MACs & Capability Tokens (HMAC/PRF) | READY | 22 | 22 | 22 | Grover / Symmetric / Lattice FHE / STARK |
| 5. Hardware Enclaves & Silicon Attestation (TEE/TPM) | All | 18 | 18 | 17 | Tier C: Conditional Hardware Enclave Roots |
| 5. Hardware Enclaves & Silicon Attestation (TEE/TPM) | READY | 15 | 15 | 14 | Tier C: Conditional Hardware Enclave Roots |
| 6. Symmetric Enc., ORAM, MPC & Lattice FHE | All | 13 | 11 | 11 | Grover / Symmetric / Lattice FHE / STARK |
| 6. Symmetric Enc., ORAM, MPC & Lattice FHE | READY | 9 | 7 | 7 | Grover / Symmetric / Lattice FHE / STARK |
| 7. Pairing & DLog ZK Proofs (Groth16/PLONK/ZKP) | All | 22 | 20 | 19 | Tier A: Direct Mathematical Shor Exposure |
| 7. Pairing & DLog ZK Proofs (Groth16/PLONK/ZKP) | READY | 19 | 17 | 16 | Tier A: Direct Mathematical Shor Exposure |
| 8. Classical RSA & Pairing/Threshold (RSA/BLS/IBE) | All | 18 | 18 | 18 | Tier A: Direct Mathematical Shor Exposure |
| 8. Classical RSA & Pairing/Threshold (RSA/BLS/IBE) | READY | 17 | 17 | 17 | Tier A: Direct Mathematical Shor Exposure |
| 9. Evaluated/Proposed PQC & Quantum Primitives | All | 16 | 11 | 11 | Evaluated or Proposed PQC / Quantum Constructions |
| 9. Evaluated/Proposed PQC & Quantum Primitives | READY | 8 | 6 | 6 | Evaluated or Proposed PQC / Quantum Constructions |

## Table 3.14 numerical view: tier sensitivity indicators

| Tier | Indicator | Unit | Numerator | Denominator | Percent |
| --- | --- | --- | --- | --- | --- |
| Tier 1 | MULTI_BOUNDARY | claims | 216 | 271 | 79.7048 |
| Tier 1 | SUPPORTED_WITHIN_SCOPE | claims | 222 | 271 | 81.9188 |
| Tier 1 | READY | claims | 243 | 271 | 89.6679 |
| Tier 1 | Strict_Formal | claims | 7 | 271 | 2.58303 |
| Tier 1 | AD | claims | 209 | 271 | 77.1218 |
| Tier 1 | Benchmark_PoC_Deployment | claims | 209 | 271 | 77.1218 |
| Tier 1 | No_Demonstrated_PQC_Migration | claims | 259 | 271 | 95.572 |
| Tier 1 | B1 | claims | 41 | 271 | 15.1292 |
| Tier 1 | B2 | claims | 220 | 271 | 81.1808 |
| Tier 1 | B3 | claims | 231 | 271 | 85.2399 |
| Tier 1 | B4 | claims | 89 | 271 | 32.8413 |
| Tier 1 | Reports_with_RQ4_Inventory | reports | 117 | 212 | 55.1887 |
| Tier 1 | Reports_with_Active_Crypto_Dependency | reports | 116 | 212 | 54.717 |
| Tier 2 | MULTI_BOUNDARY | claims | 256 | 313 | 81.7891 |
| Tier 2 | SUPPORTED_WITHIN_SCOPE | claims | 260 | 313 | 83.0671 |
| Tier 2 | READY | claims | 287 | 313 | 91.6933 |
| Tier 2 | Strict_Formal | claims | 22 | 313 | 7.02875 |
| Tier 2 | AD | claims | 306 | 313 | 97.7636 |
| Tier 2 | Benchmark_PoC_Deployment | claims | 285 | 313 | 91.0543 |
| Tier 2 | No_Demonstrated_PQC_Migration | claims | 301 | 313 | 96.1661 |
| Tier 2 | B1 | claims | 131 | 313 | 41.853 |
| Tier 2 | B2 | claims | 252 | 313 | 80.5112 |
| Tier 2 | B3 | claims | 260 | 313 | 83.0671 |
| Tier 2 | B4 | claims | 158 | 313 | 50.4792 |
| Tier 2 | Reports_with_RQ4_Inventory | reports | 128 | 230 | 55.6522 |
| Tier 2 | Reports_with_Active_Crypto_Dependency | reports | 112 | 230 | 48.6957 |
| Combined | MULTI_BOUNDARY | claims | 472 | 584 | 80.8219 |
| Combined | SUPPORTED_WITHIN_SCOPE | claims | 482 | 584 | 82.5342 |
| Combined | READY | claims | 530 | 584 | 90.7534 |
| Combined | Strict_Formal | claims | 29 | 584 | 4.96575 |
| Combined | AD | claims | 515 | 584 | 88.1849 |
| Combined | Benchmark_PoC_Deployment | claims | 494 | 584 | 84.589 |
| Combined | No_Demonstrated_PQC_Migration | claims | 560 | 584 | 95.8904 |
| Combined | B1 | claims | 172 | 584 | 29.4521 |
| Combined | B2 | claims | 472 | 584 | 80.8219 |
| Combined | B3 | claims | 491 | 584 | 84.0753 |
| Combined | B4 | claims | 247 | 584 | 42.2945 |
| Combined | Reports_with_RQ4_Inventory | reports | 245 | 442 | 55.4299 |
| Combined | Reports_with_Active_Crypto_Dependency | reports | 228 | 442 | 51.5837 |
