from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Input(Base):
    __tablename__ = "inputs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
