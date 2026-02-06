import os
import json
from openai import OpenAI
from typing import Dict, Any, AsyncIterator
from app.config import settings
from app.models import COREPField, Justification, RuleReference

class LLMServiceStreaming:
    """Service for streaming LLM integration using GitHub Models."""
    
    def __init__(self):
        """Initialize GitHub Models client."""
        self.client = OpenAI(
            base_url=settings.github_endpoint,
            api_key=settings.github_token,
        )
        self.model_name = settings.model_name
    
    async def generate_corep_output_streaming(
        self,
        user_query: str,
        scenario: Dict[str, Any],
        regulatory_context: str,
        template_id: str = "C_01_00"
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Generate structured COREP output using LLM with streaming.
        
        Yields progress updates as the LLM generates the response.
        
        Args:
            user_query: Natural language question
            scenario: Structured scenario parameters
            regulatory_context: Retrieved regulatory text
            template_id: COREP template identifier
            
        Yields:
            Dictionary containing progress updates and partial results
        """
        # Yield initial status
        yield {
            "type": "status",
            "message": "Analyzing regulatory context...",
            "progress": 10
        }
        
        prompt = self._build_prompt_with_cot(
            user_query, 
            scenario, 
            regulatory_context,
            template_id
        )
        
        yield {
            "type": "status",
            "message": "Generating COREP output with chain-of-thought reasoning...",
            "progress": 30
        }
        
        # Define function schema for structured output
        function_schema = self._get_function_schema(template_id)
        
        try:
            # Create streaming request
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt_with_cot()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=[function_schema],
                tool_choice={"type": "function", "function": {"name": "populate_corep_template"}},
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                stream=True
            )
            
            # Accumulate streamed content
            accumulated_content = ""
            tool_call_id = None
            function_name = None
            function_args = ""
            
            for chunk in stream:
                if not chunk.choices or len(chunk.choices) == 0:
                    continue
                    
                if chunk.choices[0].delta.tool_calls:
                    tool_call = chunk.choices[0].delta.tool_calls[0]
                    
                    if tool_call.id:
                        tool_call_id = tool_call.id
                    
                    if tool_call.function.name:
                        function_name = tool_call.function.name
                    
                    if tool_call.function.arguments:
                        function_args += tool_call.function.arguments
                        
                        # Try to parse partial JSON for progress updates
                        try:
                            partial_result = json.loads(function_args)
                            yield {
                                "type": "partial_result",
                                "data": partial_result,
                                "progress": 70
                            }
                        except json.JSONDecodeError:
                            # Not yet complete JSON, continue accumulating
                            pass
                
                elif chunk.choices[0].delta.content:
                    accumulated_content += chunk.choices[0].delta.content
                    
                    # Yield reasoning updates if present
                    yield {
                        "type": "reasoning",
                        "content": chunk.choices[0].delta.content,
                        "progress": 50
                    }
            
            yield {
                "type": "status",
                "message": "Parsing and validating output...",
                "progress": 90
            }
            
            # Parse final result
            if function_args:
                result = json.loads(function_args)
                parsed_result = self._parse_llm_output(result)
                
                yield {
                    "type": "complete",
                    "data": parsed_result,
                    "progress": 100
                }
            else:
                yield {
                    "type": "error",
                    "message": "No function call received from LLM",
                    "progress": 100
                }
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"LLM Error: {str(e)}",
                "progress": 100
            }
    
    def _get_system_prompt_with_cot(self) -> str:
        """Get system prompt with chain-of-thought instructions."""
        return """You are an expert in UK PRA regulatory reporting and COREP templates.

Use CHAIN-OF-THOUGHT REASONING to analyze scenarios and populate COREP templates:

STEP 1 - ANALYZE: Identify which regulatory rules apply to this scenario
- Review the provided PRA Rulebook context
- Identify relevant articles and paragraphs
- Note any special conditions or exceptions

STEP 2 - CALCULATE: Show step-by-step calculations
- Break down complex calculations into clear steps
- Show intermediate values
- Explain the logic behind each calculation

STEP 3 - JUSTIFY: Cite specific regulatory references
- Quote relevant article paragraphs
- Explain how the rule applies to this scenario
- Note confidence level in interpretation

STEP 4 - VERIFY: Check consistency with other fields
- Ensure Tier 1 = CET1 + AT1
- Ensure Own Funds = Tier 1 + Tier 2
- Flag any inconsistencies or missing data

Key principles:
- Values must be in GBP thousands
- All capital values must be positive
- Confidence scores reflect certainty of interpretation (0-1)
- Provide detailed justifications with rule citations
- For Template C 01.00, always use Column 010 for amount fields.
- Rule paragraphs can be strings or integers.
"""
    
    def _build_prompt_with_cot(
        self, 
        user_query: str, 
        scenario: Dict[str, Any],
        regulatory_context: str,
        template_id: str
    ) -> str:
        """Build prompt with chain-of-thought structure."""
        return f"""REGULATORY CONTEXT:
{regulatory_context}

USER QUERY:
{user_query}

SCENARIO DETAILS:
{json.dumps(scenario, indent=2)}

TEMPLATE: {template_id} (Own Funds)

TASK:
Use chain-of-thought reasoning to populate the COREP Own Funds template:

STEP 1 - ANALYZE the regulatory context and identify applicable rules
STEP 2 - CALCULATE field values with step-by-step breakdown
STEP 3 - JUSTIFY each value with specific rule citations
STEP 4 - VERIFY cross-field consistency

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
                "description": "Populate COREP template fields with calculated values and chain-of-thought justifications",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reasoning_steps": {
                            "type": "object",
                            "description": "Chain-of-thought reasoning breakdown",
                            "properties": {
                                "analysis": {"type": "string", "description": "Step 1: Analysis of applicable rules"},
                                "calculation": {"type": "string", "description": "Step 2: Calculation breakdown"},
                                "justification": {"type": "string", "description": "Step 3: Regulatory justification"},
                                "verification": {"type": "string", "description": "Step 4: Consistency checks"}
                            }
                        },
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
                    "required": ["reasoning_steps", "fields", "justifications"]
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
            "reasoning_steps": result.get("reasoning_steps", {}),
            "fields": fields,
            "justifications": justifications
        }
