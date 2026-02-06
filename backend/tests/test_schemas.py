"""Tests for COREP schemas."""
import pytest
from app.schemas.corep_schemas import OwnFundsTemplate, get_template_schema
from pydantic import ValidationError

class TestCOREPSchemas:
    """Test suite for COREP template schemas."""
    
    def test_own_funds_template_creation(self):
        """Test creating OwnFundsTemplate with valid data."""
        template = OwnFundsTemplate(
            tier1_capital=600,
            common_equity_tier1=600,
            additional_tier1=0,
            tier2_capital=0,
            total_own_funds=600
        )
        
        assert template.template_id == "C_01_00"
        assert template.tier1_capital == 600
        assert template.common_equity_tier1 == 600
    
    def test_positive_value_validation(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            OwnFundsTemplate(
                tier1_capital=-100,
                common_equity_tier1=600
            )
    
    def test_to_fields_conversion(self):
        """Test conversion to COREP fields list."""
        template = OwnFundsTemplate(
            total_own_funds=700,
            tier1_capital=600,
            common_equity_tier1=550,
            additional_tier1=50,
            tier2_capital=100
        )
        
        fields = template.to_fields()
        
        assert len(fields) == 5
        assert all(hasattr(field, 'row') for field in fields)
        assert all(hasattr(field, 'value') for field in fields)
        assert all(hasattr(field, 'confidence') for field in fields)
    
    def test_partial_template_creation(self):
        """Test creating template with only some fields."""
        template = OwnFundsTemplate(
            tier1_capital=600,
            common_equity_tier1=600
        )
        
        fields = template.to_fields()
        
        # Should only include non-None fields
        assert len(fields) == 2
        assert all(field.value is not None for field in fields)
    
    def test_get_template_schema(self):
        """Test template schema retrieval."""
        schema = get_template_schema("C_01_00")
        
        assert schema == OwnFundsTemplate
    
    def test_field_labels(self):
        """Test that field labels are correct."""
        template = OwnFundsTemplate(
            total_own_funds=700,
            tier1_capital=600
        )
        
        fields = template.to_fields()
        
        labels = [field.label for field in fields]
        assert "Total Own Funds" in labels
        assert "Tier 1 Capital" in labels
    
    def test_confidence_scores(self):
        """Test that confidence scores are set."""
        template = OwnFundsTemplate(
            tier1_capital=600
        )
        
        fields = template.to_fields()
        
        assert all(0 <= field.confidence <= 1 for field in fields)
