from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.database.seed import create_tables

app = FastAPI(
    title="AI Assistant API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {
        "message": "AI Assistant API"
    }