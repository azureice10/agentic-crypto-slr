# Search strings appendix

Preserved from manuscript reporting release 3.6.3. Search history and provenance qualifications remain applicable.

### 2.4. Search strings, search limits, and update policy

To document the executed searches under PRISMA-S \[15\], the supplied verbatim Scopus/IEEE search expressions and the available ACM/arXiv query summaries for **15 October 2026** are recorded below:

#### 2.4.1. Scopus Advanced Search (`S1`–`S3`)

* **`S1` (Cryptographic, Hardware-Root & Post-Quantum Assurance — 137 raw rows; 136 unique):**

  TITLE-ABS-KEY(

  ("LLM agent\*" OR "agentic AI" OR "agentic LLM\*" OR "agentic workflow\*" OR

  "large language model agent\*" OR "LLM-based agent\*" OR "LLM-powered agent\*" OR

  "LLM-driven agent\*" OR "LLM-based multi-agent\*" OR "multi-agent LLM\*" OR

  "multiagent LLM\*" OR "multi-agent large language model\*" OR

  "tool-using LLM\*" OR "tool-using agent\*" OR "model context protocol" OR

  "agent-to-agent protocol" OR "Agent2Agent" OR "A2A protocol" OR

  (LLM W/3 agent\*) OR ("large language model\*" W/3 agent\*) OR

  ("AI agent\*" AND (LLM OR "large language model\*")))

  AND

  (cryptograph\* OR "digital signature\*" OR "dual signature\*" OR

  "zero-knowledge" OR "verifiable credential\*" OR "verifiable provenance" OR

  "verifiable execution" OR "authenticated data structure\*" OR "authenticated log\*" OR

  "tamper-evident" OR "audit integrity" OR "execution integrity" OR "proof of execution" OR

  "remote attestation" OR "cryptographic attestation" OR

  "trusted execution environment\*" OR "secure enclave\*" OR "confidential computing" OR

  "Intel SGX" OR "Intel TDX" OR "AMD SEV\*" OR "ARM TrustZone" OR

  "homomorphic encryption" OR "fully homomorphic" OR "attribute-based encryption" OR

  "proxy re-encryption" OR "functional encryption" OR "multiparty computation" OR

  "multi-party computation" OR "garbled circuit\*" OR "secret sharing" OR

  "oblivious transfer" OR "Merkle tree\*" OR "hash-based signature\*" OR

  "post-quantum" OR "quantum-safe" OR "quantum-resilient" OR "quantum-resistant" OR

  "cryptographic agility" OR "ML-KEM" OR "ML-DSA" OR "SLH-DSA" OR "FN-DSA" OR

  "FIPS 203" OR "FIPS 204" OR "FIPS 205" OR

  "CRYSTALS-Kyber" OR "CRYSTALS-Dilithium" OR "SPHINCS+")

  ) AND NOT DOCTYPE(cr OR bk)

* **`S2` (Authenticated Delegation, Identity & Capability Authorization — 70 raw rows; 70 unique):**

  TITLE-ABS-KEY(

  ("LLM agent\*" OR "agentic AI" OR "agentic LLM\*" OR "agentic workflow\*" OR

  "large language model agent\*" OR "LLM-based agent\*" OR "LLM-powered agent\*" OR

  "LLM-driven agent\*" OR "multi-agent LLM\*" OR "tool-using LLM\*" OR

  "tool-using agent\*" OR "model context protocol" OR

  "agent-to-agent protocol" OR "Agent2Agent" OR "A2A protocol" OR

  (LLM W/3 agent\*) OR ("large language model\*" W/3 agent\*) OR

  ("AI agent\*" AND (LLM OR "large language model\*")))

  AND

  ("authenticated delegation" OR "secure delegation" OR

  "capability-based" OR "capability token\*" OR

  "token binding" OR "credential binding" OR "proof of possession" OR

  "SPIFFE" OR "WIMSE" OR "decentralized identifier\*" OR "UMA 2.0" OR "UMA2.0" OR

  ((delegation OR authorization OR "access control") AND

  ```
  ("security protocol" OR credential\* OR "policy enforcement" OR  
  
   "tool permission\*" OR authentication OR "OAuth\*" OR "least privilege")))  
  
  ```

  ) AND NOT DOCTYPE(cr OR bk)

* **`S3` (Boundary Attacks, Tool/MCP Exploits & Runtime Policy Enforcement — 103 raw rows; 103 unique):**

  TITLE-ABS-KEY(

  (("LLM agent\*" OR "agentic AI" OR "agentic LLM\*" OR "agentic workflow\*" OR

  ```
  "large language model agent\*" OR "LLM-based agent\*" OR "LLM-powered agent\*" OR  
  
  "LLM-driven agent\*" OR "multi-agent LLM\*" OR "tool-using LLM\*" OR  
  
  "tool-using agent\*" OR "model context protocol" OR  
  
  (LLM W/3 agent\*) OR ("large language model\*" W/3 agent\*) OR  
  
  ("AI agent\*" AND (LLM OR "large language model\*")))  
  
  ```

  AND

  ("confused deputy" OR "tool poisoning" OR "tool hijacking" OR

  ```
  "function hijacking" OR "tool squatting" OR "authorization bypass" OR  
  
  "delegation attack" OR "audit tampering" OR "tool-output injection" OR  
  
  ("prompt injection" AND ("tool invocation" OR "tool calling" OR "function calling"))))  
  
  ```

  OR

  (("model context protocol" OR "MCP server\*" OR "MCP client\*" OR

  ```
  "MCP tool\*" OR "MCP-enabled" OR "MCP-based" OR  
  
  (MCP AND (LLM OR "large language model\*" OR "agentic AI" OR "AI agent\*" OR  
  
            "tool-calling agent\*" OR "tool-using agent\*")) OR  
  
  "LLM agent tooling" OR "GenAI multi-agent\*")  
  
  ```

  AND

  ("function hijacking" OR "tool squatting" OR "tool poisoning" OR

  ```
  "confused deputy" OR "authorization bypass" OR "access control" OR  
  
  privilege\* OR "runtime policy" OR "verifiable provenance" OR  
  
  "audit integrity" OR "execution integrity" OR "prompt injection" OR  
  
  "security vulnerabilit\*"))  
  
  ```

  ) AND NOT DOCTYPE(cr OR bk)

#### 2.4.2. IEEE Xplore Command Search (`I1a`–`I3b`, `Search Within: All Metadata`)

To comply with IEEE Xplore Command Search parser limits ($\le 40$ search clauses per execution, no wildcards inside quotation marks or `NEAR/3` operands, and automatic plural stemming), the three pillars were executed as five modular queries:

* **`I1a` (78 hits):** `("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND (cryptograph* OR "digital signature" OR "dual signature" OR "zero-knowledge" OR "verifiable credential" OR "verifiable provenance" OR "verifiable execution" OR "tamper-evident" OR "audit integrity" OR "execution integrity" OR "remote attestation" OR "cryptographic attestation" OR "trusted execution environment" OR "secure enclave" OR "confidential computing" OR "Intel SGX" OR "Intel TDX" OR "AMD SEV" OR "ARM TrustZone")`

* **`I1b` (43 hits):** `("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("homomorphic encryption" OR "fully homomorphic" OR "attribute-based encryption" OR "proxy re-encryption" OR "multiparty computation" OR "multi-party computation" OR "secret sharing" OR "Merkle tree" OR "authenticated data structure" OR "authenticated log" OR "post-quantum" OR "quantum-safe" OR "quantum-resilient" OR "quantum-resistant" OR "ML-KEM" OR "ML-DSA" OR "SLH-DSA")`

* **`I2` (55 hits):** `("agentic AI" OR "agentic workflow" OR "LLM agent" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("authenticated delegation" OR "secure delegation" OR "capability-based" OR "capability token" OR "token binding" OR "credential binding" OR "proof of possession" OR SPIFFE OR WIMSE OR "decentralized identifier" OR "UMA 2.0" OR ((delegation OR authorization OR "access control") AND ("security protocol" OR credential OR "policy enforcement" OR "tool permission" OR authentication OR OAuth)))`

* **`I3a` (22 hits):** `("agentic AI" OR "agentic workflow" OR "LLM agent" OR "tool-using agent" OR "model context protocol" OR (LLM NEAR/3 agent) OR ("large language model" NEAR/3 agent) OR ("AI agent" AND "large language model")) AND ("confused deputy" OR "tool poisoning" OR "tool hijacking" OR "function hijacking" OR "tool squatting" OR "authorization bypass" OR "delegation attack" OR "audit tampering" OR "tool-output injection" OR ("prompt injection" AND ("tool invocation" OR "tool calling" OR "function calling")))`

* **`I3b` (58 hits):** `("model context protocol" OR "MCP server" OR "MCP client" OR "MCP tool" OR "MCP-enabled" OR "MCP-based" OR (MCP AND (LLM OR "large language model" OR "agentic AI" OR "AI agent")) OR "LLM agent tooling" OR "GenAI multi-agent") AND ("function hijacking" OR "tool squatting" OR "tool poisoning" OR "confused deputy" OR "authorization bypass" OR "access control" OR privilege OR "runtime policy" OR "verifiable provenance" OR "audit integrity" OR "execution integrity" OR "prompt injection" OR "security vulnerability")`

#### 2.4.3. ACM Digital Library (`ACM-S1`–`S3`) and arXiv Atom API (`ARXIV_S1a`–`S3`)

For **ACM Digital Library**, the three complete Boolean expressions supplied by the authors are recorded in `protocol/acm_arxiv_queries.md`, together with the reported export identifiers `ACM-S1`–`S3`. The author-supplied strings contain no proximity operator or explicit field prefix; the intended Title/Abstract/Keywords targeting is reported, but the original UI configuration is not independently recovered. Earlier wording asserting `"LLM agent"~3` proximity syntax and a specific field-fallback behavior is therefore withdrawn as a confirmed execution setting. The reported normalization of `2,152` raw BibTeX entries (`1,465` unique) removed `608` proceedings, `9` books, `7` generated podcasts, and `728` off-topic records, yielding `113` verified ACM records; that original yield was not rerun from the newly supplied strings.

For **arXiv**, all four supplied `search_query` expressions match the constants in the recovered `arxiv_slr_supplementary_pipeline.py`, archived under `protocol/search_sources/`. The API requests use five CS category terms; the later primary/secondary-category relevance gate allows nine CS categories, as explicitly distinguished in `protocol/acm_arxiv_queries.md`. Pagination starts at `start=0`, initially requests `max_results=200`, falls back to `100` or `50`, and advances by returned-entry count; no sort parameters are set. The pipeline records a `3.5 s` inter-request delay and a `2026-10-15T23:59:59Z` post-retrieval publication-date filter. Compact retained exports reproduce `4,142` query returns, `3,894` base IDs, and `529` gate-passing preprints (`494` new + `35` superseded); version-cutoff assessment remains a separate Stage 2 field. The live API was not rerun.

The reported publication-version cutoff and search-execution date are **15 October 2026**. Complete ACM/arXiv expressions and their provenance are now supplied in `protocol/acm_arxiv_queries.md` and machine-readable `protocol/search_sources/queries.json`. arXiv strings and request settings are corroborated by the archived code and compact occurrence exports. ACM strings are author-supplied; exact historical UI field/proximity settings and a new reproduction of the original ACM yield remain unverified.

