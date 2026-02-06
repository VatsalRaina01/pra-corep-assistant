import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from app.models import COREPField, Justification, ValidationResult, AuditLog

class AuditService:
    """Service for creating and managing audit logs."""
    
    def __init__(self, log_directory: str = "./data/audit_logs"):
        """Initialize audit service."""
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
    
    def create_audit_log(
        self,
        query_id: str,
        user_query: str,
        scenario: Dict[str, Any],
        template_id: str,
        fields: List[COREPField],
        justifications: List[Justification],
        validation: ValidationResult,
        llm_metadata: Dict[str, Any] = None
    ) -> AuditLog:
        """
        Create comprehensive audit trail.
        
        Args:
            query_id: Unique query identifier
            user_query: Original user question
            scenario: Scenario parameters
            template_id: COREP template ID
            fields: Populated fields
            justifications: Field justifications
            validation: Validation results
            llm_metadata: LLM processing metadata
            
        Returns:
            AuditLog object
        """
        audit_log = AuditLog(
            query_id=query_id,
            timestamp=datetime.utcnow(),
            user_query=user_query,
            scenario=scenario,
            template_id=template_id,
            fields=fields,
            justifications=justifications,
            validation=validation,
            llm_metadata=llm_metadata or {}
        )
        
        # Save to file
        self._save_audit_log(audit_log)
        
        return audit_log
    
    def get_audit_log(self, query_id: str) -> AuditLog:
        """Retrieve audit log by query ID."""
        log_file = self.log_directory / f"{query_id}.json"
        
        if not log_file.exists():
            raise FileNotFoundError(f"Audit log not found: {query_id}")
        
        with open(log_file, 'r') as f:
            data = json.load(f)
            return AuditLog(**data)
    
    def generate_audit_report(self, query_id: str) -> str:
        """
        Generate human-readable audit report.
        
        Args:
            query_id: Query identifier
            
        Returns:
            Formatted audit report as string
        """
        try:
            audit_log = self.get_audit_log(query_id)
        except FileNotFoundError:
            return f"Audit log not found for query: {query_id}"
        
        report_lines = [
            "=" * 80,
            "COREP REPORTING AUDIT LOG",
            "=" * 80,
            f"\nQuery ID: {audit_log.query_id}",
            f"Timestamp: {audit_log.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Template: {audit_log.template_id}",
            f"\nUSER QUERY:",
            f"{audit_log.user_query}",
            f"\nSCENARIO:",
            json.dumps(audit_log.scenario, indent=2),
            f"\n{'=' * 80}",
            "POPULATED FIELDS",
            "=" * 80,
        ]
        
        # Add field details
        for field in audit_log.fields:
            report_lines.extend([
                f"\nRow {field.row}, Column {field.column}: {field.label}",
                f"  Value: {field.value:,.2f} {field.unit}",
                f"  Confidence: {field.confidence:.2%}"
            ])
        
        # Add justifications
        report_lines.extend([
            f"\n{'=' * 80}",
            "JUSTIFICATIONS",
            "=" * 80
        ])
        
        for just in audit_log.justifications:
            report_lines.extend([
                f"\nField: {just.field_id}",
                f"Reasoning: {just.reasoning}",
                f"Confidence: {just.confidence:.2%}",
                "Rule References:"
            ])
            
            for ref in just.rule_references:
                report_lines.extend([
                    f"  - {ref.source}, {ref.article}",
                    f"    Relevance: {ref.relevance_score:.2%}",
                    f"    Excerpt: {ref.text_excerpt[:100]}..."
                ])
        
        # Add validation results
        report_lines.extend([
            f"\n{'=' * 80}",
            "VALIDATION RESULTS",
            "=" * 80,
            f"\nStatus: {'PASSED' if audit_log.validation.is_valid else 'FAILED'}"
        ])
        
        if audit_log.validation.errors:
            report_lines.append("\nErrors:")
            for error in audit_log.validation.errors:
                report_lines.append(f"  ❌ {error.message} (Rule: {error.rule})")
        
        if audit_log.validation.warnings:
            report_lines.append("\nWarnings:")
            for warning in audit_log.validation.warnings:
                report_lines.append(f"  ⚠️  {warning.message}")
        
        report_lines.append("\n" + "=" * 80)
        
        return "\n".join(report_lines)
    
    def _save_audit_log(self, audit_log: AuditLog):
        """Save audit log to file."""
        log_file = self.log_directory / f"{audit_log.query_id}.json"
        
        # Convert to dict for JSON serialization
        log_data = audit_log.model_dump(mode='json')
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
