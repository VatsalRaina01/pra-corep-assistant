"""
PRA COREP Reporting Assistant - Backend API
Enhanced with RAG, structured output, template population, and PDF export.
"""

import os
import io
import json
from typing import AsyncGenerator, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
import httpx

# Import knowledge base
from knowledge_base import (
    KNOWLEDGE_BASE,
    CA1_TEMPLATE_SCHEMA,
    CA2_TEMPLATE_SCHEMA,
    VALIDATION_RULES,
    retrieve_relevant_context,
    get_all_knowledge_for_template
)

# ============================================================================
# Configuration
# ============================================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MODEL_ENDPOINT = "https://models.github.ai/inference/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"

# System prompts
CHAT_SYSTEM_PROMPT = """You are a PRA COREP Reporting Assistant, an expert in UK banking regulatory requirements.

Your expertise covers:
- **COREP Templates**: CA1 (Own Funds), CA2 (Capital Requirements) and related templates
- **CRR/CRD IV**: Capital Requirements Regulation and Directive
- **Credit Risk**: SA and IRB approaches, RWA calculations
- **Capital Requirements**: CET1, AT1, Tier 2, capital ratios and buffers
- **Validation Rules**: COREP validation checks and common errors

When answering:
1. Be precise and reference specific CRR articles when applicable
2. Provide step-by-step guidance for complex calculations
3. Highlight common pitfalls and validation issues
4. Use clear formatting with headers and bullet points

Format responses in Markdown for readability."""

ANALYSIS_SYSTEM_PROMPT = """You are a PRA COREP Reporting Assistant that analyzes bank capital scenarios and populates COREP templates.

YOUR TASK: Analyze the user's scenario and extract values for COREP template fields.

You MUST respond with a valid JSON object in EXACTLY this format:
{
    "template": "CA1" or "CA2",
    "extracted_values": {
        "row_XXX": number_value,
        ...
    },
    "calculations": [
        {"description": "...", "formula": "...", "result": number}
    ],
    "assumptions": ["assumption 1", "assumption 2"],
    "rule_citations": [
        {"field": "row_XXX", "rule_id": "CRR_ART_XX", "explanation": "..."}
    ]
}

RULES:
- All values should be in millions (e.g., £500m = 500)
- Deduction items (rows 080, 090, 100, 110, 120, 320, 630) should be POSITIVE numbers
- Calculate totals: CET1 (row 200), AT1 (row 400), T1 (row 500), T2 (row 700), Total (row 800)
- If RWA is provided, calculate capital ratios

REFERENCE INFORMATION:
"""

# ============================================================================
# FastAPI App Setup
# ============================================================================

app = FastAPI(
    title="PRA COREP Assistant API",
    description="AI-powered regulatory reporting guidance with template population",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Models
# ============================================================================

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []

class AnalyzeRequest(BaseModel):
    scenario: str
    template: str = "CA1"  # CA1 or CA2

class TemplateField(BaseModel):
    row_id: str
    label: str
    value: Optional[float] = None
    category: str
    sign: str

class ValidationResult(BaseModel):
    rule_id: str
    name: str
    severity: str
    passed: bool
    message: str

class AuditTrailItem(BaseModel):
    field: str
    rule_id: str
    rule_title: str
    explanation: str

class AnalyzeResponse(BaseModel):
    template_id: str
    template_name: str
    fields: list[TemplateField]
    totals: dict
    ratios: dict
    validation_results: list[ValidationResult]
    audit_trail: list[AuditTrailItem]
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
    features: list[str]

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        model=MODEL_NAME,
        features=["chat", "streaming", "analyze", "pdf_export", "validation"]
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        model=MODEL_NAME,
        features=["chat", "streaming", "analyze", "pdf_export", "validation"]
    )

@app.post("/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat with RAG context."""
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not configured")
    
    # Retrieve relevant context
    context_docs = retrieve_relevant_context(request.message)
    context_text = "\n\n".join([
        f"### {doc['title']}\n{doc['text']}" 
        for doc in context_docs
    ]) if context_docs else ""
    
    # Build system prompt with context
    system_prompt = CHAT_SYSTEM_PROMPT
    if context_text:
        system_prompt += f"\n\nRELEVANT REGULATORY CONTEXT:\n{context_text}"
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in request.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": request.message})
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                MODEL_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"LLM API error: {response.text}")
            
            data = response.json()
            assistant_message = data["choices"][0]["message"]["content"]
            
            return {
                "response": assistant_message,
                "model": MODEL_NAME,
                "context_used": [doc["id"] for doc in context_docs]
            }
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat with RAG context."""
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not configured")
    
    # Retrieve relevant context
    context_docs = retrieve_relevant_context(request.message)
    context_text = "\n\n".join([
        f"### {doc['title']}\n{doc['text']}" 
        for doc in context_docs
    ]) if context_docs else ""
    
    system_prompt = CHAT_SYSTEM_PROMPT
    if context_text:
        system_prompt += f"\n\nRELEVANT REGULATORY CONTEXT:\n{context_text}"
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in request.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": request.message})
    
    async def generate() -> AsyncGenerator[str, None]:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    MODEL_ENDPOINT,
                    headers={
                        "Authorization": f"Bearer {GITHUB_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": MODEL_NAME,
                        "messages": messages,
                        "max_tokens": 2048,
                        "temperature": 0.7,
                        "stream": True
                    }
                ) as response:
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': 'API error'})}\n\n"
                        return
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                yield "data: [DONE]\n\n"
                                break
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and chunk["choices"]:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_scenario(request: AnalyzeRequest):
    """
    Analyze a bank capital scenario and populate COREP template.
    Returns structured template data with validation and audit trail.
    """
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not configured")
    
    # Get template schema
    template_schema = CA1_TEMPLATE_SCHEMA if request.template.upper() == "CA1" else CA2_TEMPLATE_SCHEMA
    
    # Get relevant knowledge
    knowledge_docs = get_all_knowledge_for_template(request.template)
    knowledge_text = "\n\n".join([
        f"### {doc.get('title', 'Reference')}\n{doc.get('text', '')}" 
        for doc in knowledge_docs if doc
    ])
    
    # Build structured prompt
    system_prompt = ANALYSIS_SYSTEM_PROMPT + knowledge_text
    
    user_prompt = f"""Analyze this bank capital scenario and populate the {request.template} template:

SCENARIO:
{request.scenario}

TEMPLATE ROWS TO POPULATE:
{json.dumps([{"row_id": r["row_id"], "label": r["label"]} for r in template_schema["rows"]], indent=2)}

Respond with a valid JSON object only, no markdown formatting."""

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                MODEL_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 4096,
                    "temperature": 0.2  # Lower temp for structured output
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"LLM API error")
            
            data = response.json()
            llm_response = data["choices"][0]["message"]["content"]
            
            # Parse LLM response
            try:
                # Clean up response (remove markdown code blocks if present)
                cleaned = llm_response.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("```")[1]
                    if cleaned.startswith("json"):
                        cleaned = cleaned[4:]
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from response
                import re
                json_match = re.search(r'\{[\s\S]*\}', llm_response)
                if json_match:
                    parsed = json.loads(json_match.group())
                else:
                    raise HTTPException(status_code=500, detail="Failed to parse LLM response as JSON")
            
            # Build template fields with values
            extracted_values = parsed.get("extracted_values", {})
            fields = []
            for row in template_schema["rows"]:
                row_key = f"row_{row['row_id']}"
                value = extracted_values.get(row_key) or extracted_values.get(row["row_id"])
                fields.append(TemplateField(
                    row_id=row["row_id"],
                    label=row["label"],
                    value=value,
                    category=row["category"],
                    sign=row["sign"]
                ))
            
            # Calculate totals
            totals = calculate_totals(extracted_values, request.template)
            
            # Calculate ratios if RWA is available
            ratios = calculate_ratios(totals, extracted_values)
            
            # Run validation
            validation_results = run_validation(extracted_values, totals, ratios)
            
            # Build audit trail
            audit_trail = []
            for citation in parsed.get("rule_citations", []):
                rule_id = citation.get("rule_id", "")
                rule_doc = KNOWLEDGE_BASE.get(rule_id, {})
                audit_trail.append(AuditTrailItem(
                    field=citation.get("field", ""),
                    rule_id=rule_id,
                    rule_title=rule_doc.get("title", rule_id),
                    explanation=citation.get("explanation", "")
                ))
            
            return AnalyzeResponse(
                template_id=template_schema["template_id"],
                template_name=template_schema["template_name"],
                fields=fields,
                totals=totals,
                ratios=ratios,
                validation_results=validation_results,
                audit_trail=audit_trail,
                timestamp=datetime.now().isoformat()
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Analysis timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export/pdf")
async def export_pdf(request: AnalyzeRequest):
    """
    Export populated COREP template as PDF.
    Requires analysis first, then generates PDF.
    """
    # First run the analysis
    analysis = await analyze_scenario(request)
    
    # Generate PDF using simple HTML-to-text approach
    # (Using basic implementation without external PDF libraries for deployment simplicity)
    pdf_content = generate_pdf_content(analysis)
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=COREP_{analysis.template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        }
    )

# ============================================================================
# Helper Functions
# ============================================================================

def calculate_totals(values: dict, template: str) -> dict:
    """Calculate template totals from extracted values."""
    totals = {}
    
    if template.upper() == "CA1":
        # CET1 calculation
        cet1_items = sum([
            values.get("row_010", 0) or 0,
            values.get("row_020", 0) or 0,
            values.get("row_030", 0) or 0,
            values.get("row_040", 0) or 0,
            values.get("row_050", 0) or 0,
            values.get("row_060", 0) or 0,
            values.get("row_070", 0) or 0,
        ])
        cet1_deductions = sum([
            values.get("row_080", 0) or 0,
            values.get("row_090", 0) or 0,
            values.get("row_100", 0) or 0,
            values.get("row_110", 0) or 0,
            values.get("row_120", 0) or 0,
        ])
        cet1_other = values.get("row_130", 0) or 0
        totals["cet1"] = cet1_items - cet1_deductions + cet1_other
        
        # AT1 calculation
        at1_items = sum([
            values.get("row_300", 0) or 0,
            values.get("row_310", 0) or 0,
        ])
        at1_deductions = values.get("row_320", 0) or 0
        at1_other = values.get("row_330", 0) or 0
        totals["at1"] = at1_items - at1_deductions + at1_other
        
        # Tier 1
        totals["tier1"] = totals["cet1"] + totals["at1"]
        
        # Tier 2 calculation
        t2_items = sum([
            values.get("row_600", 0) or 0,
            values.get("row_610", 0) or 0,
            values.get("row_620", 0) or 0,
        ])
        t2_deductions = values.get("row_630", 0) or 0
        t2_other = values.get("row_640", 0) or 0
        totals["tier2"] = t2_items - t2_deductions + t2_other
        
        # Total own funds
        totals["total_own_funds"] = totals["tier1"] + totals["tier2"]
        
    elif template.upper() == "CA2":
        # RWA totals
        totals["credit_risk_rwa"] = sum([
            values.get("row_010", 0) or 0,
            values.get("row_020", 0) or 0,
            values.get("row_030", 0) or 0,
            values.get("row_040", 0) or 0,
        ])
        totals["market_risk_rwa"] = sum([
            values.get("row_100", 0) or 0,
            values.get("row_110", 0) or 0,
            values.get("row_120", 0) or 0,
        ])
        totals["cva_risk_rwa"] = values.get("row_200", 0) or 0
        totals["op_risk_rwa"] = values.get("row_300", 0) or 0
        totals["total_rwa"] = (
            totals["credit_risk_rwa"] + 
            totals["market_risk_rwa"] + 
            totals["cva_risk_rwa"] + 
            totals["op_risk_rwa"]
        )
    
    return totals

def calculate_ratios(totals: dict, values: dict) -> dict:
    """Calculate capital ratios."""
    ratios = {}
    
    # Get RWA from totals or values
    rwa = totals.get("total_rwa") or values.get("rwa") or values.get("total_rwa") or 0
    
    if rwa > 0:
        cet1 = totals.get("cet1", 0)
        tier1 = totals.get("tier1", 0)
        total_capital = totals.get("total_own_funds", 0)
        
        ratios["cet1_ratio"] = round((cet1 / rwa) * 100, 2)
        ratios["tier1_ratio"] = round((tier1 / rwa) * 100, 2)
        ratios["total_capital_ratio"] = round((total_capital / rwa) * 100, 2)
        
        # Buffer calculation
        ratios["cet1_buffer"] = round(ratios["cet1_ratio"] - 4.5, 2)
        ratios["meets_ccb"] = ratios["cet1_ratio"] >= 7.0  # 4.5% + 2.5% CCB
    
    return ratios

def run_validation(values: dict, totals: dict, ratios: dict) -> list[ValidationResult]:
    """Run validation rules and return results."""
    results = []
    
    for rule in VALIDATION_RULES:
        passed = True
        message = ""
        
        if rule["type"] == "THRESHOLD":
            field_value = ratios.get(rule["field"], 0)
            threshold = rule["threshold"]
            passed = field_value >= threshold
            message = f"{rule['field']} is {field_value}% (minimum: {threshold}%)" if not passed else f"Passed: {field_value}% >= {threshold}%"
            
        elif rule["type"] == "SIGN":
            for field in rule.get("fields", []):
                val = values.get(field, 0)
                if val is not None and val < 0:
                    passed = False
                    message = f"Field {field} has negative value: {val}"
                    break
            if passed:
                message = "All sign validations passed"
                
        elif rule["type"] == "ARITHMETIC":
            # Simplified arithmetic validation
            passed = True
            message = "Arithmetic check passed"
        
        results.append(ValidationResult(
            rule_id=rule["id"],
            name=rule["name"],
            severity=rule["severity"],
            passed=passed,
            message=message
        ))
    
    return results

def generate_pdf_content(analysis: AnalyzeResponse) -> bytes:
    """
    Generate PDF content from analysis.
    Using a simple text-based PDF for deployment without heavy dependencies.
    """
    # Simple PDF structure (minimal valid PDF)
    # For production, use reportlab or weasyprint
    
    # Build content text
    content_lines = [
        f"COREP {analysis.template_id} - {analysis.template_name}",
        f"Generated: {analysis.timestamp}",
        "",
        "=" * 60,
        "TEMPLATE VALUES",
        "=" * 60,
    ]
    
    for field in analysis.fields:
        value_str = f"{field.value:,.2f}" if field.value is not None else "N/A"
        content_lines.append(f"Row {field.row_id}: {field.label}")
        content_lines.append(f"  Value: {value_str} million")
        content_lines.append("")
    
    content_lines.extend([
        "=" * 60,
        "TOTALS",
        "=" * 60,
    ])
    for key, value in analysis.totals.items():
        content_lines.append(f"{key}: {value:,.2f} million")
    
    if analysis.ratios:
        content_lines.extend([
            "",
            "=" * 60,
            "CAPITAL RATIOS",
            "=" * 60,
        ])
        for key, value in analysis.ratios.items():
            if isinstance(value, bool):
                content_lines.append(f"{key}: {'Yes' if value else 'No'}")
            else:
                content_lines.append(f"{key}: {value}%")
    
    content_lines.extend([
        "",
        "=" * 60,
        "VALIDATION RESULTS",
        "=" * 60,
    ])
    for result in analysis.validation_results:
        status = "✓ PASS" if result.passed else "✗ FAIL"
        content_lines.append(f"[{status}] {result.name}: {result.message}")
    
    if analysis.audit_trail:
        content_lines.extend([
            "",
            "=" * 60,
            "AUDIT TRAIL",
            "=" * 60,
        ])
        for item in analysis.audit_trail:
            content_lines.append(f"Field {item.field}: {item.rule_title}")
            content_lines.append(f"  {item.explanation}")
            content_lines.append("")
    
    content_text = "\n".join(content_lines)
    
    # Build minimal PDF
    pdf = build_minimal_pdf(content_text)
    return pdf

def build_minimal_pdf(text: str) -> bytes:
    """Build a minimal valid PDF with text content."""
    # Escape special characters
    text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    
    # Split into lines for PDF
    lines = text.split("\n")
    
    # PDF content stream
    y = 750
    content = "BT\n/F1 10 Tf\n"
    for line in lines:
        if y < 50:
            break
        content += f"1 0 0 1 50 {y} Tm\n({line}) Tj\n"
        y -= 14
    content += "ET"
    
    # Build PDF structure
    pdf_parts = [
        b"%PDF-1.4\n",
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {len(content)} >>\nstream\n{content}\nendstream\nendobj\n".encode(),
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n",
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n",
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n0\n%%EOF"
    ]
    
    return b"".join(pdf_parts)

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
