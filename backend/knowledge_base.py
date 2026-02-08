"""
PRA COREP Knowledge Base
Simplified regulatory text for CA1 (Own Funds) and CA2 (Capital Requirements)
"""

# ============================================================================
# REGULATORY KNOWLEDGE BASE
# ============================================================================

KNOWLEDGE_BASE = {
    # -------------------------------------------------------------------------
    # CET1 CAPITAL ITEMS (CRR Articles 26-35)
    # -------------------------------------------------------------------------
    "CRR_ART_26": {
        "id": "CRR_ART_26",
        "title": "CRR Article 26 - Common Equity Tier 1 items",
        "category": "CET1",
        "keywords": ["CET1", "common equity", "tier 1", "capital instruments", "share capital", "share premium"],
        "text": """
Article 26 - Common Equity Tier 1 items

1. Common Equity Tier 1 items of institutions shall consist of:
   (a) capital instruments, provided the conditions laid down in Article 28 are met;
   (b) share premium accounts related to the instruments referred to in point (a);
   (c) retained earnings;
   (d) accumulated other comprehensive income;
   (e) other reserves;
   (f) funds for general banking risk.

2. The items referred to in points (c) to (f) shall only be recognised as CET1 where 
   they are available to the institution for unrestricted and immediate use to cover 
   risks or losses as soon as these occur.

3. For the purposes of point (c), institutions may include interim or year-end profits 
   only with the prior permission of the competent authority.
"""
    },
    
    "CRR_ART_28": {
        "id": "CRR_ART_28",
        "title": "CRR Article 28 - Capital instruments qualifying as CET1",
        "category": "CET1",
        "keywords": ["CET1", "capital instruments", "ordinary shares", "conditions", "qualify"],
        "text": """
Article 28 - Capital instruments qualifying as Common Equity Tier 1 instruments

1. Capital instruments qualify as CET1 instruments only if all the following conditions are met:
   (a) the instruments are issued directly by the institution with prior approval of shareholders;
   (b) the instruments are fully paid up and not funded directly or indirectly by the institution;
   (c) the instruments are classified as equity under applicable accounting standards;
   (d) the instruments are clearly and separately disclosed in the balance sheet;
   (e) the instruments are perpetual;
   (f) the principal amount may not be reduced except through liquidation or discretionary repurchases;
   (g) distributions are paid only from distributable items;
   (h) distributions are not linked to the amount paid up at issuance;
   (i) instruments rank below all other claims in the event of insolvency or liquidation;
   (j) instruments do not benefit from any guarantee that enhances seniority.
"""
    },
    
    "CRR_ART_36": {
        "id": "CRR_ART_36",
        "title": "CRR Article 36 - Deductions from CET1 items",
        "category": "CET1_DEDUCTIONS",
        "keywords": ["deductions", "CET1", "intangible assets", "goodwill", "deferred tax", "defined benefit pension"],
        "text": """
Article 36 - Deductions from Common Equity Tier 1 items

1. Institutions shall deduct the following from CET1 items:
   (a) losses for the current financial year;
   (b) intangible assets, including goodwill;
   (c) deferred tax assets that rely on future profitability;
   (d) for institutions calculating risk-weighted exposure using IRB Approach: 
       negative amounts resulting from expected loss calculations;
   (e) defined benefit pension fund assets on the balance sheet;
   (f) direct, indirect and synthetic holdings of own CET1 instruments;
   (g) holdings of CET1 instruments of financial sector entities with reciprocal cross-holdings;
   (h) applicable amount of holdings of CET1 instruments of financial sector entities 
       where the institution has a significant investment;
   (i) the amount of items required to be deducted from AT1 that exceeds the AT1 capital;
   (j) exposures that qualify for a risk weight of 1,250% where deduction is applied.
"""
    },
    
    # -------------------------------------------------------------------------
    # AT1 CAPITAL ITEMS (CRR Articles 51-54)
    # -------------------------------------------------------------------------
    "CRR_ART_51": {
        "id": "CRR_ART_51",
        "title": "CRR Article 51 - Additional Tier 1 items",
        "category": "AT1",
        "keywords": ["AT1", "additional tier 1", "capital instruments", "share premium"],
        "text": """
Article 51 - Additional Tier 1 items

Additional Tier 1 items shall consist of:
(a) capital instruments, where the conditions laid down in Article 52 are met;
(b) the share premium accounts related to the instruments referred to in point (a).

Additional Tier 1 instruments plus share premium accounts shall equal AT1 capital 
before deductions as specified in Article 56.
"""
    },
    
    "CRR_ART_52": {
        "id": "CRR_ART_52",
        "title": "CRR Article 52 - Capital instruments qualifying as AT1",
        "category": "AT1",
        "keywords": ["AT1", "capital instruments", "conditions", "perpetual", "subordinated"],
        "text": """
Article 52 - Capital instruments qualifying as Additional Tier 1 instruments

1. Capital instruments qualify as AT1 instruments where the following conditions are met:
   (a) the instruments are issued and paid up;
   (b) the instruments are not purchased or funded directly/indirectly by the institution;
   (c) the instruments rank below Tier 2 instruments in insolvency or liquidation;
   (d) the instruments are not secured or guaranteed;
   (e) the instruments are perpetual with no incentive to redeem;
   (f) call options may only be exercised after a minimum of 5 years;
   (g) distributions are paid only from distributable items;
   (h) distributions are fully discretionary;
   (i) instruments include a principal loss absorption mechanism (write-down or conversion).
"""
    },
    
    # -------------------------------------------------------------------------
    # TIER 2 CAPITAL ITEMS (CRR Articles 62-65)
    # -------------------------------------------------------------------------
    "CRR_ART_62": {
        "id": "CRR_ART_62",
        "title": "CRR Article 62 - Tier 2 items",
        "category": "T2",
        "keywords": ["tier 2", "T2", "capital instruments", "subordinated loans"],
        "text": """
Article 62 - Tier 2 items

Tier 2 items shall consist of:
(a) capital instruments and subordinated loans where the conditions in Article 63 are met;
(b) the share premium accounts related to instruments referred to in point (a);
(c) for institutions calculating risk-weighted exposure using IRB Approach:
    positive amounts resulting from the calculation in Article 159, limited to 0.6% of RWAs;
(d) for institutions using Standardised Approach:
    general credit risk adjustments limited to 1.25% of RWAs.
"""
    },
    
    "CRR_ART_63": {
        "id": "CRR_ART_63",
        "title": "CRR Article 63 - Capital instruments qualifying as Tier 2",
        "category": "T2",
        "keywords": ["tier 2", "T2", "conditions", "subordinated", "minimum maturity"],
        "text": """
Article 63 - Capital instruments qualifying as Tier 2 instruments

Capital instruments or subordinated loans qualify as T2 instruments where:
(a) the instruments are issued and paid up;
(b) the instruments are not purchased by the institution or its subsidiaries;
(c) the claim on the principal is wholly subordinated to all non-subordinated creditors;
(d) the instruments are not secured or guaranteed;
(e) the instruments do not contain features providing incentive for early redemption;
(f) original maturity is at least 5 years;
(g) call options may only be exercised after minimum 5 years from issuance;
(h) early repayment provisions do not give holders the right to accelerate repayment.

Tier 2 instruments are subject to amortisation in the final 5 years before maturity.
"""
    },
    
    # -------------------------------------------------------------------------
    # CAPITAL REQUIREMENTS (CRR Article 92)
    # -------------------------------------------------------------------------
    "CRR_ART_92": {
        "id": "CRR_ART_92",
        "title": "CRR Article 92 - Own funds requirements",
        "category": "CAPITAL_REQUIREMENTS",
        "keywords": ["capital requirements", "CET1 ratio", "tier 1 ratio", "total capital ratio", "8%", "6%", "4.5%"],
        "text": """
Article 92 - Own funds requirements

1. Subject to Articles 93 and 94, institutions shall at all times satisfy the following:
   (a) a Common Equity Tier 1 capital ratio of 4.5%;
   (b) a Tier 1 capital ratio of 6%;
   (c) a total capital ratio of 8%.

2. Institutions shall calculate their capital ratios as follows:
   (a) CET1 capital ratio = CET1 capital / Total risk exposure amount;
   (b) Tier 1 capital ratio = Tier 1 capital / Total risk exposure amount;
   (c) Total capital ratio = Total own funds / Total risk exposure amount.

3. The total risk exposure amount shall be calculated as the sum of:
   (a) risk-weighted exposure amounts for credit risk and dilution risk;
   (b) own funds requirements for position risk, FX risk, and commodity risk × 12.5;
   (c) own funds requirements for operational risk × 12.5;
   (d) own funds requirements for credit valuation adjustment risk × 12.5.
"""
    },
    
    "CRR_ART_92A": {
        "id": "CRR_ART_92A",
        "title": "CRR Article 92a - Capital buffers",
        "category": "CAPITAL_BUFFERS",
        "keywords": ["capital buffers", "CCB", "countercyclical", "systemic", "G-SII", "O-SII"],
        "text": """
Article 92a - Capital buffer requirements (from CRD IV)

In addition to Article 92 requirements, institutions must hold capital buffers:

1. Capital Conservation Buffer (CCB): 2.5% of total risk exposure in CET1
   - Designed to ensure institutions build up capital buffers outside stressed periods

2. Countercyclical Capital Buffer (CCyB): 0-2.5% (set by national authorities)
   - Varies based on credit growth conditions in the jurisdiction

3. Systemic Risk Buffers:
   - G-SII buffer: 1-3.5% for Global Systemically Important Institutions
   - O-SII buffer: 0-3% for Other Systemically Important Institutions

Combined buffer requirement = CCB + CCyB + max(SRB, G-SII, O-SII)
"""
    },
    
    # -------------------------------------------------------------------------
    # RISK-WEIGHTED ASSETS (CRR Articles 111-134)
    # -------------------------------------------------------------------------
    "CRR_ART_111": {
        "id": "CRR_ART_111",
        "title": "CRR Article 111 - Credit risk: Standardised Approach",
        "category": "RWA",
        "keywords": ["RWA", "risk weighted assets", "standardised approach", "SA", "exposure classes"],
        "text": """
Article 111 - Exposure value under Standardised Approach

1. The exposure value of an asset item shall be its accounting value remaining after 
   specific credit risk adjustments, additional value adjustments, and deductions.

2. The exposure value of an off-balance sheet item shall be determined by applying 
   a credit conversion factor (CCF) to its nominal value:
   - 100% for guarantees, credit derivatives, securities lending
   - 50% for note issuance facilities and revolving underwriting facilities
   - 20% for undrawn credit facilities with original maturity > 1 year
   - 0% for unconditionally cancellable undrawn facilities

3. Risk weights under the Standardised Approach depend on exposure class:
   - Central governments and central banks: 0-150% based on credit quality step
   - Institutions: 20-150% based on credit quality step
   - Corporates: 20-150% based on credit quality step
   - Retail: 75% for qualifying exposures
   - Secured by mortgages on immovable property: 35% (residential), 50% (commercial)
   - Exposures in default: 100% or 150%
"""
    },
    
    # -------------------------------------------------------------------------
    # COREP TEMPLATE INSTRUCTIONS
    # -------------------------------------------------------------------------
    "COREP_CA1": {
        "id": "COREP_CA1",
        "title": "COREP Template C 01.00 - Own Funds",
        "category": "COREP_TEMPLATE",
        "keywords": ["CA1", "own funds", "template", "COREP", "reporting"],
        "text": """
C 01.00 - OWN FUNDS (CA1)

This template collects information on the composition of own funds for COREP reporting.

Row Structure:
- Rows 010-090: Common Equity Tier 1 (CET1) capital
  - 010: Capital instruments eligible as CET1
  - 020: Share premium related to CET1 instruments
  - 030: Retained earnings
  - 040: Accumulated other comprehensive income
  - 050: Other reserves
  - 060: Funds for general banking risk
  - 070: Adjustments to CET1 due to prudential filters
  - 080: (-) Goodwill
  - 090: (-) Other intangible assets

- Rows 100-200: Regulatory adjustments to CET1
  - 100: (-) Deferred tax assets dependent on future profitability
  - 110: (-) Defined benefit pension fund assets
  - 120: (-) Direct, indirect and synthetic holdings of own CET1
  - 130: CET1 capital elements or deductions - other

- Row 200: Common Equity Tier 1 capital (sum)

- Rows 300-400: Additional Tier 1 (AT1) capital
  - 300: Capital instruments eligible as AT1
  - 310: Share premium related to AT1 instruments
  - 320: (-) Holdings of own AT1 instruments
  - 400: Additional Tier 1 capital (sum)

- Row 500: Tier 1 capital = CET1 + AT1

- Rows 600-700: Tier 2 capital
  - 600: Capital instruments eligible as T2
  - 610: Share premium related to T2 instruments
  - 620: Credit risk adjustments (SA or IRB)
  - 630: (-) Holdings of own T2 instruments
  - 700: Tier 2 capital (sum)

- Row 800: Total Own Funds = Tier 1 + Tier 2
"""
    },
    
    "COREP_CA2": {
        "id": "COREP_CA2",
        "title": "COREP Template C 02.00 - Capital requirements",
        "category": "COREP_TEMPLATE",
        "keywords": ["CA2", "capital requirements", "RWA", "template", "COREP"],
        "text": """
C 02.00 - OWN FUNDS REQUIREMENTS (CA2)

This template collects risk exposure amounts and own funds requirements.

Row Structure:
- Rows 010-090: Credit risk
  - 010: Credit risk - Standardised Approach (SA)
  - 020: Credit risk - IRB Approach
  - 030: Securitisation positions
  - 040: Contribution to default fund of a CCP

- Rows 100-200: Market risk
  - 100: Position risk
  - 110: Foreign exchange risk
  - 120: Commodities risk

- Rows 300-400: Credit valuation adjustment risk
  - 300: CVA risk (standardised method)
  - 310: CVA risk (advanced method)

- Rows 500-600: Operational risk
  - 500: Basic Indicator Approach
  - 510: Standardised Approach
  - 520: Advanced Measurement Approach

- Row 700: Total risk exposure amount (TREA)

- Rows 800-900: Capital ratios (memorandum items)
  - 800: CET1 capital ratio (%)
  - 810: Tier 1 capital ratio (%)
  - 820: Total capital ratio (%)
  - 830: Institution-specific buffer requirement (%)
  - 840: CET1 available to meet buffers (%)

Column Structure:
- Column 010: Risk exposure amount / Requirement
- Column 020: Previous period comparison
"""
    },
    
    "COREP_VALIDATION": {
        "id": "COREP_VALIDATION",
        "title": "COREP Validation Rules",
        "category": "VALIDATION",
        "keywords": ["validation", "rules", "checks", "consistency", "errors"],
        "text": """
COREP Validation Rules for CA1 and CA2

Basic Arithmetic Validations:
1. CA1.200 (CET1) = 010+020+030+040+050+060+070-080-090-100-110-120+130
2. CA1.500 (Tier 1) = CA1.200 + CA1.400
3. CA1.800 (Total own funds) = CA1.500 + CA1.700
4. CA2.800 (CET1 ratio) = CA1.200 / CA2.700 × 100
5. CA2.810 (T1 ratio) = CA1.500 / CA2.700 × 100
6. CA2.820 (Total ratio) = CA1.800 / CA2.700 × 100

Regulatory Threshold Validations:
7. CA2.800 (CET1 ratio) >= 4.5% — MINIMUM_CET1_RATIO
8. CA2.810 (T1 ratio) >= 6.0% — MINIMUM_T1_RATIO
9. CA2.820 (Total ratio) >= 8.0% — MINIMUM_TOTAL_RATIO

Consistency Validations:
10. Intangible assets (CA1.080+CA1.090) <= Total assets from balance sheet
11. Tier 2 credit risk adjustments (CA1.620) <= 1.25% of RWA for SA
12. AT1 instruments must not exceed 1/3 of Tier 1 capital
13. T2 capital must not exceed Tier 1 capital

Sign Validations:
14. Deductions (rows with '-') must be reported as positive values
15. Capital items must be non-negative (except for accumulated losses)
"""
    }
}

# ============================================================================
# CA1 TEMPLATE SCHEMA
# ============================================================================

CA1_TEMPLATE_SCHEMA = {
    "template_id": "C_01.00",
    "template_name": "Own Funds",
    "rows": [
        # CET1 Capital Items
        {"row_id": "010", "label": "Capital instruments eligible as CET1 capital", "category": "CET1", "sign": "+"},
        {"row_id": "020", "label": "Share premium", "category": "CET1", "sign": "+"},
        {"row_id": "030", "label": "Retained earnings", "category": "CET1", "sign": "+"},
        {"row_id": "040", "label": "Accumulated other comprehensive income", "category": "CET1", "sign": "+"},
        {"row_id": "050", "label": "Other reserves", "category": "CET1", "sign": "+"},
        {"row_id": "060", "label": "Funds for general banking risk", "category": "CET1", "sign": "+"},
        {"row_id": "070", "label": "Adjustments to CET1 due to prudential filters", "category": "CET1", "sign": "+/-"},
        {"row_id": "080", "label": "(-) Goodwill", "category": "CET1_DED", "sign": "-"},
        {"row_id": "090", "label": "(-) Other intangible assets", "category": "CET1_DED", "sign": "-"},
        {"row_id": "100", "label": "(-) Deferred tax assets dependent on future profitability", "category": "CET1_DED", "sign": "-"},
        {"row_id": "110", "label": "(-) Defined benefit pension fund assets", "category": "CET1_DED", "sign": "-"},
        {"row_id": "120", "label": "(-) Direct, indirect and synthetic holdings of own CET1", "category": "CET1_DED", "sign": "-"},
        {"row_id": "130", "label": "CET1 capital elements or deductions - other", "category": "CET1", "sign": "+/-"},
        {"row_id": "200", "label": "Common Equity Tier 1 (CET1) capital", "category": "CET1_TOTAL", "sign": "=", "is_total": True},
        
        # AT1 Capital Items
        {"row_id": "300", "label": "Capital instruments eligible as AT1 capital", "category": "AT1", "sign": "+"},
        {"row_id": "310", "label": "Share premium related to AT1 instruments", "category": "AT1", "sign": "+"},
        {"row_id": "320", "label": "(-) Holdings of own AT1 instruments", "category": "AT1_DED", "sign": "-"},
        {"row_id": "330", "label": "AT1 capital elements or deductions - other", "category": "AT1", "sign": "+/-"},
        {"row_id": "400", "label": "Additional Tier 1 (AT1) capital", "category": "AT1_TOTAL", "sign": "=", "is_total": True},
        
        # Tier 1 Total
        {"row_id": "500", "label": "Tier 1 capital (T1 = CET1 + AT1)", "category": "T1_TOTAL", "sign": "=", "is_total": True},
        
        # Tier 2 Capital Items
        {"row_id": "600", "label": "Capital instruments eligible as T2 capital", "category": "T2", "sign": "+"},
        {"row_id": "610", "label": "Share premium related to T2 instruments", "category": "T2", "sign": "+"},
        {"row_id": "620", "label": "Credit risk adjustments", "category": "T2", "sign": "+"},
        {"row_id": "630", "label": "(-) Holdings of own T2 instruments", "category": "T2_DED", "sign": "-"},
        {"row_id": "640", "label": "T2 capital elements or deductions - other", "category": "T2", "sign": "+/-"},
        {"row_id": "700", "label": "Tier 2 (T2) capital", "category": "T2_TOTAL", "sign": "=", "is_total": True},
        
        # Total Own Funds
        {"row_id": "800", "label": "Total Own Funds (T1 + T2)", "category": "TOTAL", "sign": "=", "is_total": True},
    ]
}

# ============================================================================
# CA2 TEMPLATE SCHEMA
# ============================================================================

CA2_TEMPLATE_SCHEMA = {
    "template_id": "C_02.00",
    "template_name": "Own Funds Requirements",
    "rows": [
        # Credit Risk
        {"row_id": "010", "label": "Credit risk - Standardised Approach (SA)", "category": "CREDIT_RISK", "sign": "+"},
        {"row_id": "020", "label": "Credit risk - IRB Approach", "category": "CREDIT_RISK", "sign": "+"},
        {"row_id": "030", "label": "Securitisation positions", "category": "CREDIT_RISK", "sign": "+"},
        {"row_id": "040", "label": "Contribution to CCP default fund", "category": "CREDIT_RISK", "sign": "+"},
        {"row_id": "050", "label": "Total credit risk RWA", "category": "CREDIT_RISK_TOTAL", "sign": "=", "is_total": True},
        
        # Market Risk
        {"row_id": "100", "label": "Position risk (trading book)", "category": "MARKET_RISK", "sign": "+"},
        {"row_id": "110", "label": "Foreign exchange risk", "category": "MARKET_RISK", "sign": "+"},
        {"row_id": "120", "label": "Commodities risk", "category": "MARKET_RISK", "sign": "+"},
        {"row_id": "150", "label": "Total market risk RWA", "category": "MARKET_RISK_TOTAL", "sign": "=", "is_total": True},
        
        # CVA Risk
        {"row_id": "200", "label": "Credit valuation adjustment risk", "category": "CVA_RISK", "sign": "+"},
        
        # Operational Risk
        {"row_id": "300", "label": "Operational risk", "category": "OP_RISK", "sign": "+"},
        
        # Total RWA
        {"row_id": "500", "label": "Total Risk Exposure Amount (TREA)", "category": "TOTAL_RWA", "sign": "=", "is_total": True},
        
        # Capital Ratios
        {"row_id": "600", "label": "CET1 capital ratio (%)", "category": "RATIO", "sign": "%"},
        {"row_id": "610", "label": "Tier 1 capital ratio (%)", "category": "RATIO", "sign": "%"},
        {"row_id": "620", "label": "Total capital ratio (%)", "category": "RATIO", "sign": "%"},
        {"row_id": "630", "label": "Institution-specific buffer requirement (%)", "category": "BUFFER", "sign": "%"},
        {"row_id": "640", "label": "CET1 available to meet buffers (%)", "category": "BUFFER", "sign": "%"},
    ]
}

# ============================================================================
# VALIDATION RULES
# ============================================================================

VALIDATION_RULES = [
    {
        "id": "VAL_001",
        "name": "CET1 total calculation",
        "type": "ARITHMETIC",
        "severity": "ERROR",
        "description": "CET1 capital must equal sum of CET1 items minus deductions",
        "formula": "row_200 = row_010 + row_020 + row_030 + row_040 + row_050 + row_060 + row_070 - row_080 - row_090 - row_100 - row_110 - row_120 + row_130"
    },
    {
        "id": "VAL_002",
        "name": "Tier 1 total calculation",
        "type": "ARITHMETIC",
        "severity": "ERROR",
        "description": "Tier 1 capital must equal CET1 plus AT1",
        "formula": "row_500 = row_200 + row_400"
    },
    {
        "id": "VAL_003",
        "name": "Total own funds calculation",
        "type": "ARITHMETIC",
        "severity": "ERROR",
        "description": "Total own funds must equal Tier 1 plus Tier 2",
        "formula": "row_800 = row_500 + row_700"
    },
    {
        "id": "VAL_004",
        "name": "Minimum CET1 ratio",
        "type": "THRESHOLD",
        "severity": "ERROR",
        "description": "CET1 ratio must be at least 4.5%",
        "threshold": 4.5,
        "field": "cet1_ratio"
    },
    {
        "id": "VAL_005",
        "name": "Minimum Tier 1 ratio",
        "type": "THRESHOLD",
        "severity": "ERROR",
        "description": "Tier 1 ratio must be at least 6.0%",
        "threshold": 6.0,
        "field": "t1_ratio"
    },
    {
        "id": "VAL_006",
        "name": "Minimum total capital ratio",
        "type": "THRESHOLD",
        "severity": "ERROR",
        "description": "Total capital ratio must be at least 8.0%",
        "threshold": 8.0,
        "field": "total_ratio"
    },
    {
        "id": "VAL_007",
        "name": "Non-negative capital instruments",
        "type": "SIGN",
        "severity": "ERROR",
        "description": "Capital instruments (rows 010, 300, 600) must be non-negative",
        "fields": ["row_010", "row_300", "row_600"]
    },
    {
        "id": "VAL_008",
        "name": "Deductions as positive values",
        "type": "SIGN",
        "severity": "WARNING",
        "description": "Deduction items should be reported as positive values (they will be subtracted)",
        "fields": ["row_080", "row_090", "row_100", "row_110", "row_120", "row_320", "row_630"]
    },
    {
        "id": "VAL_009",
        "name": "Capital conservation buffer",
        "type": "THRESHOLD",
        "severity": "WARNING",
        "description": "CET1 ratio should exceed 7.0% to meet CCB requirement (4.5% + 2.5%)",
        "threshold": 7.0,
        "field": "cet1_ratio"
    },
    {
        "id": "VAL_010",
        "name": "RWA consistency",
        "type": "ARITHMETIC",
        "severity": "ERROR",
        "description": "Total RWA must equal sum of risk category RWAs",
        "formula": "ca2_row_500 = ca2_row_050 + ca2_row_150 + ca2_row_200 + ca2_row_300"
    }
]

# ============================================================================
# RETRIEVAL FUNCTION
# ============================================================================

def retrieve_relevant_context(query: str, top_k: int = 3) -> list:
    """
    Simple keyword-based retrieval from knowledge base.
    Returns most relevant regulatory text based on query.
    """
    query_lower = query.lower()
    scores = []
    
    for doc_id, doc in KNOWLEDGE_BASE.items():
        score = 0
        # Check keywords
        for keyword in doc["keywords"]:
            if keyword.lower() in query_lower:
                score += 10
        # Check title
        if any(word in doc["title"].lower() for word in query_lower.split()):
            score += 5
        # Check category
        if doc["category"].lower() in query_lower:
            score += 3
            
        if score > 0:
            scores.append((score, doc))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top_k documents
    return [doc for _, doc in scores[:top_k]]


def get_all_knowledge_for_template(template: str) -> list:
    """
    Get all knowledge items relevant to a specific template.
    """
    template_upper = template.upper()
    relevant = []
    
    for doc_id, doc in KNOWLEDGE_BASE.items():
        if template_upper in doc["category"] or template_upper in " ".join(doc["keywords"]).upper():
            relevant.append(doc)
    
    # Always include the template instructions
    if template_upper == "CA1":
        relevant.append(KNOWLEDGE_BASE.get("COREP_CA1", {}))
        relevant.append(KNOWLEDGE_BASE.get("COREP_VALIDATION", {}))
    elif template_upper == "CA2":
        relevant.append(KNOWLEDGE_BASE.get("COREP_CA2", {}))
        relevant.append(KNOWLEDGE_BASE.get("CRR_ART_92", {}))
        relevant.append(KNOWLEDGE_BASE.get("COREP_VALIDATION", {}))
    
    return relevant
