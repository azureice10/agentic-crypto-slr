# Eligibility Criteria and Preprint Rigor Gate (`IC1`–`IC5` & `EC1`–`EC5`)

**Systematic Literature Review Title:**  
*Cryptographic Assurance Gaps in LLM-Based Agentic Systems: A Systematic Literature Review* (release `v3.6.3`; unchanged `v3.5` data baseline)

## 1. Evidence Stream Model (`Stream M`, `Stream A`, `Stream M_AND_A`)
The review employs a two-stream evidence model across the `442` canonical primary reports:
- **Stream M (Mechanisms & Protocols — `107` studies, `24.2%`):** Primary studies proposing, implementing, or formalizing cryptographic, hardware-rooted, or attestation-based defenses for LLM agent operations.
- **Stream A (Boundary Attacks & Failure Analyses — `228` studies, `51.6%`):** Primary empirical studies investigating attacks, exploit demonstrations, or reproducible failure analyses targeting agent boundaries $B_1$–$B_4$.
- **Stream M_AND_A (Hybrid — `107` studies, `24.2%`):** Primary studies providing both an original defense mechanism and an empirical boundary-attack evaluation.

## 2. Inclusion Criteria (`IC1`–`IC5`)

| Code | Criterion Name | Operational Definition & Scope |
| :--- | :--- | :--- |
| **`IC1`** | **Agentic LLM Workflow** | The evaluated system must involve an LLM-based component that does more than return conversational text: it actively selects, coordinates, delegates, or executes actions through external tools, APIs, environment actuators, sub-agents, or persistent memory/state. |
| **`IC2-M`** | **Cryptographic / Hardware Mechanism (Stream M)** | The study proposes, formalizes, implements, or evaluates a concrete cryptographic primitive, protocol, or hardware-rooted mechanism (e.g., digital signatures, TEE remote attestation, capability tokens, zero-knowledge proofs, authenticated data structures, post-quantum algorithms). |
| **`IC2-A`** | **Empirical Boundary Attack (Stream A)** | The study reports an empirical attack, exploit benchmark, vulnerability demonstration, or failure analysis targeting transitions $B_1$–$B_4$ in an agentic workflow (e.g., confused deputy, tool poisoning, tool squatting, MCP hijacking, prompt injection with tool invocation). |
| **`IC3`** | **Architectural Boundary Relevance** | The mechanism or attack operates across at least one well-defined agent boundary: $B_1$ (represented user intent $\rightarrow$ delegation/policy), $B_2$ (delegation/policy $\rightarrow$ concrete agent request), $B_3$ (authorized request $\rightarrow$ actual tool/runtime execution), or $B_4$ (execution $\rightarrow$ verifiable audit evidence). |
| **`IC4`** | **Original Primary Contribution** | The paper presents original primary research (novel protocol, formal security proofs, empirical tool benchmarks, or system implementation), not merely a high-level survey, opinion, editorial, or vision paper. |
| **`IC5`** | **Language, Cutoff & Document Type** | Full text available in English, publicly accessible on or before **15 October 2026 (`2026-10-15T23:59:59Z`)**, published as a peer-reviewed article/proceeding (Tier 1, `n = 212`) or a version-pinned arXiv preprint meeting the preprint rigor gate (Tier 2, `n = 230`). |

## 3. Exclusion Criteria (`EC1`–`EC5` & Subtypes; `n = 166` Full-Text Exclusions)

| Code | Exclusion Category | Full-Text Excluded Count (`n = 166`) | Rationale & Examples |
| :--- | :--- | :---: | :--- |
| **`EC1_NON_AGENTIC`** | **Non-Agentic LLM Systems** | 53 | Studies where the LLM functions purely as a text-in/text-out conversational chatbot, standard text classifier, or static summarizer without tool execution, delegation, or persistent environment interactions. |
| **`EC2_OFFENSIVE_ONLY`** | **Offensive Tools / CTF Solvers** | 3 | Studies using LLMs exclusively as autonomous offensive cybersecurity agents (e.g., autonomous CTF solvers, automated penetration testing bots, exploit generators) without investigating or proposing assurance mechanisms for the agent system itself. |
| **`EC3_CRYPTO_CODEGEN_ONLY`** | **Cryptographic Code Synthesis** | 0 (screened out in Stage 1) | Studies where LLMs are used solely to write cryptographic code, generate Verilog/RTL hardware modules, or optimize homomorphic encryption circuits, rather than securing agentic workflows. |
| **`EC4_INCIDENTAL_APP`** | **Incidental Domain Applications** | 76 | Standard domain applications (e.g., medical recommendation, financial forecasting, robotics planners) or software engineering pipelines that do not evaluate cryptographic/attestation security mechanisms or empirical security attacks. |
| **`EC5_SECONDARY_OR_CONTAINER`** | **Secondary Literature & Containers** | 19 | High-level surveys, literature reviews, tutorials, conference proceedings front-matter/indexes (`@proceedings`), complete books (`@book`), and AI-generated conference podcast summaries (`author = {AI Generated}`). *Note: Background surveys were retained at Stage 1 as `CONTEXT_ONLY` (`n = 78`).* |
| **`LANGUAGE_NOT_ENGLISH`** | **Language Barrier** | 1 | Candidate studies whose full-text report is published in a language other than English. |
| **`EC_RIGOR_1`** | **Preprint Rigor Gate Failure (Subtype 1)** | 9 | Tier 2 arXiv preprints failing both Gate G1 (explicit adversary model with formal/symbolic proof) and Gate G2 (inspectable prototype or verifiable benchmark). |
| **`EC_RIGOR_2`** | **Preprint Rigor Gate Failure (Subtype 2)** | 5 | Tier 2 arXiv preprints with insufficient methodological specification or unverifiable experimental setup. |
