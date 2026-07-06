from fastapi import APIRouter, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version()")).scalar()

    return {
        "status": "healthy",
        "database": "connected",
        "postgres": version,
    }