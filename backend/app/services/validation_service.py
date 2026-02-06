from typing import List, Dict, Any, Optional
from app.models import COREPField, ValidationError, ValidationResult

class ValidationService:
    """Service for validating COREP template data."""
    
    def __init__(self, template_id: str = "C_01_00"):
        """Initialize validation service."""
        self.template_id = template_id
        self.rules = self._load_validation_rules()
    
    def validate_output(self, fields: List[COREPField]) -> ValidationResult:
        """
        Run all validation checks on COREP fields.
        
        Args:
            fields: List of populated COREP fields
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        # Convert fields to dict for easier lookup
        field_dict = {f"{f.row}_{f.column}": f for f in fields}
        
        # Type and range validation
        errors.extend(self._validate_types_and_ranges(fields))
        
        # Cross-field consistency checks
        errors.extend(self._validate_consistency(field_dict))
        
        # Completeness checks
        warnings.extend(self._check_completeness(field_dict))
        
        # Business rules
        errors.extend(self._validate_business_rules(field_dict))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_types_and_ranges(self, fields: List[COREPField]) -> List[ValidationError]:
        """Validate field types and value ranges."""
        errors = []
        
        for field in fields:
            field_id = f"{field.row}_{field.column}"
            
            # Check value is numeric
            if field.value is not None:
                try:
                    float(field.value)
                except (TypeError, ValueError):
                    errors.append(ValidationError(
                        field_id=field_id,
                        severity="error",
                        message=f"Field {field.label} must be numeric",
                        rule="TYPE_CHECK"
                    ))
                
                # Check for negative values in capital fields
                if field.value < 0 and field.row in ["010", "020", "030", "040", "060"]:
                    errors.append(ValidationError(
                        field_id=field_id,
                        severity="error",
                        message=f"Field {field.label} cannot be negative",
                        rule="RANGE_CHECK"
                    ))
        
        return errors
    
    def _validate_consistency(self, field_dict: Dict[str, COREPField]) -> List[ValidationError]:
        """Validate cross-field consistency."""
        errors = []
        
        # Helper to get field by row (fallback to first column if multiple exist)
        def get_by_row(row: str) -> Optional[COREPField]:
            # Try 010 first (standard)
            if f"{row}_010" in field_dict:
                return field_dict[f"{row}_010"]
            # Fallback to any column matching this row
            for key, field in field_dict.items():
                if key.startswith(f"{row}_"):
                    return field
            return None

        # Check: Tier 1 = CET1 + AT1
        tier1 = get_by_row("020")
        cet1 = get_by_row("030")
        at1 = get_by_row("040")
        
        if tier1 and cet1:
            at1_value = at1.value if at1 else 0
            expected_tier1 = cet1.value + at1_value
            
            if abs(tier1.value - expected_tier1) > 0.01:  # Allow small rounding errors
                errors.append(ValidationError(
                    field_id=f"{tier1.row}_{tier1.column}",
                    severity="error",
                    message=f"Tier 1 capital ({tier1.value}) must equal CET1 ({cet1.value}) + AT1 ({at1_value})",
                    rule="TIER1_COMPOSITION"
                ))
        
        # Check: Own Funds = Tier 1 + Tier 2
        own_funds = get_by_row("010")
        tier2 = get_by_row("060")
        
        if own_funds and tier1:
            tier2_value = tier2.value if tier2 else 0
            expected_own_funds = tier1.value + tier2_value
            
            if abs(own_funds.value - expected_own_funds) > 0.01:
                errors.append(ValidationError(
                    field_id=f"{own_funds.row}_{own_funds.column}",
                    severity="error",
                    message=f"Own Funds ({own_funds.value}) must equal Tier 1 ({tier1.value}) + Tier 2 ({tier2_value})",
                    rule="OWN_FUNDS_COMPOSITION"
                ))
        
        # Check: Tier 2 <= 1/3 of Tier 1
        if tier1 and tier2:
            max_tier2 = tier1.value / 3
            if tier2.value > max_tier2:
                errors.append(ValidationError(
                    field_id=f"{tier2.row}_{tier2.column}",
                    severity="error",
                    message=f"Tier 2 capital ({tier2.value}) cannot exceed one third of Tier 1 ({max_tier2:.2f})",
                    rule="TIER2_LIMIT"
                ))
        
        return errors
    
    def _check_completeness(self, field_dict: Dict[str, COREPField]) -> List[ValidationError]:
        """Check for missing required fields."""
        warnings = []
        
        required_rows = {
            "010": "Total Own Funds",
            "020": "Tier 1 Capital",
            "030": "Common Equity Tier 1"
        }
        
        # Create a set of populated rows
        populated_rows = {key.split('_')[0] for key, field in field_dict.items() if field.value is not None}
        
        for row, label in required_rows.items():
            if row not in populated_rows:
                warnings.append(ValidationError(
                    field_id=f"{row}_010",
                    severity="warning",
                    message=f"Required field {label} is not populated",
                    rule="COMPLETENESS_CHECK"
                ))
        
        return warnings
    
    def _validate_business_rules(self, field_dict: Dict[str, COREPField]) -> List[ValidationError]:
        """Validate business-specific rules."""
        errors = []
        
        # CET1 must be positive
        cet1 = field_dict.get("030_010")
        if cet1 and cet1.value <= 0:
            errors.append(ValidationError(
                field_id="030_010",
                severity="error",
                message="Common Equity Tier 1 must be positive",
                rule="CET1_POSITIVE"
            ))
        
        # Tier 1 must be positive
        tier1 = field_dict.get("020_010")
        if tier1 and tier1.value <= 0:
            errors.append(ValidationError(
                field_id="020_010",
                severity="error",
                message="Tier 1 capital must be positive",
                rule="TIER1_POSITIVE"
            ))
        
        return errors
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules for template."""
        return {
            "required_fields": ["010_010", "020_010", "030_010"],
            "consistency_checks": [
                "TIER1_COMPOSITION",
                "OWN_FUNDS_COMPOSITION",
                "TIER2_LIMIT"
            ],
            "business_rules": [
                "CET1_POSITIVE",
                "TIER1_POSITIVE"
            ]
        }
