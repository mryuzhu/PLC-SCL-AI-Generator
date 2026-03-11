# PLC-SCL-AI-Generator

Web-based PLC SCL auto-generation platform based on natural language requirements.

## Implemented v1 Scope

- Generate Siemens-style SCL blocks (FB/DB/UDT baseline).
- Support generation modes: `safe`, `balanced` (default), `free`.
- REST API for generation, validation, task management, and TIA import request.
- Rule-based validator with safety checks (OB restriction in safe mode).
- Project/Task/Code persistence via SQLAlchemy (SQLite default, PostgreSQL-ready).
- Minimal Next.js frontend for prompt input and generated code review.

## Project Structure

```text
backend/
  api/
  core/
  llm/
  models/
  services/
frontend/
  pages/
  components/
  editor/
  api/
docs/
```

## Quick Start

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Main APIs

- `POST /generate`
- `POST /validate`
- `POST /task/create`
- `GET /task/status/{task_id}`
- `GET /task/result/{task_id}`
- `POST /tia/import`
