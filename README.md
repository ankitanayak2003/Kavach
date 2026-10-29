# Kavach (कवच)

> **AI-Assisted Application Security Testing Platform**

Kavach is an intelligent, modern application security testing platform designed to combine automated security scanners (OWASP ZAP, Nuclei) with browser automation (Playwright) and AI-guided vulnerability triage and remediation (FreeLLMAPI).

---

## 📌 Project Status — Day 1 Foundation

> [!NOTE]
> **Current Status (Day 1 Completed)**: Core FastAPI modular structure, versioned health check route, environment configuration via `pydantic-settings`, and automated pytest suite are implemented. Database, scanner engines, queue workers, AI routing, and frontend dashboards are planned for future development milestones.

### Implemented Features (Day 1)
- **FastAPI Modular Core**: Application entry point with clear separation between routing layers and business logic.
- **Versioned Health Endpoint**: Accessible at `/api/v1/health` returning live status and service metadata.
- **Environment Settings Management**: Pydantic Settings configuration module reading environment variables and optional local `.env` files.
- **Safe Development Defaults**: `.env.example` provided; credentials and environment files safely excluded via `.gitignore`.
- **Zero-Dependency Startup**: Starts cleanly without requiring external cloud, database, or API credentials.
- **Automated Test Suite**: Pytest test suite validating health routes, metadata endpoints, and configuration loading.

### Planned Features (Upcoming Milestones)
- 🔲 **Firestore & Firebase Admin SDK**: Secure persistence for scan jobs, findings, and target profiles.
- 🔲 **Playwright Automation**: Dynamic route discovery and single-page application (SPA) crawling.
- 🔲 **OWASP ZAP & Nuclei Scanners**: Containerized active and passive vulnerability scanning.
- 🔲 **Redis & Celery**: Distributed asynchronous job execution and scan scheduling.
- 🔲 **FreeLLMAPI Routing**: AI-powered false-positive reduction, contextual risk scoring, and remediation advice.
- 🔲 **React + TypeScript Dashboard**: Interactive scanning console, real-time alerts, and report exports.
- 🔲 **Docker Containerization**: Sandboxed scanner execution and multi-container deployment.

---

## 🛠️ Technology Stack

| Component | Technology | Status | Role |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Python 3.12+ / FastAPI | **Implemented** | High-performance asynchronous REST API gateway |
| **Settings & Validation** | Pydantic & pydantic-settings | **Implemented** | Type-safe configuration and schema validation |
| **Testing Suite** | Pytest & HTTPX | **Implemented** | Automated unit and integration testing |
| **Database** | Google Cloud Firestore | *Planned* | NoSQL persistent store for scan results and targets |
| **AI LLM Routing** | FreeLLMAPI | *Planned* | Vulnerability analysis and remediation guidance |
| **Crawler Engine** | Playwright | *Planned* | Headless browser SPA crawling and authenticated flows |
| **DAST Scanners** | OWASP ZAP & Nuclei | *Planned* | Comprehensive active and passive vulnerability scanning |
| **Task Queue** | Redis & Celery | *Planned* | Distributed asynchronous task queue for scan jobs |
| **Frontend UI** | React & TypeScript | *Planned* | Modern security management dashboard |
| **Isolation** | Docker | *Planned* | Sandboxed scanner containers and reproducible deployment |

---

## 📂 Repository Structure

```text
Kavach/
├── .env.example              # Template environment configuration (safe defaults)
├── .gitignore                # Protects environments, secrets, caches, and logs
├── requirements.txt          # Pinned Python dependencies
├── README.md                 # Project documentation and quickstart guide
├── docs/
│   └── architecture.md       # High-level architecture and scan lifecycle
├── app/
│   ├── __init__.py           # App package initialization
│   ├── main.py               # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py       # Core package initialization
│   │   └── config.py         # Pydantic BaseSettings configuration module
│   └── api/
│       ├── __init__.py       # API package initialization
│       └── v1/
│           ├── __init__.py   # API v1 package initialization
│           ├── router.py     # Aggregated v1 API router
│           └── endpoints/
│               ├── __init__.py
│               └── health.py # Health check endpoint handler
└── tests/
    ├── __init__.py           # Tests package initialization
    ├── conftest.py           # Pytest test client fixtures
    ├── test_config.py        # Configuration & environment override tests
    └── test_health.py        # Health & root route automated tests
```

---

## 🚀 Getting Started (Windows Setup)

### Prerequisites
- **Python 3.12+** (Python 3.14 compatible)
- **Git**
- **PowerShell**

### 1. Clone the Repository
```powershell
git clone https://github.com/ankitanayak2003/Kavach.git
cd Kavach
```

### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1
```
*(If execution policy restricts running scripts, execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example configuration to a local `.env` file:
```powershell
Copy-Item .env.example .env
```

Default configuration in `.env.example`:
```ini
APP_NAME=Kavach
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
API_V1_PREFIX=/api/v1
LOG_LEVEL=INFO
```
> [!IMPORTANT]
> The application starts with default values even without a `.env` file. Never commit real credentials, API tokens, or service-account JSON files to Git.

### 5. Run the FastAPI Development Server
```powershell
# Option A: Run via uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Option B: Run directly via Python module
python app/main.py
```

### 6. Access Documentation & Endpoints
- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Root Metadata**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Health Endpoint**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

Verify the health endpoint using `curl`:
```powershell
curl http://127.0.0.1:8000/api/v1/health
```
Expected output:
```json
{
  "status": "healthy",
  "service": "kavach-api",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## 🧪 Running Tests

Execute the automated test suite with pytest:
```powershell
pytest
```
To run tests with detailed verbose output:
```powershell
pytest -v
```

---

## 🗓️ 30-Day Development Roadmap

| Phase | Days | Focus Areas | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Days 1–5 | **Foundation & Architecture** | FastAPI core, environment config, Docker setup, CI pipeline |
| **Phase 2** | Days 6–10 | **Data Layer & Authentication** | Firestore models, Firebase Admin SDK integration, Auth & RBAC |
| **Phase 3** | Days 11–16 | **Task Queue & Scanner Engines** | Celery + Redis broker, OWASP ZAP & Nuclei container integration |
| **Phase 4** | Days 17–21 | **Browser Automation & Discovery** | Playwright SPA crawler, authenticated crawl workflows, route mapping |
| **Phase 5** | Days 22–25 | **AI Triage & Analysis** | FreeLLMAPI integration, false-positive filtering, remediation generator |
| **Phase 6** | Days 26–30 | **Frontend Console & Release** | React + TypeScript UI, real-time finding feeds, PDF/JSON export, hardening |

---

## 🔒 Security Principles and Authorization

Kavach is designed strictly for **defensive security testing and authorized vulnerability assessments**.

1. **Authorization Mandate**: Security scans must only be run against domains, applications, and networks where explicit written authorization has been granted.
2. **Non-Destructive Testing**: Default scanning templates avoid disruptive payloads that could cause denial of service or database corruption.
3. **Secret Zero Protection**: Service account keys, Firebase credentials, and LLM API tokens must never be hardcoded or checked into Git. Use secret managers or local uncommitted `.env` files.
4. **Sandboxed Isolation**: Scanner processes must run in dedicated Docker containers with network boundaries to prevent unintended lateral network movement.
