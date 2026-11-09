#!/usr/bin/env python3
"""
========================================================================================
Systematic Literature Review (SLR) - Targeted Supplementary Preprint Search Pipeline
PRISMA 2020: "Identification of studies via other methods (Grey literature / Preprints)"
arXiv API Targeted Supplementary Search & PRISMA-S Audit Engine
========================================================================================
SLR Title: Cryptographic Assurance Gaps in LLM-Based Agentic Systems: A Systematic Literature Review
Eligibility Cutoff Date: 2026-10-15T23:59:59Z (15 October 2026 inclusive)

Architecture:
1. Queries official arXiv Atom API across 4 targeted modular queries (ARXIV_S1a, ARXIV_S1b, ARXIV_S2, ARXIV_S3).
2. Performs mandatory Gold-Standard Seed Verification (SEED_CHECK) for seeds [3], [4], [5], [13].
3. Exports export_ARXIV_ALL_RAW.csv with full provenance.
4. Programmatically filters on Title + Abstract strict gate:
   - Primary/secondary CS category check
   - Explicit LLM/Agentic/MCP/A2A entity term
   - Explicit Pillar term (P1 Crypto/TEE/PQC; P2 Authenticated Delegation; P3 Boundary/MCP)
   - Offensive CTF exclusion
   - Rigor signal classification (FORMAL_PROOF_OR_MODEL, EMPIRICAL_SYSTEM_OR_BENCHMARK, SURVEY_OR_SOK)
5. Enforces Cutoff Date (2026-10-15T23:59:59Z) and captures version-pinned arXiv IDs.
6. Deduplicates against peer-reviewed corpus (342 Scopus+IEEE + 90 ACM = 432 unique):
   - Flags superseded preprints (SUPERSEDED_BY_PEER_REVIEWED) vs NEW_ARXIV_PREPRINT.
7. Exports:
   - ARXIV_S1_S2_S3_FILTERED_DEDUP.csv
   - Master_SLR_FULL_CORPUS_DEDUP.csv (Tier 1: 432 Peer-Reviewed + Tier 2: New arXiv Preprints)
   - PRISMA_S_ARXIV_AND_MASTER_REPORT.md with SHA-256 checksums and PRISMA 2020 flow counts.
========================================================================================
"""

import os
import sys
import re
import time
import shutil
import hashlib
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Any, Optional

import requests
import pandas as pd


# ======================================================================================
# CONFIGURATION & CONSTANTS
# ======================================================================================
SLR_TITLE = "Cryptographic Assurance Gaps in LLM-Based Agentic Systems: A Systematic Literature Review"
CUTOFF_ISO_STR = "2026-10-15T23:59:59Z"
CUTOFF_DATETIME = datetime.fromisoformat(CUTOFF_ISO_STR.replace("Z", "+00:00"))

ARXIV_API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "SLR-Agentic-Crypto-Review/1.0"
RATE_LIMIT_SLEEP = 3.5  # Official arXiv rate limit requirement: 3.0s+ between requests
PAGE_SIZE = 200         # Preferred max results per query page
REQUEST_TIMEOUT = 60    # HTTP timeout in seconds
MAX_RETRIES = 3         # Retries per size candidate

# Input filenames
FILE_MASTER_SCOPUS_IEEE = "Master_Scopus_IEEE_COMBINED_DEDUP.csv"
FILE_MASTER_SCOPUS_IEEE_ALT = "Master_Scopus_IEEE_342_DEDUP.csv"
FILE_ACM_DEDUP = "ACM_S1_S2_S3_FILTERED_DEDUP.csv"

# Output filenames
OUT_RAW_CSV = "export_ARXIV_ALL_RAW.csv"
OUT_FILTERED_CSV = "ARXIV_S1_S2_S3_FILTERED_DEDUP.csv"
OUT_MASTER_CORPUS_CSV = "Master_SLR_FULL_CORPUS_DEDUP.csv"
OUT_REPORT_MD = "PRISMA_S_ARXIV_AND_MASTER_REPORT.md"

# 4 Modular Targeted Queries
QUERIES = {
    "ARXIV_S1a": (
        '(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND '
        '(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR all:"model context protocol") AND '
        '(all:"cryptographic" OR all:"cryptography" OR all:"cryptographically verifiable" OR all:"zero-knowledge" OR '
        'all:"verifiable credential" OR all:"verifiable credentials" OR all:"verifiable provenance" OR all:"verifiable execution" OR '
        'all:"tamper-evident" OR all:"remote attestation" OR all:"trusted execution environment" OR all:"confidential computing" OR all:"secure enclave")'
    ),
    "ARXIV_S1b": (
        '(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND '
        '(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR all:"model context protocol") AND '
        '(all:"homomorphic encryption" OR all:"fully homomorphic" OR all:"attribute-based encryption" OR all:"proxy re-encryption" OR '
        'all:"multiparty computation" OR all:"multi-party computation" OR all:"post-quantum" OR all:"quantum-safe" OR '
        'all:"quantum-resilient" OR all:"ML-KEM" OR all:"ML-DSA" OR all:"SLH-DSA")'
    ),
    "ARXIV_S2": (
        '(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND '
        '(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"AI agent" OR all:"AI agents" OR '
        'all:"model context protocol" OR all:"Agent2Agent" OR all:"A2A protocol") AND '
        '(all:"authenticated delegation" OR all:"secure delegation" OR all:"capability-based" OR all:"capability token" OR '
        'all:"token binding" OR all:"credential binding" OR all:"proof of possession" OR all:"SPIFFE" OR '
        'all:"decentralized identifier" OR all:"UMA 2.0" OR all:"security architecture" OR all:"zero-trust")'
    ),
    "ARXIV_S3": (
        '(cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC) AND '
        '(all:"LLM agent" OR all:"LLM agents" OR all:"agentic AI" OR all:"agentic" OR all:"tool-using agent" OR '
        'all:"model context protocol" OR all:"MCP server" OR all:"MCP servers") AND '
        '(all:"confused deputy" OR all:"tool poisoning" OR all:"tool hijacking" OR all:"function hijacking" OR '
        'all:"tool squatting" OR all:"authorization bypass" OR all:"delegation attack" OR all:"audit tampering" OR '
        'all:"memory exfiltration" OR (all:"model context protocol" AND (all:"prompt injection" OR all:"access control" OR all:"privilege" OR all:"runtime policy")))'
    )
}

# Gold-Standard Seed Preprints
SEED_PREPRINTS = {
    "2607.21325": {
        "seed_ref": "[13]",
        "expected_title": "Cryptographically verifiable authorization for autonomous AI agents: a falsifiable hypothesis and proof of concept",
        "thematic_focus": "P1/P2 Verifiable Authorization & Cryptographic Delegation PoC"
    },
    "2504.21034": {
        "seed_ref": "[3]",
        "expected_title": "SAGA: A Security Architecture for Governing AI Agentic Systems",
        "thematic_focus": "P2 Security Architecture & Governance"
    },
    "2605.06933": {
        "seed_ref": "[5]",
        "expected_title": "MAGIQ: A Post-Quantum Multi-Agentic AI Governance System with Provable Security",
        "thematic_focus": "P1 Post-Quantum Multi-Agent Governance & Provable Security"
    },
    "2605.03213": {
        "seed_ref": "[4]",
        "expected_title": "When Agents Handle Secrets: A Survey of Confidential Computing for Agentic AI",
        "thematic_focus": "P1 Confidential Computing & Hardware TEE Survey"
    }
}

ALLOWED_CATEGORIES = {
    'cs.CR', 'cs.AI', 'cs.MA', 'cs.SE', 'cs.DC', 'cs.CL', 'cs.LG', 'cs.NI', 'cs.OS'
}

# XML Namespaces
XML_NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
    'arxiv': 'http://arxiv.org/schemas/atom'
}


# ======================================================================================
# REGEX DEFINITIONS FOR STRICT RELEVANCE GATE
# ======================================================================================

# Entity match: Modern LLM / Agentic / MCP / A2A entity
ENTITY_REGEX = re.compile(
    r'\b('
    r'llm\s+agents?|llm-based\s+agents?|llm-driven\s+agents?|'
    r'large\s+language\s+model\s+(?:based\s+|driven\s+)?agents?|'
    r'agentic(?:\s+ai|\s+systems?|\s+workflows?|\s+frameworks?)?|'
    r'ai\s+agents?|autonomous\s+agents?|'
    r'multi-?agents?(?:\s+systems?|\s+collaboration|\s+workflows?)?|'
    r'tool-using\s+agents?|tool-augmented\s+agents?|'
    r'coding\s+agents?|software\s+agents?|'
    r'model\s+context\s+protocol|mcp\s+servers?|mcp\s+clients?|'
    r'agent2agent|a2a\s+protocol'
    r')\b',
    re.IGNORECASE
)

# Alternative compound check: LLM/Foundation model co-occurring with agent
LLM_CO_OCCUR_REGEX = re.compile(
    r'\b(llms?|large\s+language\s+models?|foundation\s+models?)\b',
    re.IGNORECASE
)
AGENT_CO_OCCUR_REGEX = re.compile(
    r'\b(agents?|multi-?agent)\b',
    re.IGNORECASE
)

# Pillar 1: Cryptographic Assurance, Hardware Enclaves/TEE, Provenance, PQC
P1_REGEX = re.compile(
    r'\b('
    r'cryptograph(?:ic|ically|y)|zero-knowledge|zk-snarks?|zk-starks?|zksnarks?|zkstarks?|'
    r'verifiable\s+(?:credentials?|provenance|execution|comput(?:e|ation))|'
    r'tamper-evident|tamper-proof|remote\s+attestation|'
    r'trusted\s+execution\s+environments?|tee|tees|'
    r'confidential\s+computing|secure\s+enclaves?|'
    r'intel\s+sgx|sgx|arm\s+trustzone|trustzone|nitro\s+enclaves?|sev-snp|'
    r'(?:fully\s+)?homomorphic\s+encryption|fhe|tfhe|ckks|bgv|bfv|'
    r'attribute-based\s+encryption|abe|proxy\s+re-encryption|'
    r'(?:secure\s+)?multi-?party\s+computation|mpc|smc|'
    r'post-quantum|quantum-safe|quantum-resilient|pqc|'
    r'ml-kem|ml-dsa|slh-dsa|lattice-based'
    r')\b',
    re.IGNORECASE
)

# Pillar 2: Authenticated Delegation, Identity & Capability Authorization
P2_REGEX = re.compile(
    r'\b('
    r'authenticated\s+delegation|secure\s+delegation|delegation\s+tokens?|delegation\s+chains?|'
    r'capability-based(?:\s+authorization)?|capability\s+tokens?|'
    r'token\s+binding|credential\s+binding|proof\s+of\s+possession|dpop|'
    r'macaroons|biscuit\s+tokens?|spiffe|spire|decentralized\s+identifiers?|did|'
    r'uma\s+2\.0|user-managed\s+access|zero-trust|zero\s+trust|security\s+architecture'
    r')\b',
    re.IGNORECASE
)

# Pillar 3: Boundary Attacks, Tool/MCP Exploits & Runtime Policy
P3_REGEX = re.compile(
    r'\b('
    r'confused\s+deputy|tool\s+poisoning|tool\s+hijacking|function\s+hijacking|'
    r'tool\s+squatting|authorization\s+bypass|delegation\s+attacks?|'
    r'audit\s+tampering|memory\s+exfiltration'
    r')\b',
    re.IGNORECASE
)

# MCP Security & Policy Boundary
MCP_SECURITY_REGEX = re.compile(
    r'model\s+context\s+protocol.*?(?:prompt\s+injection|access\s+control|privilege|runtime\s+policy|vulnerabilit|attack|exploit|security|boundary)',
    re.IGNORECASE | re.DOTALL
)

# CTF / Offensive Exclusion Regex (pure offensive/vulnerability solver without agent assurance)
CTF_EXCLUDE_REGEX = re.compile(
    r'\b(capture\s+the\s+flag|ctf\s+challenges?|automated\s+program\s+repair)\b',
    re.IGNORECASE
)

# Rigor Classification Regexes
RIGOR_FORMAL_REGEX = re.compile(
    r'\b(formal\s+verification|provable\s+security|theorems?|tla\+|lean|coq|cryptoverif|tamarin|security\s+proof|adversary\s+model|threat\s+model)\b',
    re.IGNORECASE
)
RIGOR_EMPIRICAL_REGEX = re.compile(
    r'\b(implementation|prototype|benchmark|latency|overhead|evaluation|open-source|github|testbed|experiments?)\b',
    re.IGNORECASE
)
RIGOR_SURVEY_REGEX = re.compile(
    r'\b(survey|systematic\s+literature\s+review|sok|taxonomy|systematization\s+of\s+knowledge)\b',
    re.IGNORECASE
)


# ======================================================================================
# HELPER FUNCTIONS: NORMALIZATION & CHECKSUMS
# ======================================================================================

def compute_sha256(filepath: str) -> str:
    """Computes the SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def normalize_title(title: Any) -> str:
    """Normalizes title: lowercase alphanumeric only, stripping LaTeX math and brackets."""
    if not title or pd.isna(title):
        return ""
    t = str(title)
    t = re.sub(r'\$.*?\$', '', t)  # strip inline math
    t = re.sub(r'[\{\}\[\]\(\)\<\>]', '', t)  # strip brackets
    t = re.sub(r'[^a-z0-9]', '', t.lower())
    return t


def normalize_doi(doi: Any) -> str:
    """Normalizes DOI: lowercase, strips https://doi.org/, doi:, and trailing slashes."""
    if not doi or pd.isna(doi):
        return ""
    d = str(doi).strip().lower()
    d = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', d)
    d = re.sub(r'^doi:\s*', '', d)
    return d.strip('/')


def extract_arxiv_id_parts(arxiv_raw_id: str) -> Tuple[str, str]:
    """
    Extracts base ID and versioned ID from arXiv identifier or URL.
    Example: 'http://arxiv.org/abs/2607.21325v3' -> ('2607.21325', '2607.21325v3')
    """
    clean_id = arxiv_raw_id.strip()
    if '/abs/' in clean_id:
        clean_id = clean_id.split('/abs/')[-1]
    elif '/pdf/' in clean_id:
        clean_id = clean_id.split('/pdf/')[-1].replace('.pdf', '')
    
    # Check for version suffix e.g. v1, v2, v3
    v_match = re.search(r'^(.*?)(v\d+)$', clean_id)
    if v_match:
        base_id = v_match.group(1)
        versioned_id = clean_id
    else:
        base_id = clean_id
        versioned_id = clean_id
    return base_id, versioned_id


def classify_preprint_rigor(text: str) -> str:
    """Classifies abstract into rigor signal categories."""
    signals = []
    if RIGOR_FORMAL_REGEX.search(text):
        signals.append("FORMAL_PROOF_OR_MODEL")
    if RIGOR_EMPIRICAL_REGEX.search(text):
        signals.append("EMPIRICAL_SYSTEM_OR_BENCHMARK")
    if RIGOR_SURVEY_REGEX.search(text):
        signals.append("SURVEY_OR_SOK")
    return "; ".join(signals) if signals else "UNCLASSIFIED"


# ======================================================================================
# API RETRIEVAL CLIENT
# ======================================================================================

class ArxivApiClient:
    """Client for querying arXiv Atom API respecting rate limits and adaptive page sizing."""

    def __init__(self, user_agent: str = USER_AGENT, rate_limit_sleep: float = RATE_LIMIT_SLEEP):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.rate_limit_sleep = rate_limit_sleep

    def fetch_url(self, params: Dict[str, Any]) -> str:
        """Fetches XML response with exponential backoff retry."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(ARXIV_API_URL, params=params, timeout=REQUEST_TIMEOUT)
                if resp.status_code == 500:
                    raise requests.HTTPError(f"500 Server Error at offset {params.get('start')} with max_results={params.get('max_results')}", response=resp)
                resp.raise_for_status()
                return resp.text
            except requests.HTTPError as he:
                if he.response is not None and he.response.status_code == 500:
                    raise  # Fast re-raise 500 to let adaptive sizing handle it
                wait_sec = attempt * 4.0
                print(f"    [WARN] Request attempt {attempt} failed: {he}. Retrying in {wait_sec:.1f}s...")
                time.sleep(wait_sec)
            except Exception as e:
                wait_sec = attempt * 4.0
                print(f"    [WARN] Request attempt {attempt} failed: {e}. Retrying in {wait_sec:.1f}s...")
                time.sleep(wait_sec)
        raise RuntimeError(f"Failed to fetch from arXiv API after {MAX_RETRIES} attempts with params: {params}")

    def parse_entry(self, entry: ET.Element, query_source: str, row_idx: int) -> Dict[str, Any]:
        """Parses an Atom entry into a standardized raw dictionary."""
        id_elem = entry.find('atom:id', XML_NS)
        raw_id_str = id_elem.text.strip() if id_elem is not None else ""
        base_id, versioned_id = extract_arxiv_id_parts(raw_id_str)

        title_elem = entry.find('atom:title', XML_NS)
        title = " ".join(title_elem.text.split()) if title_elem is not None and title_elem.text else ""

        summary_elem = entry.find('atom:summary', XML_NS)
        abstract = " ".join(summary_elem.text.split()) if summary_elem is not None and summary_elem.text else ""

        pub_elem = entry.find('atom:published', XML_NS)
        published_utc = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""

        upd_elem = entry.find('atom:updated', XML_NS)
        updated_utc = upd_elem.text.strip() if upd_elem is not None and upd_elem.text else ""

        # Primary category
        prim_cat_elem = entry.find('arxiv:primary_category', XML_NS)
        primary_category = prim_cat_elem.attrib.get('term', '') if prim_cat_elem is not None else ""

        # All categories
        all_cats = [c.attrib.get('term', '') for c in entry.findall('atom:category', XML_NS)]
        all_categories = "; ".join([c for c in all_cats if c])

        # Authors
        authors_list = []
        for author in entry.findall('atom:author', XML_NS):
            name_elem = author.find('atom:name', XML_NS)
            if name_elem is not None and name_elem.text:
                authors_list.append(name_elem.text.strip())
        authors = "; ".join(authors_list)

        # DOI
        doi_elem = entry.find('arxiv:doi', XML_NS)
        doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else ""

        # Journal Ref
        j_elem = entry.find('arxiv:journal_ref', XML_NS)
        journal_ref = j_elem.text.strip() if j_elem is not None and j_elem.text else ""

        # Comment
        comm_elem = entry.find('arxiv:comment', XML_NS)
        comment = comm_elem.text.strip() if comm_elem is not None and comm_elem.text else ""

        # Links (alternate, pdf)
        abs_url = f"https://arxiv.org/abs/{versioned_id}"
        pdf_url = f"https://arxiv.org/pdf/{versioned_id}"
        for link in entry.findall('atom:link', XML_NS):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib.get('href', pdf_url)
            elif link.attrib.get('rel') == 'alternate':
                abs_url = link.attrib.get('href', abs_url)

        return {
            "query_source": query_source,
            "query_row_idx": row_idx,
            "arxiv_id_base": base_id,
            "arxiv_id_versioned": versioned_id,
            "arxiv_url": abs_url,
            "pdf_url": pdf_url,
            "title": title,
            "authors": authors,
            "published_utc": published_utc,
            "updated_utc": updated_utc,
            "primary_category": primary_category,
            "all_categories": all_categories,
            "doi": doi,
            "journal_ref": journal_ref,
            "comment": comment,
            "abstract": abstract
        }

    def execute_query(self, query_name: str, query_str: str) -> List[Dict[str, Any]]:
        """Paginates an arXiv search query until exhausted with adaptive page sizing."""
        print(f"\n[QUERY] Executing {query_name}...")
        start = 0
        total_results: Optional[int] = None
        records: List[Dict[str, Any]] = []
        current_page_size = PAGE_SIZE

        while True:
            success = False
            xml_text = ""
            actual_size = current_page_size

            # Try candidate page sizes starting from current_page_size down to 100, then 50
            size_candidates = [current_page_size]
            for fallback in [100, 50]:
                if fallback < current_page_size and fallback not in size_candidates:
                    size_candidates.append(fallback)

            for size_cand in size_candidates:
                params = {
                    "search_query": query_str,
                    "start": start,
                    "max_results": size_cand
                }
                try:
                    xml_text = self.fetch_url(params)
                    actual_size = size_cand
                    success = True
                    if size_cand < current_page_size:
                        print(f"  [{query_name}] Adapted page size to {size_cand} at start={start} to overcome arXiv backend memory limits.")
                        current_page_size = size_cand
                    break
                except Exception as e:
                    print(f"  [{query_name}] Page size {size_cand} returned error at start={start}: {e}. Trying fallback size...")
                    time.sleep(2.0)
                    continue

            if not success:
                raise RuntimeError(f"Failed to retrieve entries for {query_name} at start={start}")

            root = ET.fromstring(xml_text)
            if total_results is None:
                tot_elem = root.find('opensearch:totalResults', XML_NS)
                total_results = int(tot_elem.text) if tot_elem is not None and tot_elem.text else 0
                print(f"  [{query_name}] arXiv reported totalResults = {total_results}")

            entries = root.findall('atom:entry', XML_NS)
            if not entries:
                print(f"  [{query_name}] No more entries returned at start={start}. Query complete.")
                break

            for i, entry in enumerate(entries):
                row_idx = start + i + 1
                rec = self.parse_entry(entry, query_name, row_idx)
                records.append(rec)

            print(f"  [{query_name}] Page retrieved: {len(entries)} items (start={start}, max_results={actual_size}, collected={len(records)}/{total_results})")
            start += len(entries)

            if start >= total_results:
                print(f"  [{query_name}] Successfully reached totalResults ({len(records)}/{total_results}).")
                break

            # Respect rate limit between pagination requests
            time.sleep(self.rate_limit_sleep)

        # Rate limit sleep before next query
        time.sleep(self.rate_limit_sleep)
        return records

    def fetch_by_id_list(self, id_list: List[str], query_source: str = "SEED_CHECK") -> List[Dict[str, Any]]:
        """Fetches preprints directly by ID list."""
        print(f"\n[SEED_FETCH] Querying specific ID list: {id_list}...")
        params = {
            "id_list": ",".join(id_list),
            "start": 0,
            "max_results": len(id_list)
        }
        xml_text = self.fetch_url(params)
        root = ET.fromstring(xml_text)
        entries = root.findall('atom:entry', XML_NS)
        records = []
        for i, entry in enumerate(entries):
            rec = self.parse_entry(entry, query_source, i + 1)
            records.append(rec)
        print(f"  [SEED_FETCH] Successfully retrieved {len(records)} entries for ID list.")
        time.sleep(self.rate_limit_sleep)
        return records


# ======================================================================================
# CORE SLR PIPELINE CLASS
# ======================================================================================

class ArxivSLRSupplementaryPipeline:
    """End-to-end SLR supplementary search, gate filtering, and deduplication engine."""

    def __init__(self):
        self.client = ArxivApiClient()
        self.raw_records: List[Dict[str, Any]] = []
        self.query_counts: Dict[str, int] = {}
        self.seed_retrieval_status: Dict[str, Dict[str, Any]] = {}
        self.peer_reviewed_df: Optional[pd.DataFrame] = None
        self.master_scopus_ieee_df: Optional[pd.DataFrame] = None
        self.acm_df: Optional[pd.DataFrame] = None

    def load_peer_reviewed_corpus(self):
        """Loads and consolidates peer-reviewed corpus (Scopus + IEEE Xplore + ACM DL)."""
        print("\n" + "="*80)
        print("STAGE 1: Loading Peer-Reviewed Corpus for Cross-Database Deduplication")
        print("="*80)

        master_path = FILE_MASTER_SCOPUS_IEEE
        if not os.path.exists(master_path):
            if os.path.exists(FILE_MASTER_SCOPUS_IEEE_ALT):
                print(f"[INFO] '{FILE_MASTER_SCOPUS_IEEE}' not found; creating alias from '{FILE_MASTER_SCOPUS_IEEE_ALT}'...")
                shutil.copy(FILE_MASTER_SCOPUS_IEEE_ALT, FILE_MASTER_SCOPUS_IEEE)
                master_path = FILE_MASTER_SCOPUS_IEEE
            else:
                raise FileNotFoundError(f"Neither '{FILE_MASTER_SCOPUS_IEEE}' nor '{FILE_MASTER_SCOPUS_IEEE_ALT}' was found!")

        self.master_scopus_ieee_df = pd.read_csv(master_path)
        print(f"[LOAD] Loaded Scopus + IEEE Master: {len(self.master_scopus_ieee_df)} records from '{master_path}'")

        if not os.path.exists(FILE_ACM_DEDUP):
            raise FileNotFoundError(f"ACM deduplicated corpus '{FILE_ACM_DEDUP}' not found!")

        self.acm_df = pd.read_csv(FILE_ACM_DEDUP)
        print(f"[LOAD] Loaded ACM Corpus: {len(self.acm_df)} total records from '{FILE_ACM_DEDUP}'")

        acm_new = self.acm_df[self.acm_df['cross_db_status'] == 'NEW_ACM_ONLY']
        print(f"[LOAD] ACM Incremental Peer-Reviewed records (NEW_ACM_ONLY): {len(acm_new)}")

        total_peer_reviewed_unique = len(self.master_scopus_ieee_df) + len(acm_new)
        print(f"[SUMMARY] Total Peer-Reviewed Unique Corpus (Tier 1): {total_peer_reviewed_unique} records (342 Scopus/IEEE + 90 ACM)")

    def execute_arxiv_searches(self):
        """Executes the 4 modular queries and verifies gold-standard seeds."""
        print("\n" + "="*80)
        print("STAGE 2: Executing Targeted Modular arXiv API Queries")
        print("="*80)

        for q_name, q_str in QUERIES.items():
            records = self.client.execute_query(q_name, q_str)
            self.query_counts[q_name] = len(records)
            self.raw_records.extend(records)

        print(f"\n[INFO] Total raw rows accumulated from 4 queries: {len(self.raw_records)}")

        # Mandatory Gold-Standard Seed Verification (SEED_CHECK)
        print("\n" + "="*80)
        print("STAGE 3: Mandatory Gold-Standard Seed Verification (SEED_CHECK)")
        print("="*80)

        retrieved_base_ids = {r["arxiv_id_base"] for r in self.raw_records}
        missing_seeds = [s_id for s_id in SEED_PREPRINTS if s_id not in retrieved_base_ids]

        if missing_seeds:
            print(f"[WARN] {len(missing_seeds)} seed(s) missed by pagination: {missing_seeds}. Fetching via id_list...")
            seed_records = self.client.fetch_by_id_list(missing_seeds, query_source="SEED_CHECK")
            self.raw_records.extend(seed_records)
            self.query_counts["SEED_CHECK"] = len(seed_records)
        else:
            print("[SUCCESS] All 4 Gold-Standard seed preprints were naturally retrieved by queries!")
            self.query_counts["SEED_CHECK"] = 0

        # Export export_ARXIV_ALL_RAW.csv
        raw_df = pd.DataFrame(self.raw_records)
        raw_df.to_csv(OUT_RAW_CSV, index=False)
        print(f"[EXPORT] Wrote {len(raw_df)} raw records to '{OUT_RAW_CSV}'")

    def internal_deduplication_and_filtering(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Deduplicates internally by arxiv_id_base and applies strict Title + Abstract gate.
        """
        print("\n" + "="*80)
        print("STAGE 4: Internal Deduplication & Strict Title + Abstract Relevance Gate")
        print("="*80)

        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for r in self.raw_records:
            base_id = r["arxiv_id_base"]
            grouped.setdefault(base_id, []).append(r)

        print(f"[INTERNAL_DEDUP] Grouped {len(self.raw_records)} raw records into {len(grouped)} unique preprints.")

        consolidated_unique: List[Dict[str, Any]] = []
        for base_id, group in grouped.items():
            first = group[0].copy()
            queries = sorted(list({g["query_source"] for g in group}))
            first["search_queries"] = "; ".join(queries)
            first["query_count"] = len(queries)
            first["raw_occurrence_count"] = len(group)
            provenance_list = [f"{g['query_source']}:row_{g['query_row_idx']}" for g in group]
            first["source_row_provenance"] = "; ".join(provenance_list)
            consolidated_unique.append(first)

        # Programmatic Gate Filtering
        passed_records: List[Dict[str, Any]] = []
        filtered_records: List[Dict[str, Any]] = []

        for rec in consolidated_unique:
            title = rec["title"]
            abstract = rec["abstract"]
            text = f"{title} {abstract}"
            all_cats_set = {c.strip() for c in rec["all_categories"].split(";") if c.strip()}
            prim_cat = rec["primary_category"]
            if prim_cat:
                all_cats_set.add(prim_cat)

            # 1. Category Gate
            cat_ok = bool(all_cats_set & ALLOWED_CATEGORIES)

            # 2. Modern LLM / Agentic / MCP / A2A Entity Gate
            entity_direct = bool(ENTITY_REGEX.search(text))
            entity_co_occur = bool(LLM_CO_OCCUR_REGEX.search(text) and AGENT_CO_OCCUR_REGEX.search(text))
            entity_ok = entity_direct or entity_co_occur

            # 3. Security / Cryptographic Pillar Gate
            p1_match = bool(P1_REGEX.search(text))
            p2_match = bool(P2_REGEX.search(text))
            p3_match = bool(P3_REGEX.search(text) or MCP_SECURITY_REGEX.search(text))
            pillar_ok = p1_match or p2_match or p3_match

            matched_pillars = []
            if p1_match: matched_pillars.append("P1")
            if p2_match: matched_pillars.append("P2")
            if p3_match: matched_pillars.append("P3")
            rec["matched_pillars"] = "; ".join(matched_pillars) if matched_pillars else "NONE"

            # 4. CTF / Offensive Exclusion Gate
            ctf_bad = bool(CTF_EXCLUDE_REGEX.search(text)) and not (p1_match or p2_match)

            # 5. Cutoff Gate
            pub_utc_str = rec["published_utc"]
            is_post_cutoff = False
            if pub_utc_str:
                pub_dt = datetime.fromisoformat(pub_utc_str.replace("Z", "+00:00"))
                if pub_dt > CUTOFF_DATETIME:
                    is_post_cutoff = True
            rec["cutoff_eligibility_status"] = "POST_CUTOFF" if is_post_cutoff else "ELIGIBLE_PRE_CUTOFF"

            # Rigor Signal Classification
            rigor_sig = classify_preprint_rigor(abstract)
            rec["preprint_rigor_signal"] = rigor_sig

            filter_pass = cat_ok and entity_ok and pillar_ok and (not ctf_bad) and (not is_post_cutoff)

            if filter_pass:
                rec["screening_status"] = "UNSCREENED"
                passed_records.append(rec)
            else:
                reasons = []
                if not cat_ok: reasons.append("CS_CATEGORY_MISMATCH")
                if not entity_ok: reasons.append("NO_AGENTIC_ENTITY")
                if not pillar_ok: reasons.append("NO_SECURITY_PILLAR")
                if ctf_bad: reasons.append("CTF_OFFENSIVE_EXCLUSION")
                if is_post_cutoff: reasons.append("POST_CUTOFF_DATE")
                rec["filter_rejection_reasons"] = "; ".join(reasons)
                filtered_records.append(rec)

        print(f"[GATE_RESULTS] Total unique preprints evaluated: {len(consolidated_unique)}")
        print(f"[GATE_RESULTS] Passed Strict Title + Abstract Gate: {len(passed_records)}")
        print(f"[GATE_RESULTS] Filtered out by Gate: {len(filtered_records)}")

        passed_df = pd.DataFrame(passed_records)
        filtered_df = pd.DataFrame(filtered_records)
        return passed_df, filtered_df

    def cross_database_deduplication(self, passed_df: pd.DataFrame) -> pd.DataFrame:
        """
        Deduplicates passed arXiv records against the 432 unique peer-reviewed records.
        """
        print("\n" + "="*80)
        print("STAGE 5: Cross-Database Deduplication Against Peer-Reviewed Corpus (432 Unique)")
        print("="*80)

        master_doi_map: Dict[str, str] = {}
        master_title_map: Dict[str, str] = {}
        acm_doi_map: Dict[str, str] = {}
        acm_title_map: Dict[str, str] = {}

        # Master Scopus + IEEE
        for _, row in self.master_scopus_ieee_df.iterrows():
            m_id = str(row["master_id"])
            doi_norm = normalize_doi(row.get("DOI"))
            if doi_norm:
                master_doi_map[doi_norm] = m_id
            title_norm = normalize_title(row.get("Title"))
            if title_norm:
                master_title_map[title_norm] = m_id

        # ACM DL (NEW_ACM_ONLY)
        acm_new = self.acm_df[self.acm_df["cross_db_status"] == "NEW_ACM_ONLY"]
        for _, row in acm_new.iterrows():
            a_id = str(row["acm_consolidated_id"])
            doi_norm = normalize_doi(row.get("doi"))
            if doi_norm:
                acm_doi_map[doi_norm] = a_id
            title_norm = normalize_title(row.get("title"))
            if title_norm:
                acm_title_map[title_norm] = a_id

        # ACM DL (OVERLAP_DOI mapped to master_id)
        acm_overlap = self.acm_df[self.acm_df["cross_db_status"] == "OVERLAP_DOI"]
        for _, row in acm_overlap.iterrows():
            m_id = str(row["matched_master_id"])
            doi_norm = normalize_doi(row.get("doi"))
            if doi_norm and doi_norm not in master_doi_map:
                master_doi_map[doi_norm] = m_id
            title_norm = normalize_title(row.get("title"))
            if title_norm and title_norm not in master_title_map:
                master_title_map[title_norm] = m_id

        superseded_count = 0
        new_arxiv_count = 0

        cross_db_status_list = []
        matched_peer_id_list = []
        dedup_basis_list = []
        arxiv_consolidated_ids = []

        for idx, row in passed_df.iterrows():
            arxiv_id_base = row["arxiv_id_base"]
            arxiv_doi_norm = normalize_doi(row.get("doi"))
            arxiv_title_norm = normalize_title(row.get("title"))

            matched_id: Optional[str] = None
            match_basis = "NONE"

            # 1. Match by Normalized DOI
            if arxiv_doi_norm:
                if arxiv_doi_norm in master_doi_map:
                    matched_id = master_doi_map[arxiv_doi_norm]
                    match_basis = "NORMALIZED_DOI_MASTER"
                elif arxiv_doi_norm in acm_doi_map:
                    matched_id = acm_doi_map[arxiv_doi_norm]
                    match_basis = "NORMALIZED_DOI_ACM"

            # 2. Match by Normalized Title
            if not matched_id and arxiv_title_norm:
                if arxiv_title_norm in master_title_map:
                    matched_id = master_title_map[arxiv_title_norm]
                    match_basis = "NORMALIZED_TITLE_MASTER"
                elif arxiv_title_norm in acm_title_map:
                    matched_id = acm_title_map[arxiv_title_norm]
                    match_basis = "NORMALIZED_TITLE_ACM"

            # 3. Match by arXiv ID in DOI or Link of peer-reviewed records
            if not matched_id:
                m_match = self.master_scopus_ieee_df[
                    self.master_scopus_ieee_df["DOI"].astype(str).str.contains(arxiv_id_base, case=False, na=False) |
                    self.master_scopus_ieee_df["Link"].astype(str).str.contains(arxiv_id_base, case=False, na=False)
                ]
                if len(m_match) > 0:
                    matched_id = str(m_match.iloc[0]["master_id"])
                    match_basis = "ARXIV_ID_IN_MASTER_METADATA"

            if not matched_id:
                a_match = acm_new[
                    acm_new["doi"].astype(str).str.contains(arxiv_id_base, case=False, na=False) |
                    acm_new["url"].astype(str).str.contains(arxiv_id_base, case=False, na=False)
                ]
                if len(a_match) > 0:
                    matched_id = str(a_match.iloc[0]["acm_consolidated_id"])
                    match_basis = "ARXIV_ID_IN_ACM_METADATA"

            if matched_id:
                cross_db_status_list.append("SUPERSEDED_BY_PEER_REVIEWED")
                matched_peer_id_list.append(matched_id)
                dedup_basis_list.append(match_basis)
                superseded_count += 1
            else:
                cross_db_status_list.append("NEW_ARXIV_PREPRINT")
                matched_peer_id_list.append("")
                dedup_basis_list.append("NONE")
                new_arxiv_count += 1

            arxiv_consolidated_ids.append(f"ARXIV-S-{len(arxiv_consolidated_ids)+1:04d}")

        passed_df["arxiv_consolidated_id"] = arxiv_consolidated_ids
        passed_df["cross_db_status"] = cross_db_status_list
        passed_df["matched_peer_reviewed_id"] = matched_peer_id_list
        passed_df["dedup_match_basis"] = dedup_basis_list

        print(f"[DEDUP_RESULTS] Filtered preprints superseded by peer-reviewed corpus: {superseded_count}")
        print(f"[DEDUP_RESULTS] Incremental new preprints (Tier 2 candidates): {new_arxiv_count}")

        # Export ARXIV_S1_S2_S3_FILTERED_DEDUP.csv
        reordered_cols = [
            "arxiv_consolidated_id", "cross_db_status", "matched_peer_reviewed_id", "dedup_match_basis",
            "arxiv_id_base", "arxiv_id_versioned", "title", "authors", "published_utc", "updated_utc",
            "matched_pillars", "preprint_rigor_signal", "cutoff_eligibility_status", "screening_status",
            "search_queries", "query_count", "raw_occurrence_count", "source_row_provenance",
            "primary_category", "all_categories", "doi", "journal_ref", "comment", "abstract",
            "arxiv_url", "pdf_url"
        ]
        passed_df = passed_df[[c for c in reordered_cols if c in passed_df.columns]]
        passed_df.to_csv(OUT_FILTERED_CSV, index=False)
        print(f"[EXPORT] Wrote {len(passed_df)} filtered unique records to '{OUT_FILTERED_CSV}'")

        return passed_df

    def build_unified_master_corpus(self, passed_df: pd.DataFrame) -> pd.DataFrame:
        """
        Builds the unified Master SLR table combining:
        - Tier 1 (PEER_REVIEWED): 432 unique records from Scopus (257), IEEE Xplore (+85), and ACM DL (+90),
          enriched with linked_arxiv_id_versioned found during deduplication.
        - Tier 2 (PREPRINT_ARXIV_VERSION_PINNED): Only the NEW_ARXIV_PREPRINT records passing the strict gate.
        """
        print("\n" + "="*80)
        print("STAGE 6: Building Unified Master SLR Full Corpus Table")
        print("="*80)

        superseded_preprints = passed_df[passed_df["cross_db_status"] == "SUPERSEDED_BY_PEER_REVIEWED"]
        peer_to_arxiv_map: Dict[str, str] = {}
        for _, r in superseded_preprints.iterrows():
            m_id = str(r["matched_peer_reviewed_id"])
            v_id = str(r["arxiv_id_versioned"])
            if m_id:
                peer_to_arxiv_map[m_id] = v_id

        master_rows: List[Dict[str, Any]] = []

        # 1. Scopus + IEEE Master (342 records)
        for _, r in self.master_scopus_ieee_df.iterrows():
            m_id = str(r["master_id"])
            linked_arxiv = peer_to_arxiv_map.get(m_id, "")
            master_rows.append({
                "study_id": m_id,
                "tier": "PEER_REVIEWED",
                "databases": r.get("databases", ""),
                "db_count": r.get("db_count", 1),
                "combined_pillars": r.get("combined_pillars", ""),
                "Title": r.get("Title", ""),
                "Authors": r.get("Authors", ""),
                "Year": r.get("Year", ""),
                "Source_Venue": r.get("Source_Venue", ""),
                "Document_Type": r.get("Document_Type", ""),
                "DOI": r.get("DOI", ""),
                "Link": r.get("Link", ""),
                "Abstract": r.get("Abstract", ""),
                "Author_Keywords": r.get("Author_Keywords", ""),
                "Index_IEEE_Terms": r.get("Index_IEEE_Terms", ""),
                "screening_status": r.get("screening_status", "UNSCREENED"),
                "linked_arxiv_id_versioned": linked_arxiv,
                "cross_db_status": "PEER_REVIEWED_SCOPUS_IEEE",
                "preprint_rigor_signal": "",
                "published_utc": "",
                "updated_utc": "",
                "provenance": f"Scopus_EID:{r.get('Scopus_EID','')}; IEEE_ID:{r.get('IEEE_Xplore_IDs','')}"
            })

        # 2. ACM DL Incremental (90 records)
        acm_new = self.acm_df[self.acm_df["cross_db_status"] == "NEW_ACM_ONLY"]
        for _, r in acm_new.iterrows():
            a_id = str(r["acm_consolidated_id"])
            linked_arxiv = peer_to_arxiv_map.get(a_id, "")
            master_rows.append({
                "study_id": a_id,
                "tier": "PEER_REVIEWED",
                "databases": "ACM_Digital_Library",
                "db_count": 1,
                "combined_pillars": r.get("pillars", ""),
                "Title": r.get("title", ""),
                "Authors": r.get("author", ""),
                "Year": r.get("year", ""),
                "Source_Venue": r.get("booktitle_or_journal", ""),
                "Document_Type": r.get("entry_type", ""),
                "DOI": r.get("doi", ""),
                "Link": r.get("url", ""),
                "Abstract": r.get("abstract", ""),
                "Author_Keywords": r.get("keywords", ""),
                "Index_IEEE_Terms": "",
                "screening_status": r.get("screening_status", "UNSCREENED"),
                "linked_arxiv_id_versioned": linked_arxiv,
                "cross_db_status": "NEW_ACM_ONLY",
                "preprint_rigor_signal": "",
                "published_utc": "",
                "updated_utc": "",
                "provenance": f"ACM_CiteKey:{r.get('all_acm_cite_keys','')}; ACM_ID:{a_id}"
            })

        tier1_count = len(master_rows)
        print(f"[CORPUS] Consolidated Tier 1 (PEER_REVIEWED): {tier1_count} studies (342 Scopus/IEEE + 90 ACM DL)")

        # 3. Tier 2: NEW_ARXIV_PREPRINT (Eligible preprints passing strict gate)
        new_preprints = passed_df[passed_df["cross_db_status"] == "NEW_ARXIV_PREPRINT"]
        for idx, r in new_preprints.iterrows():
            year_val = ""
            pub_str = str(r.get("published_utc", ""))
            if len(pub_str) >= 4 and pub_str[:4].isdigit():
                year_val = pub_str[:4]

            master_rows.append({
                "study_id": r.get("arxiv_consolidated_id", ""),
                "tier": "PREPRINT_ARXIV_VERSION_PINNED",
                "databases": "arXiv_Preprint",
                "db_count": 1,
                "combined_pillars": r.get("matched_pillars", ""),
                "Title": r.get("title", ""),
                "Authors": r.get("authors", ""),
                "Year": year_val,
                "Source_Venue": "arXiv.org",
                "Document_Type": "Preprint",
                "DOI": r.get("doi", ""),
                "Link": r.get("arxiv_url", ""),
                "Abstract": r.get("abstract", ""),
                "Author_Keywords": r.get("all_categories", ""),
                "Index_IEEE_Terms": "",
                "screening_status": "UNSCREENED",
                "linked_arxiv_id_versioned": r.get("arxiv_id_versioned", ""),
                "cross_db_status": "NEW_ARXIV_PREPRINT",
                "preprint_rigor_signal": r.get("preprint_rigor_signal", ""),
                "published_utc": r.get("published_utc", ""),
                "updated_utc": r.get("updated_utc", ""),
                "provenance": r.get("source_row_provenance", "")
            })

        tier2_count = len(new_preprints)
        total_master_count = len(master_rows)
        print(f"[CORPUS] Appended Tier 2 (PREPRINT_ARXIV_VERSION_PINNED): {tier2_count} preprints")
        print(f"[CORPUS] Total Unified Master SLR Corpus: {total_master_count} records (Tier 1: {tier1_count} + Tier 2: {tier2_count})")

        master_corpus_df = pd.DataFrame(master_rows)
        master_corpus_df.to_csv(OUT_MASTER_CORPUS_CSV, index=False)
        print(f"[EXPORT] Wrote unified Master table to '{OUT_MASTER_CORPUS_CSV}'")
        return master_corpus_df

    def verify_gold_standard_seeds(self, passed_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Verifies the retrieval and filtering status of all 4 gold-standard seeds."""
        print("\n" + "="*80)
        print("STAGE 7: Gold-Standard Seed Preprints Audit")
        print("="*80)

        seed_audit_rows = []
        for seed_id, info in SEED_PREPRINTS.items():
            seed_ref = info["seed_ref"]
            expected_title = info["expected_title"]
            thematic_focus = info["thematic_focus"]

            raw_matches = [r for r in self.raw_records if r["arxiv_id_base"] == seed_id]
            retrieved_sources = "; ".join(sorted(list({r["query_source"] for r in raw_matches}))) if raw_matches else "NOT_RETRIEVED"
            raw_version = raw_matches[0]["arxiv_id_versioned"] if raw_matches else "N/A"
            published_utc = raw_matches[0]["published_utc"] if raw_matches else "N/A"
            updated_utc = raw_matches[0]["updated_utc"] if raw_matches else "N/A"

            filtered_match = passed_df[passed_df["arxiv_id_base"] == seed_id]
            if len(filtered_match) > 0:
                frow = filtered_match.iloc[0]
                pass_status = "PASSED_STRICT_GATE"
                cross_status = frow["cross_db_status"]
                rigor_sig = frow["preprint_rigor_signal"]
                matched_peer = frow["matched_peer_reviewed_id"] if frow["matched_peer_reviewed_id"] else "None (New Preprint)"
            else:
                pass_status = "REJECTED_OR_MISSING"
                cross_status = "N/A"
                rigor_sig = "N/A"
                matched_peer = "N/A"

            audit_item = {
                "seed_id": seed_id,
                "versioned_id": raw_version,
                "seed_ref": seed_ref,
                "title": expected_title,
                "thematic_focus": thematic_focus,
                "query_sources": retrieved_sources,
                "gate_status": pass_status,
                "cross_db_status": cross_status,
                "matched_peer_id": matched_peer,
                "rigor_signal": rigor_sig,
                "published_utc": published_utc,
                "updated_utc": updated_utc
            }
            seed_audit_rows.append(audit_item)
            print(f"[SEED {seed_ref}] ID: {raw_version} | Status: {pass_status} | Cross-DB: {cross_status} | Sources: {retrieved_sources}")

        return seed_audit_rows

    def generate_prisma_s_report(self, passed_df: pd.DataFrame, seed_audit: List[Dict[str, Any]], master_corpus_df: pd.DataFrame):
        """Generates comprehensive PRISMA-S audit report in Markdown with SHA-256 checksums."""
        print("\n" + "="*80)
        print("STAGE 8: Generating PRISMA-S Audit Report")
        print("="*80)

        execution_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        checksum_files = [
            ("Master Scopus + IEEE Input", FILE_MASTER_SCOPUS_IEEE),
            ("ACM DL Deduplicated Input", FILE_ACM_DEDUP),
            ("arXiv Raw Export Output", OUT_RAW_CSV),
            ("arXiv Filtered & Deduplicated Output", OUT_FILTERED_CSV),
            ("Master SLR Full Corpus Output", OUT_MASTER_CORPUS_CSV)
        ]

        checksum_rows = []
        for desc, fpath in checksum_files:
            if os.path.exists(fpath):
                sha = compute_sha256(fpath)
                size_bytes = os.path.getsize(fpath)
                checksum_rows.append(f"| `{os.path.basename(fpath)}` | {desc} | `{sha}` | {size_bytes:,} bytes |")
            else:
                checksum_rows.append(f"| `{os.path.basename(fpath)}` | {desc} | *FILE NOT FOUND* | - |")

        q_raw_counts = self.query_counts
        
        q_passed_counts = {}
        q_superseded_counts = {}
        q_new_counts = {}

        for q in ["ARXIV_S1a", "ARXIV_S1b", "ARXIV_S2", "ARXIV_S3"]:
            q_passed = passed_df[passed_df["search_queries"].astype(str).str.contains(q)]
            q_passed_counts[q] = len(q_passed)
            q_superseded_counts[q] = len(q_passed[q_passed["cross_db_status"] == "SUPERSEDED_BY_PEER_REVIEWED"])
            q_new_counts[q] = len(q_passed[q_passed["cross_db_status"] == "NEW_ARXIV_PREPRINT"])

        tier1_total = len(master_corpus_df[master_corpus_df["tier"] == "PEER_REVIEWED"])
        tier2_total = len(master_corpus_df[master_corpus_df["tier"] == "PREPRINT_ARXIV_VERSION_PINNED"])
        full_corpus_total = len(master_corpus_df)

        report_md = f"""# PRISMA-S Audit Report: Targeted Supplementary Preprint Search & Consolidated Master Corpus

**SLR Title:** *{SLR_TITLE}*  
**Search Method:** Targeted Supplementary Preprint Search (PRISMA 2020: *"Identification of studies via other methods / grey literature"*)  
**Execution Timestamp:** `{execution_utc}`  
**Eligibility Cutoff Date:** `{CUTOFF_ISO_STR}` (15 October 2026 inclusive)  
**API Endpoint:** `{ARXIV_API_URL}`  
**Rate Limit Compliance:** `time.sleep({RATE_LIMIT_SLEEP})` between requests | `User-Agent: {USER_AGENT}`  

---

## 1. Cryptographic File Integrity & SHA-256 Checksums

The table below documents the cryptographic SHA-256 checksums and byte lengths of all input databases and generated production datasets:

| Artifact / Dataset | Description | SHA-256 Checksum | File Size |
| :--- | :--- | :--- | :--- |
""" + "\n".join(checksum_rows) + f"""

---

## 2. Targeted Supplementary Search Architecture (`ARXIV_S1a` – `ARXIV_S3`)

Four targeted modular queries were executed against the official arXiv Atom API, restricted to Computer Science categories (`cat:cs.CR OR cat:cs.AI OR cat:cs.MA OR cat:cs.SE OR cat:cs.DC`). Results were parsed, deduplicated internally across queries, passed through the strict `Title + Abstract` relevance gate, and deduplicated against our peer-reviewed corpus:

| Query ID | Thematic Pillar Focus | Raw arXiv Hits | Passing Gate (Unique) | Superseded by Peer-Reviewed | Incremental New Preprints |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`ARXIV_S1a`** | Cryptographic Assurance, Hardware Enclaves/TEE & Provenance | {q_raw_counts.get('ARXIV_S1a', 0):,} | {q_passed_counts.get('ARXIV_S1a', 0):,} | {q_superseded_counts.get('ARXIV_S1a', 0):,} | {q_new_counts.get('ARXIV_S1a', 0):,} |
| **`ARXIV_S1b`** | Advanced Encryption, Multiparty Computation & Post-Quantum | {q_raw_counts.get('ARXIV_S1b', 0):,} | {q_passed_counts.get('ARXIV_S1b', 0):,} | {q_superseded_counts.get('ARXIV_S1b', 0):,} | {q_new_counts.get('ARXIV_S1b', 0):,} |
| **`ARXIV_S2`** | Authenticated Delegation, Workload Identity & Capabilities | {q_raw_counts.get('ARXIV_S2', 0):,} | {q_passed_counts.get('ARXIV_S2', 0):,} | {q_superseded_counts.get('ARXIV_S2', 0):,} | {q_new_counts.get('ARXIV_S2', 0):,} |
| **`ARXIV_S3`** | Boundary Attacks, Tool/MCP Exploits & Runtime Policy | {q_raw_counts.get('ARXIV_S3', 0):,} | {q_passed_counts.get('ARXIV_S3', 0):,} | {q_superseded_counts.get('ARXIV_S3', 0):,} | {q_new_counts.get('ARXIV_S3', 0):,} |
| **`SEED_CHECK`** | Direct ID Fetch for Gold-Standard Seed Preprints | {q_raw_counts.get('SEED_CHECK', 0):,} | - | - | - |
| **TOTAL (Consolidated)** | **Net Unique arXiv Corpus** | **{len(self.raw_records):,}** | **{len(passed_df):,}** | **{len(passed_df[passed_df['cross_db_status'] == 'SUPERSEDED_BY_PEER_REVIEWED']):,}** | **{tier2_total:,}** |

> **Note on Query Overlap:** Preprints matching multiple queries (e.g., both cryptographic enclaves in `S1a` and authenticated delegation in `S2`) are counted in each applicable query column above, but are strictly deduplicated to single unique rows in the consolidated totals and in `{OUT_FILTERED_CSV}`.

---

## 3. Gold-Standard Seed Preprint Verification (`SEED_CHECK`)

Four benchmark seed preprints were predefined as gold standards to validate query sensitivity and gate precision:

| Seed Ref | arXiv ID (Base) | Version-Pinned ID | Title | Query Source | Gate Status | Cross-DB Status | Matched Peer ID | Rigor Signal | Published (UTC) |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
"""

        for sa in seed_audit:
            report_md += f"| **{sa['seed_ref']}** | `{sa['seed_id']}` | `{sa['versioned_id']}` | *{sa['title']}* | `{sa['query_sources']}` | `{sa['gate_status']}` | `{sa['cross_db_status']}` | `{sa['matched_peer_id']}` | `{sa['rigor_signal']}` | `{sa['published_utc']}` |\n"

        report_md += f"""
---

## 4. Complete PRISMA 2020 Identification & Deduplication Flow

The flow counts below reflect the complete literature identification across both peer-reviewed databases and targeted supplementary grey literature (preprints):

```mermaid
flowchart TD
    subgraph Traditional_Databases ["Identification: Peer-Reviewed Databases"]
        S1["Scopus + IEEE Xplore Raw Hits<br/>(Initial Exports)"] --> S2["Master Scopus + IEEE Combined<br/><b>342 unique studies</b>"]
        S2 --> S3["Scopus exclusive: 156<br/>Scopus + IEEE overlap: 101<br/>IEEE Xplore exclusive: 85"]
        A1["ACM Digital Library Raw Hits<br/>(113 records)"] --> A2["ACM Cross-DB Deduplication<br/>(23 matched Scopus/IEEE)"]
        A2 --> A3["ACM DL Exclusive:<br/><b>+90 unique studies</b>"]
        S2 --> T1["Consolidated Tier 1 (Peer-Reviewed)<br/><b>432 unique studies</b>"]
        A3 --> T1
    end

    subgraph Supplementary_Preprints ["Identification: Other Methods / Preprints (arXiv)"]
        X1["arXiv Modular API Retrieval<br/><b>{len(self.raw_records):,} raw hits</b><br/>(S1a: {q_raw_counts.get('ARXIV_S1a', 0):,}, S1b: {q_raw_counts.get('ARXIV_S1b', 0):,}, S2: {q_raw_counts.get('ARXIV_S2', 0):,}, S3: {q_raw_counts.get('ARXIV_S3', 0):,})"] --> X2["Internal Deduplication by Base ID<br/><b>{len({r['arxiv_id_base'] for r in self.raw_records}):,} unique preprints</b>"]
        X2 --> X3["Strict Title + Abstract Gate<br/>(Category, LLM Entity, Pillar & CTF filter)<br/><b>{len(passed_df):,} passing preprints</b>"]
        X3 --> X4{{"Cross-DB Matching with Tier 1<br/>(Normalized DOI & Title)"}}
        X4 -- "Matched Peer-Reviewed" --> X5["SUPERSEDED_BY_PEER_REVIEWED<br/><b>{len(passed_df[passed_df['cross_db_status'] == 'SUPERSEDED_BY_PEER_REVIEWED']):,} preprints</b><br/>(Enriched into Tier 1 records)"]
        X4 -- "No Match (Unique)" --> X6["NEW_ARXIV_PREPRINT<br/><b>{tier2_total:,} incremental preprints</b><br/>(Tier 2: Version-Pinned)"]
    end

    subgraph Unified_Corpus ["Consolidated Master SLR Full Corpus"]
        T1 --> M["Unified Master SLR Corpus (DEDUP)<br/><b>{full_corpus_total:,} total studies</b>"]
        X6 --> M
    end
```

### Detailed Flow Accounting:
1. **Tier 1 (Peer-Reviewed Corpus):**
   - Scopus Unique Records: **257** (156 Scopus exclusive + 101 dual-indexed in IEEE)
   - IEEE Xplore Exclusive Records: **85**
   - Scopus + IEEE Combined: **342**
   - ACM Digital Library Exclusive (`NEW_ACM_ONLY`): **90**
   - **Total Tier 1 Unique Studies:** **432**
2. **Tier 2 (Targeted Supplementary Preprints / arXiv):**
   - Total Raw Hits Retrieved: **{len(self.raw_records):,}**
   - Unique Preprints Evaluated: **{len({r['arxiv_id_base'] for r in self.raw_records}):,}**
   - Preprints Passing Strict `Title + Abstract` Gate: **{len(passed_df):,}**
   - Preprints Superseded by Peer-Reviewed Versions: **{len(passed_df[passed_df['cross_db_status'] == 'SUPERSEDED_BY_PEER_REVIEWED']):,}**
   - **Total Tier 2 Incremental New Preprints:** **{tier2_total:,}**
3. **Consolidated Master SLR Full Corpus (`{OUT_MASTER_CORPUS_CSV}`):**
   - **Total Studies for Screening:** **{full_corpus_total:,}** (`432` Tier 1 Peer-Reviewed + `{tier2_total:,}` Tier 2 Version-Pinned Preprints)

---

## 5. Peer-Reviewed Supersession Audit

All arXiv preprints matching records in the peer-reviewed corpus (`Master_Scopus_IEEE_COMBINED_DEDUP.csv` or `ACM_S1_S2_S3_FILTERED_DEDUP.csv`) by normalized DOI, normalized Title, or embedded metadata were designated as `SUPERSEDED_BY_PEER_REVIEWED`. This ensures that preprints published as formal journal or conference papers are not double-counted in synthesis, while their exact version string is recorded in the Master corpus under `linked_arxiv_id_versioned`.

---
*Report generated automatically by `arxiv_slr_supplementary_pipeline.py` adhering to PRISMA 2020 and PRISMA-S reporting standards.*
"""

        with open(OUT_REPORT_MD, "w", encoding="utf-8") as f:
            f.write(report_md)

        print(f"[EXPORT] Successfully wrote PRISMA-S report to '{OUT_REPORT_MD}'")

    def run(self):
        """Executes the complete pipeline."""
        start_time = time.time()
        print("="*80)
        print(f"STARTING SLR SUPPLEMENTARY PREPRINT PIPELINE")
        print(f"Title: {SLR_TITLE}")
        print(f"Cutoff Date: {CUTOFF_ISO_STR}")
        print("="*80)

        # 1. Load Peer-Reviewed Corpus
        self.load_peer_reviewed_corpus()

        # 2. Execute arXiv API Searches & Seed Check
        self.execute_arxiv_searches()

        # 3. Internal Deduplication & Strict Gate Filtering
        passed_df, filtered_df = self.internal_deduplication_and_filtering()

        # 4. Cross-Database Deduplication
        passed_df = self.cross_database_deduplication(passed_df)

        # 5. Build Unified Master SLR Corpus
        master_corpus_df = self.build_unified_master_corpus(passed_df)

        # 6. Verify Seeds
        seed_audit = self.verify_gold_standard_seeds(passed_df)

        # 7. Generate PRISMA-S Report
        self.generate_prisma_s_report(passed_df, seed_audit, master_corpus_df)

        elapsed = time.time() - start_time
        print("\n" + "="*80)
        print(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.1f}s ({elapsed/60.0:.2f} min)")
        print("="*80)


# ======================================================================================
# ENTRY POINT
# ======================================================================================
if __name__ == "__main__":
    pipeline = ArxivSLRSupplementaryPipeline()
    pipeline.run()
