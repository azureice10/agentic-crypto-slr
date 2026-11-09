**Release:** `3.6.3` (3 November 2026); analytical CSV baseline `v3.5`, recorded sign-off 2 November 2026. Screening and arXiv provenance counts are now recalculated from normalized register exports; the complete four-platform raw yield remains reported search history.

# Comprehensive Search Strategy & Identification Protocol (PRISMA-S)

**Systematic Literature Review Title:**

*Cryptographic Assurance Gaps in LLM-Based Agentic Systems: A Systematic Literature Review*

**Methodological Reporting Frameworks:**

* **PRISMA 2020 Statement:** *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* \[14\]

* **PRISMA-S Explanation and Elaboration:** *Reporting Literature Searches in Systematic Reviews* \[15\]

* **PRISMA-P Protocol Guidelines:** *Preferred Reporting Items for Systematic Review and Meta-Analysis Protocols* \[16\]

**Core Operational Parameters:**

* **Execution Date:** 15 October 2026 (all databases and API searches executed on this date)

* **Publication-Version Eligibility Cutoff:** `2026-10-15T23:59:59Z` (inclusive)

* **Language Restriction:** English full text required (no search-time metadata exclusion applied)

* **Information Sources:** Tier 1 Peer-Reviewed Databases (Scopus, IEEE Xplore, ACM Digital Library) + Tier 2 Supplementary Preprint Server (arXiv via official Atom API)

* **Total Raw Yield:** `6,860` query-returned records (`310` Scopus + `256` IEEE Xplore + `2,152` ACM Digital Library + `4,142` arXiv Atom API)

* **Formal Screening Queue:** `926` deduplicated records (`432` Tier 1 peer-reviewed + `494` Tier 2 arXiv preprints)

* **Full-Text Eligibility Queue:** `610` retrieved full-text reports (`0` unretrieved; `166` excluded at full text; `2` linked companion preprints `ARXIV-S-0173` and `ARXIV-S-0403`)

* **Final Included Canonical Reports (`v3.5`):** `442` canonical primary reports (`212` Tier 1 peer-reviewed + `230` rigor-gated Tier 2 arXiv preprints; normalized 1-to-1 to `442` canonical-report clusters `SF-<Source_Record_ID>`)

## 1. Search Objectives & Three-Pillar Architecture

This systematic literature review addresses the security, cryptographic guarantees, and empirical attack surfaces of Large Language Model (LLM) agentic workflows. To ensure comprehensive coverage without combinatorial explosion, the search space was decomposed into **three thematic pillars** across four distinct operational boundaries:

* **Boundary 1 (**$B_1$**):** *Intent to Delegation* (User / Principal $\rightarrow$ Agent Planner)

* **Boundary 2 (**$B_2$**):** *Delegation to Tool Request* (Agent Planner $\rightarrow$ Tool Broker / Sub-agent / MCP Client)

* **Boundary 3 (**$B_3$**):** *Request to Execution* (Tool Broker / MCP Client $\rightarrow$ Tool Provider / MCP Server / Environment)

* **Boundary 4 (**$B_4$**):** *Execution to Audit & Output* (Tool Output / Environment $\rightarrow$ Audit Log / User)

```
flowchart LR
    subgraph P1 ["Pillar 1: Cryptography, Enclaves & PQC"]
        direction TB
        c1["Cryptographic Attestation & Signatures"]
        c2["Hardware Enclaves (TEEs: SGX/TDX/SEV/TrustZone)"]
        c3["Verifiable Computation & ZK-Proofs"]
        c4["Post-Quantum Cryptography (ML-KEM/ML-DSA)"]
    end

    subgraph P2 ["Pillar 2: Delegation & Capability Authorization"]
        direction TB
        d1["Authenticated & Attenuated Delegation"]
        d2["Capability Tokens & Macaroons"]
        d3["Workload Identity (SPIFFE/WIMSE/DIDs)"]
        d4["Token Binding & Proof-of-Possession"]
    end

    subgraph P3 ["Pillar 3: Boundary Attacks & MCP Security"]
        direction TB
        a1["Confused Deputy & Privilege Escalation"]
        a2["Tool / Metadata Poisoning & Squatting"]
        a3["Model Context Protocol (MCP) Exploits"]
        a4["Tool-Output Injection & Cross-Tool Taint"]
    end

    subgraph Boundaries ["Operational Boundaries B1–B4"]
        direction TB
        B1["B1: Intent to Delegation"]
        B2["B2: Delegation to Request"]
        B3["B3: Request to Execution"]
        B4["B4: Execution to Audit"]
    end

    P1 -.-> Boundaries
    P2 -.-> Boundaries
    P3 -.-> Boundaries

```

### Research Questions (RQ1–RQ4) Mapping:

1. **RQ1 — Mechanism & Architecture Landscape:** What cryptographic, hardware-enforced, and capability-based mechanisms have been proposed to secure LLM agentic operations across boundaries $B_1$–$B_4$?

2. **RQ2 — Claim Verification & Assurance Gaps:** What specific security properties do authors claim, under what explicit adversary models, and what methodological limitations (`DG`, `AD`, `UG`, `NG`), trust assumptions, or unproved leaps emerge upon formal/empirical appraisal?

3. **RQ3 — Empirical Performance & Practical Overhead:** What are the computational, latency (`L1`–`L4`), token, and communication costs of integrating cryptographic assurance into autonomous agent loops?

4. **RQ4 — Post-Quantum Vulnerability & Migration:** Which cryptographic functions in agentic architectures depend on classical discrete-log or factoring assumptions, and what post-quantum or hybrid migrations (`STAGE_0`–`STAGE_6`) have been empirically evaluated?

*(Note: Detailed inclusion/exclusion criteria `IC1`–`IC5`, `EC1`–`EC5`, and the Tier 2 preprint rigor gate `G1`/`G2` are documented in companion file `protocol/eligibility_criteria.md`.)*

## 2. Information Sources & Access Modalities

The search was executed simultaneously across four major digital libraries and repositories on **15 October 2026**:

```
flowchart TD
    subgraph Tier1 ["Tier 1: Primary Peer-Reviewed Databases"]
        DB1["Scopus (Elsevier)<br/>Advanced Search: S1, S2, S3<br/><b>310 raw records</b>"]
        DB2["IEEE Xplore Digital Library<br/>Command Search: I1a–I3b<br/><b>256 raw records</b>"]
        DB3["ACM Digital Library<br/>Advanced Search: ACM-S1–S3<br/><b>2,152 raw records</b>"]
    end

    subgraph Tier2 ["Tier 2: Targeted Supplementary Preprints"]
        DB4["arXiv Atom API<br/>export.arxiv.org/api/query<br/>Queries: ARXIV_S1a–S3<br/><b>4,142 raw records</b>"]
    end

    Tier1 --> P1["Raw Peer-Reviewed: 2,718 records"]
    Tier2 --> P2["Raw Preprints: 4,142 records"]
    P1 --> U["Total Raw Search Yield: 6,860 records"]
    P2 --> U

```

### Source Specifications:

1. **Scopus (Elsevier):**

   * *Platform:* Advanced Search Interface (`https://www.scopus.com/search/form.uri?display=advanced`).

   * *Search Fields:* `TITLE-ABS-KEY(...)`.

   * *Container Limit:* `AND NOT DOCTYPE(cr OR bk)` (excluding conference reviews and whole books).

   * *Export Format:* Full CSV (`Export: CSV - All available citation information, abstract, keywords, and funding details`).

2. **IEEE Xplore Digital Library:**

   * *Platform:* IEEE Xplore Command Search (`https://ieeexplore.ieee.org/search/advanced/command`).

   * *Search Fields:* `Search Within: All Metadata`.

   * *Parser Limit Adjustments:* Modular partitioning ($\le 40$ search terms per execution; removal of wildcards within double quotes; automatic plural stemming enabled).

   * *Export Format:* CSV metadata export.

3. **ACM Digital Library:**

   * *Platform:* ACM DL Advanced Search (`https://dl.acm.org/search/advanced`).

   * *Search expression provenance:* Author-supplied Boolean strings; historical UI/proximity settings remain unverified (see acm_arxiv_queries.md).

   * *Export Format:* BibTeX exports (`acm.bib`, `acm(1).bib`, `acm(2).bib`).

   * *Post-Processing:* Deterministic Python filter to remove container `@proceedings`, `@book`, and AI session summaries, enforcing `Title + Abstract + Author Keywords` strict relevance.

4. **arXiv Repository (Targeted Supplementary Grey Literature):**

   * *Platform:* Official arXiv Atom API (`https://export.arxiv.org/api/query`).

   * *Subject Categories:* `cs.CR` (Cryptography and Security), `cs.AI` (Artificial Intelligence), `cs.MA` (Multiagent Systems), `cs.SE` (Software Engineering), `cs.DC` (Distributed, Parallel, and Cluster Computing).

   * *Query Method:* Automated REST pipeline with exponential backoff and rate-limit compliance (`time.sleep(3.5)` between query pages).

   * *Version Handling:* Pinned version recorded for every preprint (`v1`, `v2`, `v3`).

## 3. Exact Search Strings & Database Executions

### 3.1. Scopus Advanced Search Strings (`S1`–`S3`)

#### Query `S1`: Cryptographic Assurance, Hardware Roots of Trust & Post-Quantum Algorithms

* **Execution Date:** `2026-10-15`

* **Raw Yield:** `137` records (`136` unique)

* **Export File:** `export_S1.csv`

* **SHA-256 Checksum:** `28ea4a7861095202586291509d21c8d171c5f22a16beae5e14788d0733140839`

```
TITLE-ABS-KEY(
  ("LLM agent*" OR "agentic AI" OR "agentic LLM*" OR "agentic workflow*" OR
   "large language model agent*" OR "LLM-based agent*" OR "LLM-powered agent*" OR
   "LLM-driven agent*" OR "LLM-based multi-agent*" OR "multi-agent LLM*" OR
   "multiagent LLM*" OR "multi-agent large language model*" OR
   "tool-using LLM*" OR "tool-using agent*" OR "model context protocol" OR
   "agent-to-agent protocol" OR "Agent2Agent" OR "A2A protocol" OR
   (LLM W/3 agent*) OR ("large language model*" W/3 agent*) OR
   ("AI agent*" AND (LLM OR "large language model*")))
  AND
  (cryptograph* OR "digital signature*" OR "dual signature*" OR
   "zero-knowledge" OR "verifiable credential*" OR "verifiable provenance" OR
   "verifiable execution" OR "authenticated data structure*" OR "authenticated log*" OR
   "tamper-evident" OR "audit integrity" OR "execution integrity" OR "proof of execution" OR
   "remote attestation" OR "cryptographic attestation" OR
   "trusted execution environment*" OR "secure enclave*" OR "confidential computing" OR
   "Intel SGX" OR "Intel TDX" OR "AMD SEV*" OR "ARM TrustZone" OR
   "homomorphic encryption" OR "fully homomorphic" OR "attribute-based encryption" OR
   "proxy re-encryption" OR "functional encryption" OR "multiparty computation" OR
   "multi-party computation" OR "garbled circuit*" OR "secret sharing" OR
   "oblivious transfer" OR "Merkle tree*" OR "hash-based signature*" OR
   "post-quantum" OR "quantum-safe" OR "quantum-resilient" OR "quantum-resistant" OR
   "cryptographic agility" OR "ML-KEM" OR "ML-DSA" OR "SLH-DSA" OR "FN-DSA" OR
   "FIPS 203" OR "FIPS 204" OR "FIPS 205" OR
   "CRYSTALS-Kyber" OR "CRYSTALS-Dilithium" OR "SPHINCS+")
) AND NOT DOCTYPE(cr OR bk)

```

#### Query `S2`: Authenticated Delegation, Workload Identity & Capability Tokens

* **Execution Date:** `2026-10-15`

* **Raw Yield:** `70` records (`70` unique, `+46` incremental to `S1`)

* **Export File:** `export_S2.csv`

* **SHA-256 Checksum:** `fa5970f5bce19c673be6707995f342aaa8dcb6aeaea68292d5dc7d98f607079f`

```
TITLE-ABS-KEY(
  ("LLM agent*" OR "agentic AI" OR "agentic LLM*" OR "agentic workflow*" OR
   "large language model agent*" OR "LLM-based agent*" OR "LLM-powered agent*" OR
   "LLM-driven agent*" OR "multi-agent LLM*" OR "tool-using LLM*" OR
   "tool-using agent*" OR "model context protocol" OR
   "agent-to-agent protocol" OR "Agent2Agent" OR "A2A protocol" OR
   (LLM W/3 agent*) OR ("large language model*" W/3 agent*) OR
   ("AI agent*" AND (LLM OR "large language model*")))
  AND
  ("authenticated delegation" OR "secure delegation" OR
   "capability-based" OR "capability token*" OR
   "token binding" OR "credential binding" OR "proof of possession" OR
   "SPIFFE" OR "WIMSE" OR "decentralized identifier*" OR "UMA 2.0" OR "UMA2.0" OR
   ((delegation OR authorization OR "access control") AND
    ("security protocol" OR credential* OR "policy enforcement" OR
     "tool permission*" OR authentication OR "OAuth*" OR "least privilege")))
) AND NOT DOCTYPE(cr OR bk)

```

#### Query `S3`: Boundary Attacks, Tool/MCP Exploits & Runtime Policy Enforcement

* **Execution Date:** `2026-10-15`

* **Raw Yield:** `103` records (`103` unique, `+75` incremental to `S1+S2`)

* **Export File:** `export_S3.csv`

* **SHA-256 Checksum:** `782b3ba62bc60b281fd0e5b71da7a2ee299cc23a91fc76e8728c342766c6c476`

```
TITLE-ABS-KEY(
  (("LLM agent*" OR "agentic AI" OR "agentic LLM*" OR "agentic workflow*" OR
    "large language model agent*" OR "LLM-based agent*" OR "LLM-powered agent*" OR
    "LLM-driven agent*" OR "multi-agent LLM*" OR "tool-using LLM*" OR
    "tool-using agent*" OR "model context protocol" OR
    (LLM W/3 agent*) OR ("large language model*" W/3 agent*) OR
    ("AI agent*" AND (LLM OR "large language model*")))
   AND
   ("confused deputy" OR "tool poisoning" OR "tool hijacking" OR
    "function hijacking" OR "tool squatting" OR "authorization bypass" OR
    "delegation attack" OR "audit tampering" OR "tool-output injection" OR
    ("prompt injection" AND ("tool invocation" OR "tool calling" OR "function calling"))))
  OR
  (("model context protocol" OR "MCP server*" OR "MCP client*" OR
    "MCP tool*" OR "MCP-enabled" OR "MCP-based" OR
    (MCP AND (LLM OR "large language model*" OR "agentic AI" OR "AI agent*" OR
              "tool-calling agent*" OR "tool-using agent*")) OR
    "LLM agent tooling" OR "GenAI multi-agent*")
   AND
   ("function hijacking" OR "tool squatting" OR "tool poisoning" OR
    "confused deputy" OR "authorization bypass" OR "access control" OR
    privilege* OR "runtime policy" OR "verifiable provenance" OR
    "audit integrity" OR "execution integrity" OR "prompt injection" OR
    "security vulnerabilit*"))
) AND NOT DOCTYPE(cr OR bk)

```

* **Consolidated Scopus Yield:** `310` raw rows $\rightarrow$ **`257` unique peer-reviewed studies** (`SCOPUS-S-0001` through `SCOPUS-S-0257`).

* **Consolidated File:** `Scopus_S1_S2_S3_COMBINED_DEDUP.csv`

* **SHA-256 Checksum:** `d6cf515d9b82035277e95a6fac840f782b2dd3822549c17bd8d04ed4498d5d50`

### 3.2. IEEE Xplore Command Search Strings (`I1a`–`I3b`)

Executed under `Search Within: All Metadata` without user-interface facet filters.

#### Query `I1a`: Cryptography, Remote Attestation & Hardware Enclaves (`78` hits)

* **Export File:** `export_I1a.csv`

* **SHA-256 Checksum:** `e77d603d467262dfd9283b14596acb758bc475bdf30bf9e87bba43f510424d7c`

```
("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND (cryptograph* OR "digital signature" OR "dual signature" OR "zero-knowledge" OR "verifiable credential" OR "verifiable provenance" OR "verifiable execution" OR "tamper-evident" OR "audit integrity" OR "execution integrity" OR "remote attestation" OR "cryptographic attestation" OR "trusted execution environment" OR "secure enclave" OR "confidential computing" OR "Intel SGX" OR "Intel TDX" OR "AMD SEV" OR "ARM TrustZone")

```

#### Query `I1b`: Advanced Privacy, Multiparty Computation & Post-Quantum (`43` hits, `+24` incremental)

* **Export File:** `export_I1b.csv`

* **SHA-256 Checksum:** `0ef80198e4d63fe1d39fc2be3b51e8834965dd6c5935062b34f44639e33b9d3b`

```
("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("homomorphic encryption" OR "fully homomorphic" OR "attribute-based encryption" OR "proxy re-encryption" OR "multiparty computation" OR "multi-party computation" OR "secret sharing" OR "Merkle tree" OR "authenticated data structure" OR "authenticated log" OR "post-quantum" OR "quantum-safe" OR "quantum-resilient" OR "quantum-resistant" OR "ML-KEM" OR "ML-DSA" OR "SLH-DSA")

```

#### Query `I2`: Authenticated Delegation, Capabilities & Identity (`55` hits, `+39` incremental)

* **Export File:** `export_I2.csv`

* **SHA-256 Checksum:** `bbf88741539cfd1e24d823e2dd1311d5cad6eabb1b80c21b8699df839c6198b6`

```
("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("authenticated delegation" OR "secure delegation" OR "capability-based" OR "capability token" OR "token binding" OR "credential binding" OR "proof of possession" OR SPIFFE OR WIMSE OR "decentralized identifier" OR "UMA 2.0" OR ((delegation OR authorization OR "access control") AND ("security protocol" OR credential OR "policy enforcement" OR "tool permission" OR authentication OR OAuth)))

```

#### Query `I3a`: Agent Boundary Attacks & Tool Exploits (`22` hits, `+12` incremental)

* **Export File:** `export_I3a.csv`

* **SHA-256 Checksum:** `77531d54c1266b0864b9ed0b587524844439647dce7d9f4f20ac7473f644a6d2`

```
("agentic AI" OR "agentic workflow" OR "LLM agent" OR "tool-using agent" OR "model context protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("confused deputy" OR "tool poisoning" OR "tool hijacking" OR "function hijacking" OR "tool squatting" OR "authorization bypass" OR "delegation attack" OR "audit tampering" OR "tool-output injection" OR ("prompt injection" AND ("tool invocation" OR "tool calling" OR "function calling")))

```

#### Query `I3b`: MCP Security, Runtime Policy & Taint Enforcement (`58` hits, `+33` incremental)

* **Export File:** `export_I3b.csv`

* **SHA-256 Checksum:** `2ff68b3bb96f652c46f928343e022ede138f1e650249f84c58b5aeba2c006dc0`

```
("model context protocol" OR "MCP server" OR "MCP client" OR "MCP tool" OR "MCP-enabled" OR "MCP-based" OR (MCP AND (LLM OR "large language model" OR "agentic AI" OR "AI agent")) OR "LLM agent tooling" OR "GenAI multi-agent") AND ("function hijacking" OR "tool squatting" OR "tool poisoning" OR "confused deputy" OR "authorization bypass" OR "access control" OR privilege OR "runtime policy" OR "verifiable provenance" OR "audit integrity" OR "execution integrity" OR "prompt injection" OR "security vulnerability")

```

* **Consolidated IEEE Yield:** `256` raw records $\rightarrow$ **`186` unique IEEE records** (`IEEE-S-0001` through `IEEE-S-0186`).

* **Cross-Database Deduplication with Scopus:** `101` records overlapped with Scopus; **`+85` incremental unique peer-reviewed studies** contributed to the corpus.

* **Master Scopus + IEEE Combined:** **`342` unique studies** (`Master_Scopus_IEEE_COMBINED_DEDUP.csv`, SHA-256: `8d21acd7bafd805be17263bdccf5b621466078126fa5a1b40ea050be44b9a684`).

### 3.3. ACM Digital Library Queries (`ACM-S1`–`S3`)

**Query availability:** Complete author-supplied Boolean expressions are included in [acm_arxiv_queries.md](acm_arxiv_queries.md). They do not contain the proximity operator asserted in older notes. Original UI field/proximity settings are not recovered, so the strings are documented as supplied expressions rather than a newly verified historical execution log.

Executed via ACM DL Advanced Search and downloaded as BibTeX collections:

* `ACM-S1` (Attestation & Cryptography): `771` raw entries (`acm.bib`)

* `ACM-S2` (Delegation & Authorization): `1,000` raw entries (`acm(1).bib`)

* `ACM-S3` (MCP & Boundary Attacks): `381` raw entries (`acm(2).bib`)

* **Total Raw ACM BibTeX Entries:** **`2,152`** (representing `1,465` unique BibTeX items)

#### Deterministic Container & Relevance Normalization Pipeline:

1. **Container Stripping:** Removed `608` conference proceedings containers (`@proceedings`), `9` books (`@book`), and `7` AI session podcast summaries (`author = {AI Generated}`).

2. **Relevance Enforcement:** The reported post-export Title/Abstract/Keywords relevance filter removed `728` off-topic records. Exact historical UI field/proximity configuration is not recovered; the filter result does not itself establish how the query was parsed.

3. **Cross-Database Matching:** `23` records matched existing Scopus/IEEE records and were unified into existing study records.

4. **Final Verified ACM Yield:** **`113` verified ACM records** (**`+90` incremental unique studies** added to Tier 1 $\rightarrow$ `432` Tier 1 studies in the screening queue).

* **Consolidated File:** `ACM_S1_S2_S3_FILTERED_DEDUP.csv`

* **SHA-256 Checksum:** `1190a1ebca7311607385c94d0c0072237cb8873cab51bfe3b58fff9ff0936eda`

### 3.4. arXiv Atom API Queries (`ARXIV_S1a`–`ARXIV_S3`)

**Query availability:** All four complete `search_query` strings, request configuration, adaptive pagination, and post-retrieval cutoff handling are documented in [acm_arxiv_queries.md](acm_arxiv_queries.md). The strings match the archived source pipeline. Compact query-occurrence and gate-pass registers reproduce recorded counts without redistributing abstracts. This documents the retained retrieval; no live API rerun is claimed.

Executed via the official arXiv REST endpoint (`https://export.arxiv.org/api/query`) targeting computer science categories (`cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC`):

| Query Identifier | Focus Area & Search Logic | Raw Hits | Passing Gate | Superseded by Tier 1 | Incremental Preprints | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **`ARXIV_S1a`** | Cryptographic Assurance, Hardware Enclaves (TEEs) & Verifiable Provenance | 3,814 | 474 | 33 | 441 | 
| **`ARXIV_S1b`** | Multiparty Computation, Advanced Privacy & Post-Quantum Cryptography | 76 | 37 | 0 | 37 | 
| **`ARXIV_S2`** | Authenticated Delegation, Workload Identity & Capability Tokens | 145 | 107 | 6 | 101 | 
| **`ARXIV_S3`** | Boundary Attacks, MCP Exploits, Confused Deputy & Runtime Policy | 107 | 94 | 15 | 79 | 
| **Consolidated** | **Net Unique arXiv Retrieval** | **4,142** | **529** | **35** | **494** | 

#### Rigor & Supersession Gate for arXiv Preprints:

* **Raw Export:** `export_ARXIV_ALL_RAW.csv` (`7,489,802` bytes, SHA-256: `e58f5de0eb711011199e7b38b8200bc27e251e5f304ba1199fba9332fab247cf`).

* **Per-Query Non-Exclusive vs. Consolidated Deduplicated Accounting:** In the table above, the four query rows (`ARXIV_S1a`–`ARXIV_S3`) report *per-query non-exclusive counts* prior to cross-query deduplication (`3,814 + 76 + 145 + 107 = 4,142` raw hits; `474 + 37 + 107 + 94 = 712` per-query hits passing the relevance gate; `33 + 0 + 6 + 15 = 54` per-query hits matching Tier 1; `441 + 37 + 101 + 79 = 658` per-query incremental hits). Across queries `ARXIV_S1a`–`ARXIV_S3`, **`248` raw hits** overlapped across multiple arXiv queries (`4,142 - 248 = 3,894` unique base arXiv IDs), including **`183` multi-query overlaps among gate-passing preprints** (`712 - 183 = 529` net unique preprints passing the relevance gate), **`19` multi-query overlaps among Tier 1-superseded preprints** (`54 - 19 = 35` net unique preprints superseded by Tier 1), and **`164` multi-query overlaps among incremental preprints** (`658 - 164 = 494` net unique Tier 2 preprints advancing to the `926`-study formal screening queue).

* **Strict Title + Abstract Relevance Gate:** `529` preprints passed all thematic entity checks; `3,365` non-agentic / generic AI preprints were eliminated.

* **Peer-Reviewed Supersession:** `35` preprints were matched via normalized DOI and title to formal peer-reviewed publications in Tier 1 (`SUPERSEDED_BY_PEER_REVIEWED`) and linked via `linked_arxiv_id_versioned`, preventing duplicate counting.

* **Net Tier 2 Contribution:** **`+494` incremental version-pinned preprints** (`ARXIV_S1_S2_S3_FILTERED_DEDUP.csv`, SHA-256: `8ba9feeb852347782e1ed721bc12abe52ff0706e273fbdf1d22d9b5588988f7d`).

## 4. Reported Known-Item Sensitivity Check

The four arXiv seed assignments below are verified against the compact occurrence export, with historical reference-number changes resolved by stable arXiv ID. Other seed assignments remain reported search-history metadata because their raw per-query exports are not redistributed.

To validate search sensitivity prior to screening, **10 gold-standard seed publications** representing foundational contributions across all three pillars were checked against the executed retrieval sets:

| Benchmark Seed Paper | Thematic Pillar & Key Contribution | Database & Query Source | Assigned Master ID | Retrieval Status | 
| ----- | ----- | ----- | ----- | ----- | 
| **South et al. \[1\]** | Attenuated delegation & capability tokens in LLM agents | Scopus (`S2`) | `SLR-M-0228` | **RETRIEVED (100%)** | 
| **Kalyanasundaram \[2\]** | Cryptographic verification & policy enforcement | Scopus (`S1; S2`) | `SLR-M-0172` | **RETRIEVED (100%)** | 
| **Llambí-Morillas & Fernández-Fernández \[3\]** | Cryptographically verifiable authorization (CVA) proof of concept | arXiv (`ARXIV_S1a`) | `ARXIV-S-0001` | **RETRIEVED (100%)** | 
| **Syros et al. \[4\]** | SAGA security architecture for governing agentic systems | arXiv (`ARXIV_S1a;ARXIV_S2`) | `ARXIV-S-0160` | **RETRIEVED (100%)** | 
| **Avizheh et al. \[5\]** | MAGIQ: Post-quantum multi-agent governance system | arXiv (`ARXIV_S1a; S1b`) | `ARXIV-S-0057` | **RETRIEVED (100%)** | 
| **Ştefănescu & Aciobăniţei \[6\]** | Cryptographic authorization for autonomous agents | Scopus (`S1; S2`) / IEEE (`I1a; I2`) | `SLR-M-0188` | **RETRIEVED (100%)** | 
| **Grigor et al. \[7\]** | Verifiable agent credentials & secure runtime | Scopus (`S1`) / ACM (`ACM-S1`) | `SLR-M-0330` | **RETRIEVED (100%)** | 
| **Zhang et al. \[8\]** | Homomorphic encryption & privacy-preserving agents | Scopus (`S1`) / IEEE (`I1b`) | `SLR-M-0234` | **RETRIEVED (100%)** | 
| **Sun et al. \[9\]** | Boundary attacks & tool hijacking in multi-agent workflows | Scopus (`S3`) / ACM (`ACM-S3`) | `SLR-M-0204` | **RETRIEVED (100%)** | 
| **Forough et al. \[13\]** | Confidential-computing survey (context) and the separate primary AgenTEE report | arXiv (`ARXIV_S1a`) / ACM (`ACM-S1`) | `ARXIV-S-0004` / `SLR-M-0042` | **RETRIEVED (100%)** | 

## 5. Pre-Screening Normalization & Deduplication Accounting

### Population Reconciliation Formula:

$$
\text{Screening Queue} = N_{\text{raw}} - N_{\text{duplicates}} - N_{\text{containers}} - N_{\text{automated\_relevance}} - N_{\text{superseded\_preprints}}
$$

$$
926 = 6{,}860 - 1{,}182 - 624 - 4{,}093 - 35
$$

### Detailed Deduplication Breakdown:

1. **Duplicate Entries Removed (**$n = 1{,}182$**):**

   * Scopus internal multi-query overlap: `53`

   * IEEE Xplore internal multi-query overlap: `70`

   * IEEE–Scopus cross-database duplicate indexing: `101`

   * ACM DL internal multi-query overlap: `687`

   * ACM–Scopus/IEEE cross-database duplicate indexing: `23`

   * arXiv internal multi-query overlap: `248`

2. **Ineligible Containers & Podcasts Removed (**$n = 624$**):**

   * Conference proceedings containers (`@proceedings`): `608`

   * Complete textbook records (`@book`): `9`

   * AI-generated session podcast summaries (`author = {AI Generated}`): `7`

3. **Automated Title/Abstract Relevance Gate Removals (**$n = 4{,}093$**):**

   * ACM DL off-topic full-text keyword fallbacks: `728`

   * arXiv out-of-scope non-agentic / generic AI papers: `3,365`

4. **Superseded Preprints Linked to Peer-Reviewed Versions (**$n = 35$**):**

   * Linked to corresponding Tier 1 entries via `linked_arxiv_id_versioned`.

5. **Formal Screening Queue Yield:** **`926` unique studies**

   * **Tier 1 (Peer-Reviewed):** `432` studies (`46.65%`)

   * **Tier 2 (Preprints):** `494` studies (`53.35%`)

   * **Master Corpus File:** `Master_SLR_FULL_CORPUS_DEDUP.csv`

   * **SHA-256 Checksum:** `fe9786f7fc40ce3f2e9ab54003f1d7f0e3ea86a315521ca3b9d123b70d18464a`

## 6. Two-Stage Selection & PRISMA 2020 Flow Accounting

### 6.1. Stage 1: Title & Abstract Screening (`N = 926`)

* **`ADVANCE_FULLTEXT`:** `610` reports

* **`EXCLUDE_STAGE1`:** `236` reports

* **`CONTEXT_ONLY`:** `78` reports (background/context surveys retained outside primary synthesis)

* **`LINK_REPORT_VERSION`:** `2` reports (pre-screening version links)

* **Inter-Rater Reliability (IRR):** Observed raw agreement `646 / 926` (`69.76%`); binary Cohen's $\kappa = 0.4446$; five-class $\kappa = 0.4172$.

### 6.2. Stage 2: Full-Text Eligibility & Preprint Rigor Gating (`n = 610`)

* **Full-Text Retrieval:** `610 / 610` (`100%` retrieved; `0` unretrieved).

* **Full-Text Exclusions (`n = 166`):** `EC1_NON_AGENTIC` (`53`), `EC2_OFFENSIVE_ONLY` (`3`), `EC4_INCIDENTAL_APP` (`76`), `EC5_SECONDARY_OR_CONTAINER` (`19`), `LANGUAGE_NOT_ENGLISH` (`1`), `EC_RIGOR_1` (`9`), and `EC_RIGOR_2` (`5`).

* **Companion Preprints Linked (`n = 2`):** `ARXIV-S-0173` (*CapSeal* companion to `SLR-M-0219`) and `ARXIV-S-0403` (*SecureMCP* companion to `SLR-M-0271`).

* **Final Canonical Included Primary Reports (`n = 442`):** `212` Tier 1 peer-reviewed publications (`156` Scopus + `33` IEEE exclusive + `23` ACM exclusive) and `230` rigor-gated Tier 2 arXiv preprints, stratified across **Stream A** (`228` studies, `51.6%`), **Stream M** (`107` studies, `24.2%`), and **Stream M_AND_A** (`107` studies, `24.2%`).

```
flowchart TD
    subgraph Identification ["Identification (PRISMA 2020 & PRISMA-S)"]
        A1["Databases Queried:<br/>Scopus (n = 310)<br/>IEEE Xplore (n = 256)<br/>ACM DL (n = 2,152)"]
        A2["Supplementary Grey Literature:<br/>arXiv Atom API (n = 4,142)"]
        A1 & A2 --> RAW["Total Query-Returned Records<br/><b>N = 6,860 entries</b>"]
        
        RAW --> DEDUP["Records Removed Before Screening (n = 5,934):<br/>• Duplicate entries: 1,182<br/>• Containers & podcasts: 624<br/>• Automated relevance filters: 4,093<br/>• Superseded preprints linked: 35"]
        RAW --> SCREEN_QUEUE["Records Screened (Title/Abstract)<br/><b>N = 926 records</b><br/>(Tier 1: 432; Tier 2: 494)"]
    end

    subgraph Screening ["Screening Phase"]
        SCREEN_QUEUE --> STAGE1_EXC["Records Excluded Stage 1 (n = 316):<br/>• EXCLUDE_STAGE1: 236<br/>• CONTEXT_ONLY: 78<br/>• Pre-screening version links: 2"]
        SCREEN_QUEUE --> SOUGHT["Reports Sought for Retrieval<br/><b>n = 610 reports</b>"]
    end

    subgraph Retrieval ["Full-Text Retrieval"]
        SOUGHT --> RETRIEVED["Reports Assessed for Eligibility<br/><b>n = 610 reports</b><br/>(Reports Not Retrieved = 0)"]
    end

    subgraph Eligibility ["Eligibility & Rigor Appraisal"]
        RETRIEVED --> FT_EXC["Reports Excluded at Full Text (n = 166):<br/>• EC1 Non-Agentic: 53<br/>• EC2 Offensive Only: 3<br/>• EC4 Incidental App: 76<br/>• EC5 Secondary/Container: 19<br/>• Language (Non-English): 1<br/>• Preprint Rigor Failures: 14"]
        RETRIEVED --> COMPANION["Linked Companion Preprints (n = 2):<br/>• CapSeal (ARXIV-S-0173)<br/>• SecureMCP (ARXIV-S-0403)"]
        RETRIEVED --> INCLUDED["Canonical Reports Included<br/><b>N = 442 canonical reports</b><br/>(Tier 1: 212; Tier 2: 230)"]
    end

    subgraph Synthesis ["Stage 3 Extraction, QA Release Gate & v3.5 Final Adjudication"]
        INCLUDED --> STAGE3["Full-Text Extraction & v3.5 Final Adjudication (E01–E09):<br/>• 442 Canonical Reports (406 with READY claims; 442 normalized report clusters)<br/>• 584 Extracted Claims (530 READY [90.8%] + 54 FLAGGED [9.2%])<br/>• 1,111 RQ3 Metric Records (454 time rows -> 399 deduplicated online runtime [362 READY])<br/>• 283 RQ4 Inventory Records (266 active crypto/attestation [224 READY: 222 concrete + 44 Suite NR] + 17 excluded non-crypto [17 READY]; 0 HOLD / 0 Pending)<br/>• 220/220 Adjudication Decisions Enacted & Signed Off (Reviewer 1: Herman Kabetta; Reviewer 2: I Komang Setia Buana; Adjudicator: Raden Budiarto — Bogor, 2 November 2026; 0 HOLD / 0 Pending)"]
    end

```

## 7. Search Export Audit Trail & Cryptographic Checksums

In strict adherence to PRISMA-S guidelines for reproducible search reporting, the following table records the SHA-256 checksums and byte sizes of the primary Stage 1–2 search export artifacts from the primary search execution log (`15 October 2026`). *(Provenance & Redistribution Note: Full publisher metadata/abstract dumps and original XLSX files are not redistributed. Normalized screening decisions and compact arXiv provenance are supplied without abstracts; their SHA-256 digests are preserved below as an immutable audit trail of the upstream identification pipeline that produced `data/studies.csv` [`n = 442`].)*

| Artifact Path | Operational Function | Cryptographic SHA-256 Checksum | File Size (Bytes) | 
| ----- | ----- | ----- | ----- | 
| `export_S1.csv` | Raw Scopus `S1` Query Export (`137` rows) | `28ea4a7861095202586291509d21c8d171c5f22a16beae5e14788d0733140839` | 374,112 | 
| `export_S2.csv` | Raw Scopus `S2` Query Export (`70` rows) | `fa5970f5bce19c673be6707995f342aaa8dcb6aeaea68292d5dc7d98f607079f` | 192,440 | 
| `export_S3.csv` | Raw Scopus `S3` Query Export (`103` rows) | `782b3ba62bc60b281fd0e5b71da7a2ee299cc23a91fc76e8728c342766c6c476` | 278,901 | 
| `Scopus_S1_S2_S3_COMBINED_DEDUP.csv` | Consolidated Scopus Master (`257` unique) | `d6cf515d9b82035277e95a6fac840f782b2dd3822549c17bd8d04ed4498d5d50` | 642,883 | 
| `export_I1a.csv` | Raw IEEE `I1a` Query Export (`78` rows) | `e77d603d467262dfd9283b14596acb758bc475bdf30bf9e87bba43f510424d7c` | 215,604 | 
| `export_I1b.csv` | Raw IEEE `I1b` Query Export (`43` rows) | `0ef80198e4d63fe1d39fc2be3b51e8834965dd6c5935062b34f44639e33b9d3b` | 118,320 | 
| `export_I2.csv` | Raw IEEE `I2` Query Export (`55` rows) | `bbf88741539cfd1e24d823e2dd1311d5cad6eabb1b80c21b8699df839c6198b6` | 151,902 | 
| `export_I3a.csv` | Raw IEEE `I3a` Query Export (`22` rows) | `77531d54c1266b0864b9ed0b587524844439647dce7d9f4f20ac7473f644a6d2` | 60,412 | 
| `export_I3b.csv` | Raw IEEE `I3b` Query Export (`58` rows) | `2ff68b3bb96f652c46f928343e022ede138f1e650249f84c58b5aeba2c006dc0` | 160,204 | 
| `IEEE_I1a_I1b_I2_I3a_I3b_COMBINED_DEDUP.csv` | Consolidated IEEE Master (`186` unique) | `7dc4a0160ab4ebc9f7d31946c55533c3fde93076cd5d71ee80b70b1b6749010a` | 468,110 | 
| `Master_Scopus_IEEE_COMBINED_DEDUP.csv` | Master Scopus + IEEE Combined (`342` unique) | `8d21acd7bafd805be17263bdccf5b621466078126fa5a1b40ea050be44b9a684` | 836,727 | 
| `ACM_S1_S2_S3_FILTERED_DEDUP.csv` | ACM DL Deduplicated & Filtered (`113` unique) | `1190a1ebca7311607385c94d0c0072237cb8873cab51bfe3b58fff9ff0936eda` | 231,776 | 
| `export_ARXIV_ALL_RAW.csv` | Raw arXiv Atom API Harvest (`4,142` rows) | `e58f5de0eb711011199e7b38b8200bc27e251e5f304ba1199fba9332fab247cf` | 7,489,802 | 
| `ARXIV_S1_S2_S3_FILTERED_DEDUP.csv` | arXiv Filtered & Rigor-Gated (`494` unique) | `8ba9feeb852347782e1ed721bc12abe52ff0706e273fbdf1d22d9b5588988f7d` | 1,072,327 | 
| `Master_SLR_FULL_CORPUS_DEDUP.csv` | Unified Master Screening Queue (`926` unique) | `fe9786f7fc40ce3f2e9ab54003f1d7f0e3ea86a315521ca3b9d123b70d18464a` | 1,970,158 | 
| `DAFTAR_ANTREAN_STAGE2_610.csv` | Full-Text Queue Register (`610` reports) | `3a5e8832a514d7a71f021e513812d358be85e50529d2abefda92782b7db5f50f` | 1,289,450 | 


## 8. Recovered screening registers and source qualifications

See [screening_register.md](screening_register.md) and `results/screening_audit.md` for the 926-to-610-to-442 selection reconciliation, full-text exclusions, recomputed agreement, source-workbook hashes, historical Stage 2 extraction states, and the 104 Reviewer 2 date corrections explicitly confirmed as 2026-10-16. Exact source paths and original field values were not changed.
