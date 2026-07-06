# AI Assistant Platform - Developer Guide

## Overview
This project is a FastAPI backend and React/Vite frontend for an Input-first AI assistant platform. The current implementation focuses on the first real pipeline step: accepting raw input, storing it, and processing it through a basic repository-backed flow.

## Current Backend Architecture
- FastAPI app entry: app/main.py
- API routes: app/api/v1/api.py and app/api/v1/routers/
- Database models: app/models/
- Database bootstrapping: app/database/
- Repository layer: app/repositories/
- Services: app/services/

## Current Feature Status
- Health endpoint available
- Input model exists and creates an inputs table on startup
- Input repository layer exists
- Input processor exists for basic pending-input processing
- API endpoint for input submission is wired into the backend

## Backend Run Commands
From the backend directory:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api/v1/input

## Backend Tests
Run:

```bash
cd backend
pytest -q tests/api/test_input_api.py tests/services/test_input_processor.py
```

## Frontend Run Commands
From the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

The Vite frontend will be available at:
- http://127.0.0.1:5173/

## Suggested Next Steps
1. Connect the frontend form to POST /api/v1/input
2. Display submitted inputs in the dashboard
3. Add a real processor that emits structured events
4. Expand into memory, tasks, notes, and calendar modules

## Notes
- The project is intentionally structured around an Input-first architecture.
- Speech is treated as one type of input, not the center of the system.
- The repository layer is already introduced so future services can remain clean and testable.
