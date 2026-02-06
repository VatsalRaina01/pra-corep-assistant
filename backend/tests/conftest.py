"""Test configuration and fixtures."""
import pytest
from app.config import settings

@pytest.fixture
def sample_scenario():
    """Sample COREP scenario for testing."""
    return {
        "entity_type": "UK bank",
        "ordinary_shares": 500,
        "retained_earnings": 100,
        "additional_tier1": 0,
        "tier2_capital": 0,
        "currency": "GBP"
    }

@pytest.fixture
def sample_query():
    """Sample user query for testing."""
    return "How should we report Tier 1 capital for our UK subsidiary?"

@pytest.fixture
def sample_regulatory_context():
    """Sample regulatory context for testing."""
    return """PRA Rulebook - Article 25: Common Equity Tier 1 items
    
Common Equity Tier 1 (CET1) comprises:
- Capital instruments (ordinary shares)
- Share premium
- Retained earnings
- Other reserves

Article 51: Tier 1 capital = Common Equity Tier 1 + Additional Tier 1

Article 72: Own funds = Tier 1 capital + Tier 2 capital"""
