"""
Complete End-to-End Demo with Mock Data
Demonstrates the full COREP Assistant workflow without requiring GitHub token
"""

import sys
sys.path.insert(0, '.')

from app.models import QueryRequest
from app.services.rag_service import RAGService
from app.services.mock_llm_service import MockLLMService
from app.services.validation_service import ValidationService
from app.services.audit_service import AuditService
import json
from datetime import datetime

print("=" * 80)
print("PRA COREP ASSISTANT - END-TO-END DEMONSTRATION")
print("=" * 80)
print()

# Scenario 1: Basic Tier 1 Capital
print("📊 SCENARIO 1: Basic Tier 1 Capital Reporting")
print("-" * 80)

scenario1 = {
    "entity_type": "UK bank",
    "ordinary_shares": 500,  # £500M
    "retained_earnings": 100,  # £100M
    "additional_tier1": 0,
    "tier2_capital": 0,
    "currency": "GBP"
}

query1 = "How should we report Tier 1 capital for our UK subsidiary?"

print(f"Query: {query1}")
print(f"Scenario: Ordinary Shares: £{scenario1['ordinary_shares']}M, Retained Earnings: £{scenario1['retained_earnings']}M")
print()

# Step 1: RAG Retrieval
print("🔍 Step 1: Retrieving regulatory context...")
try:
    rag_service = RAGService()
    documents = rag_service.retrieve_relevant_rules(
        query=query1,
        template_filter="C_01_00",
        top_k=3
    )
    print(f"✅ Retrieved {len(documents)} relevant regulatory documents")
    for i, doc in enumerate(documents[:2], 1):
        print(f"   {i}. {doc['metadata'].get('article', 'Unknown')} (relevance: {doc['relevance_score']:.2f})")
except Exception as e:
    print(f"⚠️  RAG service not initialized, using fallback context")
    documents = []

regulatory_context = rag_service.format_context_for_llm(documents) if documents else "PRA Rulebook context"
print()

# Step 2: LLM Generation (Mock)
print("🧠 Step 2: Generating COREP output with chain-of-thought reasoning...")
mock_llm = MockLLMService()
llm_output = mock_llm.generate_corep_output(
    user_query=query1,
    scenario=scenario1,
    regulatory_context=regulatory_context,
    template_id="C_01_00"
)

print("✅ Generated structured output")
print()

# Display Chain-of-Thought Reasoning
print("💭 Chain-of-Thought Reasoning:")
print("-" * 80)
reasoning = llm_output.get("reasoning_steps", {})

print("\n🔍 STEP 1 - ANALYSIS:")
print(reasoning.get("analysis", "N/A"))

print("\n🧮 STEP 2 - CALCULATION:")
print(reasoning.get("calculation", "N/A"))

print("\n📋 STEP 3 - JUSTIFICATION:")
print(reasoning.get("justification", "N/A"))

print("\n✅ STEP 4 - VERIFICATION:")
print(reasoning.get("verification", "N/A"))
print()

# Step 3: Display Populated Template
print("📄 Populated COREP Template (C 01.00 - Own Funds):")
print("-" * 80)
fields = llm_output.get("fields", [])
for field in fields:
    confidence_icon = "🟢" if field.confidence >= 0.9 else "🟡" if field.confidence >= 0.8 else "🔴"
    print(f"{confidence_icon} Row {field.row}: {field.label}")
    print(f"   Value: £{field.value:,}k | Confidence: {field.confidence:.0%}")
print()

# Step 4: Validation
print("✅ Step 3: Validating output...")
validation_service = ValidationService(template_id="C_01_00")
validation_results = validation_service.validate_output(fields)

if validation_results.is_valid:
    print("✅ All validation checks passed!")
else:
    print(f"⚠️  Validation found {len(validation_results.errors)} error(s)")
    for error in validation_results.errors:
        print(f"   ❌ {error.message}")

if validation_results.warnings:
    print(f"⚠️  {len(validation_results.warnings)} warning(s):")
    for warning in validation_results.warnings:
        print(f"   ⚠️  {warning.message}")
print()

# Step 5: Audit Trail
print("📋 Audit Trail:")
print("-" * 80)
justifications = llm_output.get("justifications", [])
for just in justifications[:2]:  # Show first 2 for brevity
    print(f"\n🔹 Field: {just.field_id}")
    print(f"   Reasoning: {just.reasoning[:150]}...")
    print(f"   Confidence: {just.confidence:.0%}")
    print(f"   Rule References: {len(just.rule_references)} citation(s)")
    for ref in just.rule_references[:1]:
        print(f"      • {ref.source} - {ref.article} (relevance: {ref.relevance_score:.0%})")
print()

# Scenario 2: Full Capital Stack
print("\n" + "=" * 80)
print("📊 SCENARIO 2: Full Capital Stack with Tier 2")
print("-" * 80)

scenario2 = {
    "entity_type": "UK bank",
    "ordinary_shares": 500,
    "retained_earnings": 100,
    "additional_tier1": 50,
    "tier2_capital": 100,
    "currency": "GBP"
}

query2 = "Calculate our complete regulatory capital structure including Tier 2"

print(f"Query: {query2}")
print(f"Scenario: Ordinary Shares: £{scenario2['ordinary_shares']}M, Retained: £{scenario2['retained_earnings']}M, AT1: £{scenario2['additional_tier1']}M, Tier 2: £{scenario2['tier2_capital']}M")
print()

llm_output2 = mock_llm.generate_corep_output(
    user_query=query2,
    scenario=scenario2,
    regulatory_context=regulatory_context,
    template_id="C_01_00"
)

print("📄 Populated Template:")
print("-" * 80)
fields2 = llm_output2.get("fields", [])
for field in fields2:
    print(f"Row {field.row}: {field.label:30s} = £{field.value:>10,}k ({field.confidence:.0%})")
print()

validation_results2 = validation_service.validate_output(fields2)
print(f"Validation: {'✅ PASSED' if validation_results2.is_valid else '❌ FAILED'}")
if not validation_results2.is_valid:
    for error in validation_results2.errors:
        print(f"   ❌ {error.message}")
print()

# Scenario 3: Invalid Data (Demonstrates Error Detection)
print("\n" + "=" * 80)
print("📊 SCENARIO 3: Error Detection Demo")
print("-" * 80)

scenario3 = {
    "entity_type": "UK bank",
    "ordinary_shares": 300,
    "retained_earnings": 100,
    "additional_tier1": 0,
    "tier2_capital": 200,  # This will exceed 1/3 of Tier 1
    "currency": "GBP"
}

print(f"Scenario: Tier 2 (£200M) exceeds 1/3 of Tier 1 (£400M)")
print()

llm_output3 = mock_llm.generate_corep_output(
    user_query="Report capital with excessive Tier 2",
    scenario=scenario3,
    regulatory_context=regulatory_context,
    template_id="C_01_00"
)

fields3 = llm_output3.get("fields", [])
validation_results3 = validation_service.validate_output(fields3)

print(f"Validation: {'✅ PASSED' if validation_results3.is_valid else '❌ FAILED (as expected)'}")
if not validation_results3.is_valid:
    print("\n🔍 Detected Errors:")
    for error in validation_results3.errors:
        print(f"   ❌ {error.message}")
print()

# Summary
print("=" * 80)
print("DEMONSTRATION SUMMARY")
print("=" * 80)
print()
print("✅ Successfully demonstrated:")
print("   1. RAG-based regulatory text retrieval")
print("   2. LLM output generation with chain-of-thought reasoning")
print("   3. COREP template population with confidence scores")
print("   4. Multi-level validation (type, consistency, business rules)")
print("   5. Complete audit trail with regulatory citations")
print("   6. Error detection for invalid data")
print()
print("📊 Test Scenarios:")
print(f"   • Scenario 1: Basic Tier 1 - {len(fields)} fields populated")
print(f"   • Scenario 2: Full capital stack - {len(fields2)} fields populated")
print(f"   • Scenario 3: Error detection - {len(validation_results3.errors)} error(s) caught")
print()
print("🎯 Key Features Demonstrated:")
print("   ⚡ Streaming-ready architecture")
print("   🧠 Chain-of-thought reasoning (4 steps)")
print("   ✅ Comprehensive validation engine")
print("   📋 Complete audit trail")
print("   🎨 Confidence scoring")
print()
print("=" * 80)
print("Demo complete! This shows the full workflow without requiring GitHub token.")
print("=" * 80)
