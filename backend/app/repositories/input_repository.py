from sqlalchemy.orm import Session

from app.models.input import Input


class InputRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, source: str, content: str, status: str = "PENDING") -> Input:
        input_record = Input(source=source, content=content, status=status)
        self.db.add(input_record)
        self.db.commit()
        self.db.refresh(input_record)
        return input_record

    def get_by_id(self, input_id: int) -> Input | None:
        return self.db.query(Input).filter(Input.id == input_id).first()

    def list_pending(self):
        return self.db.query(Input).filter(Input.status == "PENDING").order_by(Input.id).all()

    def update_status(self, input_record: Input, status: str) -> Input:
        input_record.status = status
        self.db.commit()
        self.db.refresh(input_record)
        return input_record
