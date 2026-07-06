from fastapi import FastAPI

from app.api.v1.api import api_router
from app.database.seed import create_tables

app = FastAPI(
    title="AI Assistant API",
    version="1.0.0",
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