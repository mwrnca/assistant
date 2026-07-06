from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.input_repository import InputRepository
from app.schemas.input import InputCreate, InputOut
from app.services.input_service import InputService

router = APIRouter(
    prefix="/input",
    tags=["Input"],
)


def get_input_service(db: Session = Depends(get_db)) -> InputService:
    repository = InputRepository(db)
    return InputService(repository)


@router.post("", response_model=InputOut, status_code=status.HTTP_201_CREATED)
def create_input(payload: InputCreate, service: InputService = Depends(get_input_service)):
    return service.create_input(payload)


@router.post("/upload", response_model=InputOut, status_code=status.HTTP_201_CREATED)
def upload_input(
    source: str = Form(...),
    content: str = Form(default=""),
    file: UploadFile | None = File(None),
    service: InputService = Depends(get_input_service),
):
    payload = InputCreate(
        source=source,
        content=content or (file.filename if file else "Uploaded content"),
        file_name=file.filename if file else None,
        mime_type=file.content_type if file else None,
    )
    return service.create_input(payload)


@router.get("/health", status_code=status.HTTP_200_OK)
def input_health():
    return {"status": "ok"}


@router.get("/{input_id}", response_model=InputOut)
def get_input(input_id: int, service: InputService = Depends(get_input_service)):
    result = service.get_input(input_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Input not found")
    return result
