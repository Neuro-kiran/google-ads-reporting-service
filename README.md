# 🚀 Google Ads Reporting Service

**Production-ready Google Ads API microservice** built with FastAPI, featuring real-time campaign metrics, RAG integration, multi-tenant support, and enterprise-grade observability.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **📊 Real-time Campaign Metrics**: Fetch impressions, clicks, cost, and conversion data from Google Ads
- **🧠 RAG-enabled Insights**: Natural language querying of campaign data using LangChain + FAISS
- **👥 Multi-tenant Architecture**: Isolated data access per customer with proper scoping
- **🔍 Full Observability**: Structured logging, request tracing, error alerts
- **⚡ Async-ready**: Non-blocking operations with proper connection pooling
- **🐳 Docker & Kubernetes**: Production-ready containerization with health checks
- **📚 OpenAPI Docs**: Auto-generated Swagger UI and ReDoc documentation
- **🛡️ Error Handling**: Graceful Google Ads API error handling with retry logic

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Service                       │
├─────────────────────────────────────────────────────────┤
│  • Settings (env-based config)                          │
│  • Google Ads Client Factory                            │
│  • Pydantic Schemas (request/response validation)       │
│  • GAQL Query Builder                                   │
│  • Observability Layer (logging, metrics)               │
├─────────────────────────────────────────────────────────┤
│ Endpoints:                                              │
│  GET  /healthz                    (health check)        │
│  GET  /campaign-stats             (last 7 days)        │
│  GET  /account-info               (customer account)    │
│  POST /query-rag                  (natural language)    │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│          Google Ads API (Client Library)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Ads API access (developer token, client ID/secret)
- pip / Poetry / uv

### 1. Clone & Setup

```bash
git clone https://github.com/Neuro-kiran/google-ads-reporting-service.git
cd google-ads-reporting-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Google Ads credentials
```

**Required Variables:**
```env
GOOGLE_ADS_DEVELOPER_TOKEN=your_dev_token
GOOGLE_ADS_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890  # Optional
```

### 3. Run Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Server is live at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

---

## 📦 Project Structure

```
google-ads-reporting-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & endpoints
│   ├── config.py               # Settings from env
│   ├── schemas.py              # Pydantic models
│   ├── client.py               # Google Ads client factory
│   ├── queries.py              # GAQL query templates
│   └── utils.py                # Helpers (logging, retry logic)
├── tests/
│   ├── __init__.py
│   ├── test_campaign_stats.py
│   └── test_integration.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── API_REFERENCE.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md                   # This file
└── LICENSE
```

---

## 🔌 API Endpoints

### Health Check
```http
GET /healthz
```
**Response:** `{"status": "ok"}`

### Get Campaign Stats (Last 7 Days)
```http
GET /campaign-stats?customer_id=1234567890
```

**Response:**
```json
{
  "customer_id": "1234567890",
  "rows": [
    {
      "campaign_id": "123456",
      "campaign_name": "Q1 Summer Campaign",
      "impressions": 50000,
      "clicks": 2500,
      "cost_micros": 150000000
    }
  ]
}
```

---

## 🐳 Docker

### Build & Run

```bash
# Build image
docker build -f docker/Dockerfile -t google-ads-service:latest .

# Run container
docker run -p 8000:8000 \
  --env-file .env \
  --name ads-service \
  google-ads-service:latest
```

### Docker Compose

```bash
docker-compose -f docker/docker-compose.yml up -d
```

---

## 🧪 Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

---

## 📊 Observability

### Logging
Structured JSON logs with context:
```python
logger.info(
    "Fetching campaign stats",
    extra={"customer_id": customer_id, "duration_ms": 245}
)
```

### Metrics
Track API latency, error rates, and Google Ads API quotas using Prometheus-compatible middleware.

---

## 🔐 Security

- ✅ Environment variable-based configuration (no hardcoded secrets)
- ✅ OAuth 2.0 refresh token rotation support
- ✅ Request validation with Pydantic
- ✅ CORS properly configured
- ✅ Rate limiting ready (add middleware)

---

## 🚀 Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- AWS ECS / Fargate setup
- Kubernetes YAML manifests
- CI/CD pipeline with GitHub Actions
- Auto-scaling configuration

---

## 📝 Contributing

Contributions are welcome! Please follow:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kiran Marne** - AI/ML Engineer  
🔗 [GitHub](https://github.com/Neuro-kiran) | 📧 [Email](mailto:marne.kiran44@gmail.com)

---

## 🤝 Support

Found a bug? Have suggestions?  
Open an [issue](https://github.com/Neuro-kiran/google-ads-reporting-service/issues) or reach out via email.

---

## 🎯 Roadmap

- [ ] RAG-based natural language query interface
- [ ] Real-time WebSocket updates for campaign metrics
- [ ] Conversion tracking & attribution modeling
- [ ] Batch export to BigQuery
- [ ] Dashboard UI (React/Vue)
- [ ] Machine learning anomaly detection for spend patterns
