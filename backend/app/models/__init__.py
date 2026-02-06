from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class COREPField(BaseModel):
    """Represents a single field in a COREP template."""
    row: str
    column: str
    label: str
    value: Optional[float] = None
    unit: str = "GBP_thousands"
    confidence: float = Field(ge=0, le=1, default=0.0)

class RuleReference(BaseModel):
    """Reference to a regulatory rule."""
    source: str  # e.g., "PRA Rulebook"
    article: str
    paragraph: Optional[Any] = None
    text_excerpt: str
    relevance_score: float = Field(ge=0, le=1)

class Justification(BaseModel):
    """Justification for a field value."""
    field_id: str
    rule_references: List[RuleReference]
    reasoning: str
    confidence: float = Field(ge=0, le=1)

class ValidationError(BaseModel):
    """Validation error or warning."""
    field_id: Optional[str] = None
    severity: str  # "error" or "warning"
    message: str
    rule: Optional[str] = None

class ValidationResult(BaseModel):
    """Result of validation checks."""
    is_valid: bool
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

class QueryRequest(BaseModel):
    """Request to process a COREP query."""
    user_query: str
    scenario: Dict[str, Any]
    template_id: str = "C_01_00"

class COREPResponse(BaseModel):
    """Response containing populated COREP template."""
    query_id: str
    template_id: str
    fields: List[COREPField]
    justifications: List[Justification]
    validation: ValidationResult
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
class AuditLog(BaseModel):
    """Audit log for a query."""
    query_id: str
    timestamp: datetime
    user_query: str
    scenario: Dict[str, Any]
    template_id: str
    fields: List[COREPField]
    justifications: List[Justification]
    validation: ValidationResult
    llm_metadata: Dict[str, Any]
