import os
from openai import OpenAI
from typing import Dict, Any, List
from app.config import settings
from app.models import COREPField, Justification, RuleReference
import json

class LLMService:
    """Service for LLM integration using GitHub Models."""
    
    def __init__(self):
        """Initialize GitHub Models client."""
        self.client = OpenAI(
            base_url=settings.github_endpoint,
            api_key=settings.github_token,
        )
        self.model_name = settings.model_name
    
    def generate_corep_output(
        self,
        user_query: str,
        scenario: Dict[str, Any],
        regulatory_context: str,
        template_id: str = "C_01_00"
    ) -> Dict[str, Any]:
        """
        Generate structured COREP output using LLM with function calling.
        
        Args:
            user_query: Natural language question
            scenario: Structured scenario parameters
            regulatory_context: Retrieved regulatory text
            template_id: COREP template identifier
            
        Returns:
            Dictionary containing fields and justifications
        """
        prompt = self._build_prompt(
            user_query, 
            scenario, 
            regulatory_context,
            template_id
        )
        
        # Define function schema for structured output
        function_schema = self._get_function_schema(template_id)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=[function_schema],
                tool_choice={"type": "function", "function": {"name": "populate_corep_template"}},
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            # Extract function call result
            if response.choices and len(response.choices) > 0 and response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                if tool_call.function.name == "populate_corep_template":
                    result = json.loads(tool_call.function.arguments)
                    return self._parse_llm_output(result)
            
            # Fallback if no tool call
            return self._create_empty_response()
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._create_empty_response()
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for LLM."""
        return """You are an expert in UK PRA regulatory reporting and COREP templates.

Your task is to analyze reporting scenarios and populate COREP template fields based on PRA Rulebook requirements.

Key responsibilities:
1. Carefully read the regulatory context and identify relevant rules
2. Map scenario details to appropriate COREP fields
3. Calculate values based on regulatory definitions
4. Provide rule references and reasoning for each field
5. Assign confidence scores (0-1) based on clarity of rules
6. Flag any missing information or ambiguities

Always ensure:
- Values are in GBP thousands
- Tier 1 capital = Common Equity Tier 1 + Additional Tier 1
- Total Own Funds = Tier 1 + Tier 2
- Confidence scores reflect certainty of interpretation
- Always use column '010' for amount fields in C 01.00
- Rule paragraphs can be strings or integers
"""
    
    def _build_prompt(
        self, 
        user_query: str, 
        scenario: Dict[str, Any],
        regulatory_context: str,
        template_id: str
    ) -> str:
        """Build prompt for LLM."""
        return f"""REGULATORY CONTEXT:
{regulatory_context}

USER QUERY:
{user_query}

SCENARIO DETAILS:
{json.dumps(scenario, indent=2)}

TEMPLATE: {template_id} (Own Funds)

TASK:
Analyze the scenario and populate the COREP Own Funds template fields. For each field you populate:
1. Calculate the value in GBP thousands
2. Identify which PRA Rulebook articles/paragraphs justify this value
3. Explain your reasoning
4. Assign a confidence score (0-1)

Focus on these key fields:
- Row 010: Total Own Funds
- Row 020: Tier 1 Capital
- Row 030: Common Equity Tier 1 (CET1)
- Row 040: Additional Tier 1 (AT1)
- Row 060: Tier 2 Capital

Use the populate_corep_template function to return your structured output."""
    
    def _get_function_schema(self, template_id: str) -> Dict[str, Any]:
        """Get function schema for structured output."""
        return {
            "type": "function",
            "function": {
                "name": "populate_corep_template",
                "description": "Populate COREP template fields with calculated values and justifications",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fields": {
                            "type": "array",
                            "description": "List of populated COREP fields",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "row": {"type": "string", "description": "Row identifier (e.g., '020')"},
                                    "column": {"type": "string", "description": "Column identifier (e.g., '010')"},
                                    "label": {"type": "string", "description": "Field label"},
                                    "value": {"type": "number", "description": "Value in GBP thousands"},
                                    "confidence": {"type": "number", "description": "Confidence score 0-1"}
                                },
                                "required": ["row", "column", "label", "value", "confidence"]
                            }
                        },
                        "justifications": {
                            "type": "array",
                            "description": "Justifications for each field",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field_id": {"type": "string", "description": "Field identifier (row_column)"},
                                    "reasoning": {"type": "string", "description": "Explanation of calculation"},
                                    "confidence": {"type": "number", "description": "Confidence score 0-1"},
                                    "rule_references": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "source": {"type": "string"},
                                                "article": {"type": "string"},
                                                "paragraph": {"type": "string"},
                                                "text_excerpt": {"type": "string"},
                                                "relevance_score": {"type": "number"}
                                            }
                                        }
                                    }
                                },
                                "required": ["field_id", "reasoning", "confidence", "rule_references"]
                            }
                        }
                    },
                    "required": ["fields", "justifications"]
                }
            }
        }
    
    def _parse_llm_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM output into structured format."""
        fields = []
        for field_data in result.get("fields", []):
            fields.append(COREPField(
                row=field_data["row"],
                column=field_data["column"],
                label=field_data["label"],
                value=field_data["value"],
                unit="GBP_thousands",
                confidence=field_data.get("confidence", 0.8)
            ))
        
        justifications = []
        for just_data in result.get("justifications", []):
            rule_refs = []
            for ref_data in just_data.get("rule_references", []):
                rule_refs.append(RuleReference(
                    source=ref_data.get("source", "PRA Rulebook"),
                    article=ref_data.get("article", "Unknown"),
                    paragraph=ref_data.get("paragraph"),
                    text_excerpt=ref_data.get("text_excerpt", ""),
                    relevance_score=ref_data.get("relevance_score", 0.8)
                ))
            
            justifications.append(Justification(
                field_id=just_data["field_id"],
                rule_references=rule_refs,
                reasoning=just_data["reasoning"],
                confidence=just_data.get("confidence", 0.8)
            ))
        
        return {
            "fields": fields,
            "justifications": justifications
        }
    
    def _create_empty_response(self) -> Dict[str, Any]:
        """Create empty response on error."""
        return {
            "fields": [],
            "justifications": []
        }
