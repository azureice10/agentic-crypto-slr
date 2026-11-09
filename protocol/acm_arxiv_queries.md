# ACM and arXiv search expressions

Release 3.6.3. Author-supplied expressions received on 3 November 2026. The four arXiv expressions match the archived pipeline constants. The three ACM expressions are supplied Boolean strings; original UI field/proximity settings remain unverified.

## arXiv request and filtering configuration

Endpoint: https://export.arxiv.org/api/query. User-Agent: SLR-Agentic-Crypto-Review/1.0. Inter-request delay: 3.5 seconds. Pagination starts at 0 with max_results=200 and fallback sizes 100 and 50; the offset advances by the number of returned entries. No sortBy/sortOrder parameters are set in the archived code. Timeout: 60 seconds; up to 3 attempts per request size. The publication cutoff 2026-10-15T23:59:59Z is applied after retrieval using published_utc, rather than as an API date clause. Stage 2 separately records version-cutoff checks.

The API queries use five CS categories; the archived relevance gate allows primary/secondary categories cs.CR, cs.AI, cs.MA, cs.SE, cs.DC, cs.CL, cs.LG, cs.NI, and cs.OS. These are different steps and should not be described as identical filters. The source pipeline is archived unchanged beside queries.json; it is supplied for inspection and was not rerun against the live API.

## ARXIV_S1a

Provenance: author note and matching archived pipeline. Execution fidelity: matches archived pipeline constant.

```text
(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND 
(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR all:"model context protocol") AND 
(all:"cryptographic" OR all:"cryptography" OR all:"cryptographically verifiable" OR all:"zero-knowledge" OR 
all:"verifiable credential" OR all:"verifiable credentials" OR all:"verifiable provenance" OR all:"verifiable execution" OR 
all:"tamper-evident" OR all:"remote attestation" OR all:"trusted execution environment" OR all:"confidential computing" OR all:"secure enclave")
```

## ARXIV_S1b

Provenance: author note and matching archived pipeline. Execution fidelity: matches archived pipeline constant.

```text
(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND 
(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR all:"model context protocol") AND 
(all:"homomorphic encryption" OR all:"fully homomorphic" OR all:"attribute-based encryption" OR all:"proxy re-encryption" OR 
all:"multiparty computation" OR all:"multi-party computation" OR all:"post-quantum" OR all:"quantum-safe" OR 
all:"quantum-resilient" OR all:"ML-KEM" OR all:"ML-DSA" OR all:"SLH-DSA")
```

## ARXIV_S2

Provenance: author note and matching archived pipeline. Execution fidelity: matches archived pipeline constant.

```text
(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND 
(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR 
all:"model context protocol" OR all:"Agent2Agent" OR all:"A2A protocol") AND 
(all:"authenticated delegation" OR all:"secure delegation" OR all:"capability-based" OR all:"capability token" OR 
all:"token binding" OR all:"credential binding" OR all:"proof of possession" OR all:"SPIFFE" OR 
all:"decentralized identifier" OR all:"UMA 2.0" OR all:"security architecture" OR all:"zero-trust")
```

## ARXIV_S3

Provenance: author note and matching archived pipeline. Execution fidelity: matches archived pipeline constant.

```text
(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND 
(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"tool-using agent" OR 
all:"model context protocol" OR all:"MCP server" OR all:"MCP servers") AND 
(all:"confused deputy" OR all:"tool poisoning" OR all:"tool hijacking" OR all:"function hijacking" OR 
all:"tool squatting" OR all:"authorization bypass" OR all:"delegation attack" OR all:"audit tampering" OR 
all:"memory exfiltration" OR (all:"model context protocol" AND (all:"prompt injection" OR all:"access control" OR all:"privilege" OR all:"runtime policy")))
```

## ACM-S1

Provenance: author-supplied Boolean expression. Execution fidelity: original UI field/proximity settings not recovered.

```text
("LLM agent" OR "LLM agents" OR "agentic AI" OR "agentic" OR "AI agent" OR "AI agents" OR "model context protocol") 
AND 
("cryptographic" OR "cryptography" OR "zero-knowledge" OR "verifiable credential" OR "verifiable provenance" OR "remote attestation" OR "trusted execution environment" OR "confidential computing" OR "secure enclave" OR "homomorphic encryption" OR "multi-party computation" OR "post-quantum")
```

## ACM-S2

Provenance: author-supplied Boolean expression. Execution fidelity: original UI field/proximity settings not recovered.

```text
("LLM agent" OR "LLM agents" OR "agentic AI" OR "agentic" OR "AI agent" OR "AI agents" OR "model context protocol" OR "Agent2Agent" OR "A2A protocol") 
AND 
("authenticated delegation" OR "secure delegation" OR "capability-based" OR "capability token" OR "token binding" OR "proof of possession" OR "SPIFFE" OR "decentralized identifier" OR "zero-trust" OR "security architecture")
```

## ACM-S3

Provenance: author-supplied Boolean expression. Execution fidelity: original UI field/proximity settings not recovered.

```text
("LLM agent" OR "LLM agents" OR "agentic AI" OR "agentic" OR "tool-using agent" OR "model context protocol" OR "MCP server") 
AND 
("confused deputy" OR "tool poisoning" OR "tool hijacking" OR "function hijacking" OR "tool squatting" OR "authorization bypass" OR "delegation attack" OR "audit tampering" OR "prompt injection" OR "runtime policy")
```

## ACM field and historical-description qualification

The author note describes Title/Abstract/Keywords targeting. The supplied strings themselves do not encode field prefixes or the previously described `"LLM agent"~3` proximity operator. They are now the documented author-supplied expressions. Neither the old proximity claim nor the exact UI field configuration is established by the retained filtered export. No new ACM search was run, and the original reported yields are not asserted to have been reproduced from these strings.

## Seed identity reconciliation

Use arXiv IDs to reconcile source documents whose reference numbers differ: CVA 2607.21325v3 = manuscript [3]; SAGA 2504.21034v2 = [4]; MAGIQ 2605.06933v2 = [5]; confidential-computing survey 2605.03213v2 = [13]. The old [13]/[3]/[4] labels in the archived pipeline and author note are historical labels, not current manuscript reference numbers. The raw occurrence export identifies CVA via ARXIV_S1a, SAGA via ARXIV_S1a and ARXIV_S2, MAGIQ via ARXIV_S1a and ARXIV_S1b, and the survey via ARXIV_S1a.
