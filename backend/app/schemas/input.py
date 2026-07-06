from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class InputCreate(BaseModel):
    source: Literal["TEXT", "VOICE", "PDF", "EMAIL", "API"] = Field(...)
    content: str = Field(..., min_length=1)


class InputOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    content: str
    status: str
