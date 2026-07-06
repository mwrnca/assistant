from app.repositories.input_repository import InputRepository
from app.schemas.input import InputCreate, InputOut


class InputService:
    def __init__(self, repository: InputRepository):
        self.repository = repository

    def create_input(self, payload: InputCreate) -> InputOut:
        content = payload.content
        if payload.file_name:
            content = f"[{payload.file_name}] {content}"
        input_record = self.repository.create(
            source=payload.source,
            content=content,
        )
        return InputOut.model_validate(input_record)

    def get_input(self, input_id: int):
        input_record = self.repository.get_by_id(input_id)
        if not input_record:
            return None
        return InputOut.model_validate(input_record)
