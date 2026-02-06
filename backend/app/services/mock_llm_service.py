"""Mock LLM Service for testing without GitHub token."""
from typing import Dict, Any, List
from app.models import COREPField, Justification, RuleReference

class MockLLMService:
    """Mock LLM service that returns predefined responses."""
    
    def __init__(self):
        """Initialize mock service."""
        self.model_name = "mock-gpt-4o-mini"
    
    def generate_corep_output(
        self,
        user_query: str,
        scenario: Dict[str, Any],
        regulatory_context: str,
        template_id: str = "C_01_00"
    ) -> Dict[str, Any]:
        """
        Generate mock COREP output based on scenario.
        
        This simulates what the real LLM would return.
        """
        # Extract scenario values
        ordinary_shares = scenario.get("ordinary_shares", 0)
        retained_earnings = scenario.get("retained_earnings", 0)
        additional_tier1 = scenario.get("additional_tier1", 0)
        tier2_capital = scenario.get("tier2_capital", 0)
        
        # Calculate values (in thousands)
        cet1_value = (ordinary_shares + retained_earnings) * 1000
        tier1_value = cet1_value + (additional_tier1 * 1000)
        tier2_value = tier2_capital * 1000
        own_funds_value = tier1_value + tier2_value
        
        # Create fields
        fields = []
        
        if own_funds_value > 0:
            fields.append(COREPField(
                row="010",
                column="010",
                label="Total Own Funds",
                value=own_funds_value,
                unit="GBP_thousands",
                confidence=0.92
            ))
        
        if tier1_value > 0:
            fields.append(COREPField(
                row="020",
                column="010",
                label="Tier 1 Capital",
                value=tier1_value,
                unit="GBP_thousands",
                confidence=0.95
            ))
        
        if cet1_value > 0:
            fields.append(COREPField(
                row="030",
                column="010",
                label="Common Equity Tier 1 (CET1)",
                value=cet1_value,
                unit="GBP_thousands",
                confidence=0.93
            ))
        
        if additional_tier1 > 0:
            fields.append(COREPField(
                row="040",
                column="010",
                label="Additional Tier 1 (AT1)",
                value=additional_tier1 * 1000,
                unit="GBP_thousands",
                confidence=0.90
            ))
        
        if tier2_value > 0:
            fields.append(COREPField(
                row="060",
                column="010",
                label="Tier 2 Capital",
                value=tier2_value,
                unit="GBP_thousands",
                confidence=0.88
            ))
        
        # Create justifications
        justifications = []
        
        # Justification for CET1
        if cet1_value > 0:
            justifications.append(Justification(
                field_id="030_010",
                reasoning=f"Based on Article 25 of the PRA Rulebook, Common Equity Tier 1 comprises ordinary shares (£{ordinary_shares}M) and retained earnings (£{retained_earnings}M), totaling £{ordinary_shares + retained_earnings}M or £{cet1_value:,}k.",
                confidence=0.93,
                rule_references=[
                    RuleReference(
                        source="PRA Rulebook",
                        article="Article 25",
                        paragraph="1",
                        text_excerpt="Common Equity Tier 1 items shall comprise: (a) capital instruments; (b) share premium; (c) retained earnings; (d) accumulated other comprehensive income",
                        relevance_score=0.95
                    ),
                    RuleReference(
                        source="COREP Instructions",
                        article="C 01.00",
                        paragraph="Row 030",
                        text_excerpt="Common Equity Tier 1 capital includes ordinary shares and retained earnings after deductions",
                        relevance_score=0.90
                    )
                ]
            ))
        
        # Justification for Tier 1
        if tier1_value > 0:
            justifications.append(Justification(
                field_id="020_010",
                reasoning=f"According to Article 51, Tier 1 capital equals CET1 (£{cet1_value:,}k) plus Additional Tier 1 (£{additional_tier1 * 1000:,}k), totaling £{tier1_value:,}k.",
                confidence=0.95,
                rule_references=[
                    RuleReference(
                        source="PRA Rulebook",
                        article="Article 51",
                        paragraph="1",
                        text_excerpt="Tier 1 capital shall consist of the sum of Common Equity Tier 1 capital and Additional Tier 1 capital",
                        relevance_score=0.98
                    )
                ]
            ))
        
        # Justification for Own Funds
        if own_funds_value > 0:
            justifications.append(Justification(
                field_id="010_010",
                reasoning=f"Per Article 72, Own Funds equal Tier 1 capital (£{tier1_value:,}k) plus Tier 2 capital (£{tier2_value:,}k), totaling £{own_funds_value:,}k.",
                confidence=0.92,
                rule_references=[
                    RuleReference(
                        source="PRA Rulebook",
                        article="Article 72",
                        paragraph="1",
                        text_excerpt="Own funds shall consist of the sum of Tier 1 capital and Tier 2 capital",
                        relevance_score=0.97
                    )
                ]
            ))
        
        # Add reasoning steps for chain-of-thought
        reasoning_steps = {
            "analysis": f"The scenario describes a UK bank with ordinary shares of £{ordinary_shares}M and retained earnings of £{retained_earnings}M. According to PRA Rulebook Article 25, these components qualify as Common Equity Tier 1 (CET1). Additional Tier 1 instruments total £{additional_tier1}M, and Tier 2 capital is £{tier2_capital}M.",
            
            "calculation": f"""Step-by-step calculation:
1. CET1 = Ordinary Shares + Retained Earnings
   CET1 = £{ordinary_shares}M + £{retained_earnings}M = £{ordinary_shares + retained_earnings}M = £{cet1_value:,}k

2. Tier 1 = CET1 + AT1
   Tier 1 = £{cet1_value:,}k + £{additional_tier1 * 1000:,}k = £{tier1_value:,}k

3. Own Funds = Tier 1 + Tier 2
   Own Funds = £{tier1_value:,}k + £{tier2_value:,}k = £{own_funds_value:,}k""",
            
            "justification": "Article 25 confirms that ordinary shares and retained earnings are core CET1 components. Article 51 establishes that Tier 1 comprises CET1 and AT1. Article 72 defines Own Funds as the sum of Tier 1 and Tier 2 capital. All regulatory citations support the calculated values.",
            
            "verification": f"""Cross-field consistency checks:
✓ Tier 1 (£{tier1_value:,}k) = CET1 (£{cet1_value:,}k) + AT1 (£{additional_tier1 * 1000:,}k)
✓ Own Funds (£{own_funds_value:,}k) = Tier 1 (£{tier1_value:,}k) + Tier 2 (£{tier2_value:,}k)
✓ All capital values are positive
{"✓ Tier 2 is within 1/3 of Tier 1 limit" if tier2_value <= tier1_value / 3 else "⚠ Tier 2 exceeds 1/3 of Tier 1"}"""
        }
        
        return {
            "reasoning_steps": reasoning_steps,
            "fields": fields,
            "justifications": justifications
        }
