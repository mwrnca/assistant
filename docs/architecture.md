# AI Assistant Architecture

## Overview

The platform is being shaped as an Input-first AI system that can later grow into a reusable platform.

Its responsibilities include:

- Authentication
- Input ingestion from multiple sources
- AI understanding and event generation
- Long-term memory
- Task management
- Conversation history
- User management
- API endpoints

The frontend never communicates directly with the database.

```
React
      │
      ▼
 FastAPI Backend
      │
      ▼
 PostgreSQL
```

---

## Core Architecture Direction

Everything now centers around the following flow:

```
Input
  ▼
Input Repository
  ▼
Input Processor
  ▼
AI Understanding Layer
  ▼
Event Generation
  ▼
Event Bus
  ├── Memory
  ├── Tasks
  └── Planner
```

This means speech is treated as one input source, not the center of the system.

---

# backend/app/

Contains all application logic.

The project structure is intentionally organized to support gradual expansion into a reusable AI platform.

---

## api/

Contains API endpoints.

These should remain thin and delegate to services.

---

## services/

Contains service layer logic for business workflows and orchestration.

---

## repositories/

Contains persistence access for domain models.

---

## models/

Contains database entities.

---

## schemas/

Contains request and response validation models.

---

## orchestrator/

Contains workflow and routing logic for processing input into meaningful actions.

---

## events/

Contains event bus, event handling, and event types.

---

## modules/

Contains domain-specific modules such as memory, tasks, planner, search, calendar, automation, analytics, and integrations.

---

## ai/

Contains AI-related components such as prompts, LLM abstractions, embeddings, summarization, classification, and extraction helpers.

---

## clients/

Contains integrations with external systems.

These should remain transport-oriented and avoid business logic.

---

## utils/

Contains shared helpers, datetime utilities, validators, and exceptions.

---

# frontend/src/

Contains the React application structure.

The UI should grow around dashboard and capability pages rather than around speech alone.

---

## components/

Shared UI components grouped by feature area.

---

## pages/

Top-level pages such as Dashboard, Assistant, Memory, Tasks, Conversations, Search, and Settings.

---

## services/

Frontend services for API communication and shared client logic.

---

## store/

State management and application state slices.

---

## types/

Shared TypeScript types.

---

## utils/

Shared frontend utility functions.


## llm.py

Communicates with

- OpenAI
- Ollama
- Claude
- Gemini

---

## whisper.py

Speech recognition.

---

## email.py

Email provider.

---

## storage.py

Cloud storage.

Future

- AWS S3
- Cloudflare R2
- Google Cloud Storage

---

# core/

Application configuration.

---

## config.py

Loads

```
DATABASE_URL
JWT_SECRET
OPENAI_KEY
```

Only place environment variables should be read.

---

## security.py

Security helpers.

Encryption

Random tokens

Password policies

---

## logging.py

Configures logging.

Instead of

```
print()
```

use

```
logger.info()
```

---

## constants.py

Stores constants.

Instead of

```
MAX_UPLOAD = 50000000
```

everywhere

define once.

---

# database/

Everything related to the database.

---

## session.py

Creates database connection.

---

## base.py

SQLAlchemy Base.

All models inherit from this.

---

## seed.py

Optional.

Creates test data.

---

# middleware/

Runs before requests reach the API.

---

## auth.py

Authentication middleware.

---

## cors.py

Cross-origin settings.

Allows React to communicate with FastAPI.

---

## rate_limit.py

Stops abuse.

Example

100 requests/minute.

---

## request_logger.py

Logs every request.

---

# models/

Database tables.

Every file represents one SQL table.

---

## user.py

User table.

---

## speech.py

Stores every transcript.

---

## task.py

Stores tasks.

---

## memory.py

Stores assistant memories.

---

## conversation.py

Stores chat history.

---

# prompts/

Prompt engineering.

Never hardcode huge prompts.

assistant.txt

Planner

Summarizer

Memory extraction

Speech cleanup

---

# schemas/

Pydantic models.

These validate API input/output.

Example

Incoming request

```json
{
 "email":"..."
}
```

Schema checks

Required fields

Types

Validation

Schemas are NOT database tables.

---

# services/

Business logic.

Most important folder.

Contains the intelligence of your application.

---

## assistant_service.py

Coordinates everything.

Receives transcript.

Calls LLM.

Stores results.

Creates tasks.

Creates memories.

---

## speech_service.py

Speech workflow.

---

## task_service.py

Everything task-related.

---

## memory_service.py

Everything memory-related.

---

## conversation_service.py

Conversation history.

---

## user_service.py

User operations.

---

# utils/

Small reusable helpers.

Example

```
format_datetime()

clean_filename()

validate_email()
```

Should remain small.

---

# main.py

Application entry point.

Starts FastAPI.

Registers routers.

Registers middleware.

Starts application.

---

# tests/

Contains automated tests.

Should mirror app structure.

```
tests/

api/

services/

database/
```

---

# frontend/

React application.

Only responsible for UI.

Never contains business logic.

---

# api/

Functions that call FastAPI.

Example

```
login()

getTasks()

createTask()
```

---

# assets/

Images

Icons

Audio

Fonts

---

# components/

Reusable UI.

Buttons

Cards

Speech visualizer

Task card

Memory card

---

# hooks/

Custom React hooks.

Example

```
useAuth()

useSpeech()

useTasks()
```

---

# layouts/

Application layouts.

Dashboard layout.

Login layout.

---

# pages/

Actual pages.

Dashboard

Tasks

Memory

Conversation

Settings

Login

---

# services/

Frontend business helpers.

Formatting

Caching

Client-side processing.

---

# store/

Global state.

Example

```
User

Theme

Notifications
```

---

# styles/

Global CSS.

---

# types/

TypeScript interfaces.

---

# utils/

Frontend helper functions.

---

# docs/

Project documentation.

Architecture

API

Roadmap

Database

---

# storage/

Temporary files.

Audio uploads.

Images.

Temporary exports.

Ignored by Git.

---

# logs/

Application logs.

Ignored by Git.

---

# Docker

## backend/Dockerfile

Container for FastAPI.

---

## frontend/Dockerfile

Container for React.

---

## docker-compose.yml

Starts

- React
- FastAPI
- PostgreSQL

with one command.

---

# Design Principles

1. API handles HTTP only.
2. Services contain business logic.
3. Models represent database tables.
4. Schemas validate data.
5. Clients communicate with external services.
6. Frontend never accesses the database directly.
7. Environment variables are read only from `core/config.py`.
8. Large prompts belong in `prompts/`.
9. Reusable code belongs in `utils/`.
10. Every feature should follow the flow:

```
Request
    ↓
Router
    ↓
Service
    ↓
Client / Database
    ↓
Response
```