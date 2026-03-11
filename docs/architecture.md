# PLC SCL AI Generator Architecture

## Flow

1. Frontend sends a natural-language request to `POST /generate`.
2. Prompt Engine builds a mode-aware prompt.
3. LLM Adapter dispatches request to Coze/OpenAI/Local provider.
4. SCL Generator returns FC/FB/DB/UDT-oriented SCL text.
5. Code Validator performs syntax/rule checks and produces pass/warning/error.
6. Task Manager persists task + code results.
7. TIA Integration either exports `.scl` or triggers Openness import workflow.

## Backend Modules

- `backend/api`: FastAPI routes.
- `backend/core/prompt_engine`: prompt construction by generation mode.
- `backend/core/scl_generator`: orchestration over prompt + LLM adapter.
- `backend/core/validator`: SCL and safety policy checks.
- `backend/core/tia_integration`: export/import interface.
- `backend/llm/*`: provider implementations.
- `backend/models`: SQLAlchemy entities and API schemas.
- `backend/services`: task manager and adapter composition.

## Data Model

- `projects`: project metadata.
- `tasks`: generation request and lifecycle status.
- `codes`: generated SCL plus validation output.

## Deployment Notes

- Use PostgreSQL by setting `DATABASE_URL`.
- Run API: `uvicorn backend.main:app --reload`.
- Run frontend in `frontend/` with Next.js.
- Integrate Windows Openness worker for production TIA imports.
