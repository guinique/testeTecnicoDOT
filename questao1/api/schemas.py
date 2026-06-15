from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


# modelos de dados para a API usando Pydantic
class BookBase(BaseModel):
    title: str = Field(..., example="Fourth Wing")
    author: str = Field(..., example="Rebecca Yarros")
    public_date: date = Field(..., example="2023-04-05")
    summary: Optional[str] = Field(None, example="Fourth Wing is a new adult fantasy romance novel...")

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True