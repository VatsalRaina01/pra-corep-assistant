# PRA COREP Reporting Assistant

> **LLM-assisted prototype for UK banking regulatory reporting**

An AI-powered assistant that helps analysts prepare COREP regulatory returns by interpreting PRA Rulebook requirements and automatically populating template fields with audit trails.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://pra-corep-web.onrender.com)
[![API Status](https://img.shields.io/badge/api-healthy-blue)](https://pra-corep-api.onrender.com/health)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://python.org)

---

## 🎯 Problem Statement

UK Banks subject to the **PRA Rulebook** must submit COREP regulatory returns that accurately reflect their capital, risk exposures and prudential metrics. Preparing these returns is:

- **Labour-intensive**: Analysts must interpret dense, frequently updated rules
- **Error-prone**: Complex mappings between regulations and template fields
- **Time-consuming**: Manual cross-referencing of EBA/PRA taxonomies

---

## 💡 Solution

This prototype demonstrates an **end-to-end regulatory reporting workflow**:

```
User Question → Retrieval of Regulatory Text → Structured LLM Output → Populated Template
```

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **RAG-Powered Q&A** | Retrieves relevant CRR articles and COREP instructions based on user queries |
| **Template Population** | Automatically maps extracted values to CA1/CA2 template fields |
| **Validation Engine** | Flags missing/inconsistent data using regulatory rules |
| **Audit Trail** | Documents which rule paragraphs justify each populated field |

---

## 📊 Scope

This prototype focuses on two COREP templates:

- **C 01.00 (CA1)**: Own Funds composition
- **C 02.00 (CA2)**: Capital Requirements

### Knowledge Base Coverage
- CRR Articles 26-36 (CET1 Capital)
- CRR Articles 51-52 (AT1 Capital)
- CRR Articles 62-63 (Tier 2 Capital)
- CRR Article 92 (Capital Requirements)
- COREP template instructions

---

## 🚀 Live Demo

**Frontend**: [pra-corep-web.onrender.com](https://pra-corep-web.onrender.com)  
**API**: [pra-corep-api.onrender.com](https://pra-corep-api.onrender.com)

### Try This Scenario

Switch to **Analyze** mode and enter:

> "Our bank has ordinary share capital of £500 million, share premium £200 million, retained earnings £150 million, intangible assets £30 million, subordinated debt (Tier 2) £100 million, and total RWAs of £4 billion."

**Expected Output:**
- Populated CA1 template with 15+ fields
- CET1 = £820m, CET1 ratio = 20.5%
- All validation checks pass ✓
- Audit trail linking fields to CRR articles

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   FastAPI       │────▶│   GitHub        │
│   (Vanilla JS)  │     │   Backend       │     │   Models API    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                        ┌────────▼────────┐
                        │  Knowledge Base │
                        │  (CRR Articles) │
                        └─────────────────┘
```

### End-to-End Flow

1. **User Input**: Natural language description of capital position
2. **RAG Retrieval**: Relevant CRR articles and instructions retrieved
3. **LLM Processing**: Structured JSON output aligned to template schema
4. **Template Mapping**: Values populated into CA1/CA2 fields
5. **Validation**: Rules checked (ratios, arithmetic, thresholds)
6. **Audit Trail**: Field-to-regulation citations generated

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | Vanilla HTML/CSS/JS |
| Backend | FastAPI (Python 3.11) |
| LLM | GPT-4o-mini via GitHub Models |
| Deployment | Render.com |

---

## 📁 Project Structure

```
pra-corep-assistant/
├── backend/
│   ├── main.py              # API endpoints (/chat, /analyze, /export/pdf)
│   ├── knowledge_base.py    # Regulatory text, schemas, validation rules
│   └── requirements.txt     
├── frontend/
│   ├── index.html           # Chat + Analyze modes
│   ├── styles.css           # Dark theme UI
│   └── app.js               # API integration
├── render.yaml              # Deployment config
└── README.md
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with feature list |
| `/chat` | POST | RAG-powered Q&A |
| `/chat/stream` | POST | Streaming responses (SSE) |
| `/analyze` | POST | Template population from scenario |
| `/export/pdf` | POST | Generate PDF report |

### Example: Analyze Endpoint

**Request:**
```json
{
  "scenario": "Bank has £500m share capital, £150m reserves, £30m intangibles",
  "template": "CA1"
}
```

**Response:**
```json
{
  "template_id": "C_01.00",
  "fields": [{"row_id": "010", "label": "Capital instruments", "value": 500}],
  "totals": {"cet1": 620, "tier1": 620},
  "ratios": {"cet1_ratio": 15.5},
  "validation_results": [{"rule_id": "VAL_001", "passed": true}],
  "audit_trail": [{"field": "row_010", "rule_id": "CRR_ART_26", "explanation": "..."}]
}
```

---

## 🧪 Validation Rules

| Rule | Type | Description |
|------|------|-------------|
| CET1 ratio ≥ 4.5% | Threshold | Minimum requirement (CRR Art. 92) |
| Tier 1 ratio ≥ 6% | Threshold | Minimum requirement |
| Total capital ≥ 8% | Threshold | Minimum requirement |
| CET1 = sum of items - deductions | Arithmetic | Template consistency |
| Deductions ≥ 0 | Sign | Positive values only |

---

## 🚀 Local Development

```bash
# Clone
git clone https://github.com/VatsalRaina01/pra-corep-assistant.git
cd pra-corep-assistant

# Backend
cd backend
pip install -r requirements.txt
$env:GITHUB_TOKEN = "your-token"  # PowerShell
python main.py  # → http://localhost:8000

# Frontend (new terminal)
cd frontend
python -m http.server 3000  # → http://localhost:3000
```

---

## ✅ Success Criteria Met

| Criterion | Status |
|-----------|--------|
| User question → retrieval of regulatory text | ✅ |
| Structured LLM output aligned to schema | ✅ |
| Populated template extract | ✅ |
| Validation with basic rules | ✅ |
| Audit log of rule paragraphs used | ✅ |
| Constrained scope (CA1/CA2 only) | ✅ |

---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

- PRA Rulebook and COREP templates by EBA/PRA
- Built for the LLM-assisted regulatory reporting challenge
