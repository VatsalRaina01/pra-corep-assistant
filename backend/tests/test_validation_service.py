"""Tests for validation service."""
import pytest
from app.services.validation_service import ValidationService
from app.models import COREPField

class TestValidationService:
    """Test suite for ValidationService."""
    
    def test_valid_tier1_composition(self):
        """Test that Tier 1 = CET1 + AT1 validation passes."""
        fields = [
            COREPField(row="020", column="010", label="Tier 1", value=600, confidence=0.9),
            COREPField(row="030", column="010", label="CET1", value=500, confidence=0.9),
            COREPField(row="040", column="010", label="AT1", value=100, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert result.is_valid == True
        assert len(result.errors) == 0
    
    def test_invalid_tier1_composition(self):
        """Test that incorrect Tier 1 composition is caught."""
        fields = [
            COREPField(row="020", column="010", label="Tier 1", value=700, confidence=0.9),
            COREPField(row="030", column="010", label="CET1", value=500, confidence=0.9),
            COREPField(row="040", column="010", label="AT1", value=100, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert result.is_valid == False
        assert len(result.errors) > 0
        assert any("Tier 1" in error.message for error in result.errors)
    
    def test_valid_own_funds_composition(self):
        """Test that Own Funds = Tier 1 + Tier 2 validation passes."""
        fields = [
            COREPField(row="010", column="010", label="Own Funds", value=700, confidence=0.9),
            COREPField(row="020", column="010", label="Tier 1", value=600, confidence=0.9),
            COREPField(row="060", column="010", label="Tier 2", value=100, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert result.is_valid == True
        assert len(result.errors) == 0
    
    def test_tier2_limit_validation(self):
        """Test that Tier 2 <= 1/3 of Tier 1 is enforced."""
        fields = [
            COREPField(row="020", column="010", label="Tier 1", value=600, confidence=0.9),
            COREPField(row="060", column="010", label="Tier 2", value=300, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert result.is_valid == False
        assert any("one third" in error.message.lower() for error in result.errors)
    
    def test_negative_value_validation(self):
        """Test that negative capital values are rejected."""
        fields = [
            COREPField(row="030", column="010", label="CET1", value=-100, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert result.is_valid == False
        assert any("negative" in error.message.lower() for error in result.errors)
    
    def test_completeness_warnings(self):
        """Test that missing required fields generate warnings."""
        fields = [
            COREPField(row="040", column="010", label="AT1", value=50, confidence=0.9),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        assert len(result.warnings) > 0
        assert any("required field" in warning.message.lower() for warning in result.warnings)
    
    def test_empty_fields_list(self):
        """Test validation with no fields."""
        service = ValidationService()
        result = service.validate_output([])
        
        assert len(result.warnings) > 0  # Should warn about missing required fields
    
    def test_confidence_scores_preserved(self):
        """Test that confidence scores are preserved through validation."""
        fields = [
            COREPField(row="030", column="010", label="CET1", value=600, confidence=0.95),
        ]
        
        service = ValidationService()
        result = service.validate_output(fields)
        
        # Validation shouldn't modify the input fields
        assert fields[0].confidence == 0.95
