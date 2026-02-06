from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.config import settings
from app.models import QueryRequest, COREPResponse
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.services.llm_service_streaming import LLMServiceStreaming
from app.services.validation_service import ValidationService
from app.services.audit_service import AuditService
import uuid
import json
from datetime import datetime

app = FastAPI(
    title="PRA COREP Assistant API",
    description="LLM-assisted regulatory reporting assistant for COREP templates",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_service = RAGService()
llm_service = LLMService()
llm_service_streaming = LLMServiceStreaming()
audit_service = AuditService()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PRA COREP Assistant API",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "RAG-based retrieval",
            "GitHub Models LLM",
            "Streaming responses",
            "Chain-of-thought reasoning",
            "Validation engine",
            "Audit logging"
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/query", response_model=COREPResponse)
async def process_query(request: QueryRequest):
    """
    Main endpoint: Process user query and generate COREP output.
    
    Request:
    - user_query: Natural language question
    - scenario: Structured scenario parameters
    - template_id: Which COREP template to populate
    
    Response:
    - query_id: Unique identifier
    - template_id: Template identifier
    - fields: Populated COREP fields
    - justifications: Rule-based justifications
    - validation: Validation results
    """
    try:
        # Generate unique query ID
        query_id = str(uuid.uuid4())
        
        # 1. Retrieve relevant regulatory text
        print(f"[{query_id}] Retrieving regulatory context...")
        documents = rag_service.retrieve_relevant_rules(
            query=request.user_query,
            template_filter=request.template_id,
            top_k=5
        )
        regulatory_context = rag_service.format_context_for_llm(documents)
        
        # 2. Generate structured output with LLM
        print(f"[{query_id}] Generating COREP output with LLM...")
        llm_output = llm_service.generate_corep_output(
            user_query=request.user_query,
            scenario=request.scenario,
            regulatory_context=regulatory_context,
            template_id=request.template_id
        )
        
        fields = llm_output.get("fields", [])
        justifications = llm_output.get("justifications", [])
        
        # 3. Validate output
        print(f"[{query_id}] Validating output...")
        validation_service = ValidationService(template_id=request.template_id)
        validation_results = validation_service.validate_output(fields)
        
        # 4. Create audit log
        print(f"[{query_id}] Creating audit log...")
        audit_log = audit_service.create_audit_log(
            query_id=query_id,
            user_query=request.user_query,
            scenario=request.scenario,
            template_id=request.template_id,
            fields=fields,
            justifications=justifications,
            validation=validation_results,
            llm_metadata={
                "model": settings.model_name,
                "temperature": settings.temperature,
                "retrieved_documents": len(documents)
            }
        )
        
        print(f"[{query_id}] Query processed successfully")
        
        return COREPResponse(
            query_id=query_id,
            template_id=request.template_id,
            fields=fields,
            justifications=justifications,
            validation=validation_results,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/api/query/stream")
async def process_query_streaming(request: QueryRequest):
    """
    Streaming endpoint: Process user query with real-time updates.
    
    Returns Server-Sent Events (SSE) with progress updates and partial results.
    """
    async def event_generator():
        try:
            query_id = str(uuid.uuid4())
            
            # Send initial event
            yield f"data: {json.dumps({'type': 'start', 'query_id': query_id, 'progress': 0})}\n\n"
            
            # 1. Retrieve regulatory context
            yield f"data: {json.dumps({'type': 'status', 'message': 'Retrieving regulatory context...', 'progress': 10})}\n\n"
            
            documents = rag_service.retrieve_relevant_rules(
                query=request.user_query,
                template_filter=request.template_id,
                top_k=5
            )
            regulatory_context = rag_service.format_context_for_llm(documents)
            
            yield f"data: {json.dumps({'type': 'status', 'message': f'Retrieved {len(documents)} regulatory documents', 'progress': 20})}\n\n"
            
            # 2. Stream LLM generation
            async for update in llm_service_streaming.generate_corep_output_streaming(
                user_query=request.user_query,
                scenario=request.scenario,
                regulatory_context=regulatory_context,
                template_id=request.template_id
            ):
                # Convert Pydantic models to dicts for JSON serialization
                if update.get("type") == "complete":
                    data = update["data"]
                    serialized_data = {
                        "reasoning_steps": data.get("reasoning_steps", {}),
                        "fields": [f.model_dump() for f in data.get("fields", [])],
                        "justifications": [j.model_dump() for j in data.get("justifications", [])]
                    }
                    update["data"] = serialized_data
                
                yield f"data: {json.dumps(update)}\n\n"
                
                # If complete, run validation
                if update.get("type") == "complete":
                    fields = update["data"]["fields"]
                    justifications = update["data"]["justifications"]
                    
                    # Convert back to Pydantic models for validation
                    from app.models import COREPField, Justification
                    field_objects = [COREPField(**f) for f in fields]
                    
                    yield f"data: {json.dumps({'type': 'status', 'message': 'Validating output...', 'progress': 95})}\n\n"
                    
                    validation_service = ValidationService(template_id=request.template_id)
                    validation_results = validation_service.validate_output(field_objects)
                    
                    yield f"data: {json.dumps({'type': 'validation', 'data': validation_results.model_dump(), 'progress': 98})}\n\n"
                    
                    # Create audit log (don't block on this)
                    just_objects = [Justification(**j) for j in justifications]
                    audit_service.create_audit_log(
                        query_id=query_id,
                        user_query=request.user_query,
                        scenario=request.scenario,
                        template_id=request.template_id,
                        fields=field_objects,
                        justifications=just_objects,
                        validation=validation_results,
                        llm_metadata={
                            "model": settings.model_name,
                            "streaming": True
                        }
                    )
                    
                    yield f"data: {json.dumps({'type': 'done', 'query_id': query_id, 'progress': 100})}\n\n"
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/templates")
async def list_templates():
    """List available COREP templates."""
    return {
        "templates": [
            {
                "id": "C_01_00",
                "name": "Own Funds",
                "description": "Template for reporting own funds composition (Tier 1, Tier 2)",
                "features": [
                    "Streaming support",
                    "Chain-of-thought reasoning",
                    "Automated validation",
                    "Audit trail"
                ]
            }
        ]
    }

@app.get("/api/audit/{query_id}")
async def get_audit_log(query_id: str):
    """Retrieve audit log for a specific query."""
    try:
        audit_log = audit_service.get_audit_log(query_id)
        return audit_log
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Audit log not found: {query_id}"
        )

@app.get("/api/audit/{query_id}/report")
async def get_audit_report(query_id: str):
    """Get human-readable audit report."""
    try:
        report = audit_service.generate_audit_report(query_id)
        return {"query_id": query_id, "report": report}
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Error generating report: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
