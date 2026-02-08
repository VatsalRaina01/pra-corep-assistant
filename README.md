# PRA COREP Reporting Assistant

AI-powered assistant for UK banking regulatory reporting. Analyzes bank capital scenarios and populates COREP templates (CA1 Own Funds, CA2 Capital Requirements) with validation and audit trails.

![Status](https://img.shields.io/badge/status-ready%20to%20deploy-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)

## ✨ Features

| Feature | Description |
|---------|-------------|
| **RAG-Powered Chat** | Answers questions using embedded regulatory knowledge (CRR Articles, COREP instructions) |
| **Template Analysis** | Populates CA1/CA2 templates from natural language scenarios |
| **Validation Engine** | Checks capital ratios, arithmetic, and regulatory thresholds |
| **Audit Trail** | Links each field to relevant CRR articles |
| **PDF Export** | Downloads completed templates as PDF |
| **Streaming Responses** | Real-time chat with Server-Sent Events |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- GitHub Models API Token

### Local Development

```bash
# 1. Navigate to project
cd pra-corep-assistant

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Set API token (PowerShell)
$env:GITHUB_TOKEN = "your-token"

# 4. Start backend
python main.py
# → Backend at http://localhost:8000

# 5. Open frontend (new terminal)
cd ../frontend
python -m http.server 3000
# → Frontend at http://localhost:3000
```

## 🌐 Deploy to Render.com

1. Push to GitHub
2. Render Dashboard → New → Blueprint
3. Connect repository (auto-detects `render.yaml`)
4. Set `GITHUB_TOKEN` in environment variables
5. Update `API_BASE_URL` in `frontend/app.js` with backend URL

## 📁 Project Structure

```
pra-corep-assistant/
├── backend/
│   ├── main.py              # FastAPI with /chat, /analyze, /export/pdf
│   ├── knowledge_base.py    # Regulatory text, schemas, validation rules
│   └── requirements.txt     
├── frontend/
│   ├── index.html           # UI with chat/analyze modes
│   ├── styles.css           # Dark theme, template tables
│   └── app.js               # Mode switching, API calls
├── render.yaml              # Render deployment config
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Non-streaming chat with RAG |
| `/chat/stream` | POST | Streaming chat (SSE) |
| `/analyze` | POST | Analyze scenario → populate template |
| `/export/pdf` | POST | Export analysis as PDF |

### Analyze Request
```json
{
  "scenario": "Bank has £500m share capital, £150m retained earnings, £30m intangibles, RWA £4bn",
  "template": "CA1"
}
```

### Analyze Response
```json
{
  "template_id": "C_01.00",
  "fields": [{"row_id": "010", "value": 500, ...}],
  "totals": {"cet1": 620, "tier1": 620, ...},
  "ratios": {"cet1_ratio": 15.5, ...},
  "validation_results": [...],
  "audit_trail": [...]
}
```

## 📊 Demo Scenario

Try this in Analyze mode:

> "Our bank has ordinary share capital of £500 million, share premium £200 million, retained earnings £150 million, intangible assets £30 million, subordinated debt (Tier 2) £100 million, and total RWAs of £4 billion."

Expected output:
- CET1 = £820m (500+200+150-30)
- CET1 ratio = 20.5%
- All validation checks pass

## 📝 License

MIT License
