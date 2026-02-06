from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class COREPField(BaseModel):
    """Field definition for COREP templates."""
    row: str
    column: str
    label: str
    value: Optional[float] = None
    unit: str = "GBP_thousands"
    confidence: float = Field(ge=0, le=1, default=0.0)

class OwnFundsTemplate(BaseModel):
    """
    COREP Template C 01.00 - Own Funds
    
    Simplified schema for prototype focusing on key Tier 1 capital fields.
    """
    template_id: str = "C_01_00"
    template_name: str = "Own Funds"
    
    # Key fields
    tier1_capital: Optional[float] = Field(None, description="Row 020: Total Tier 1 Capital")
    common_equity_tier1: Optional[float] = Field(None, description="Row 030: Common Equity Tier 1")
    additional_tier1: Optional[float] = Field(None, description="Row 040: Additional Tier 1")
    tier2_capital: Optional[float] = Field(None, description="Row 060: Tier 2 Capital")
    total_own_funds: Optional[float] = Field(None, description="Row 010: Total Own Funds")
    
    @field_validator('tier1_capital', 'common_equity_tier1', 'total_own_funds')
    @classmethod
    def validate_positive(cls, v):
        """Ensure capital values are positive."""
        if v is not None and v < 0:
            raise ValueError("Capital values must be positive")
        return v
    
    def to_fields(self) -> List[COREPField]:
        """Convert to list of COREP fields."""
        fields = []
        
        if self.total_own_funds is not None:
            fields.append(COREPField(
                row="010", column="010", 
                label="Total Own Funds",
                value=self.total_own_funds,
                confidence=0.9
            ))
        
        if self.tier1_capital is not None:
            fields.append(COREPField(
                row="020", column="010",
                label="Tier 1 Capital",
                value=self.tier1_capital,
                confidence=0.9
            ))
        
        if self.common_equity_tier1 is not None:
            fields.append(COREPField(
                row="030", column="010",
                label="Common Equity Tier 1",
                value=self.common_equity_tier1,
                confidence=0.9
            ))
        
        if self.additional_tier1 is not None:
            fields.append(COREPField(
                row="040", column="010",
                label="Additional Tier 1",
                value=self.additional_tier1,
                confidence=0.8
            ))
        
        if self.tier2_capital is not None:
            fields.append(COREPField(
                row="060", column="010",
                label="Tier 2 Capital",
                value=self.tier2_capital,
                confidence=0.8
            ))
        
        return fields

# Template registry
TEMPLATE_SCHEMAS = {
    "C_01_00": OwnFundsTemplate
}

def get_template_schema(template_id: str):
    """Get schema for a specific template."""
    return TEMPLATE_SCHEMAS.get(template_id, OwnFundsTemplate)
