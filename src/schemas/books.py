from typing import Optional

from pydantic import BaseModel, Field


class BaseBook(BaseModel):
    class Config:
        form_attributes = True


class CreateBook(BaseBook):
    name: str = Field(max_length=50)
    author: str = Field(max_length=50)
    year: Optional[int] = Field(max_length=4)
    ISBN: Optional[str] = Field(max_length=50)
    count: Optional[int] = Field(ge=1)


class ResponseBook(BaseBook):
    id: int
    name: str = Field(max_length=50)
    author: str = Field(max_length=50)
    year: Optional[int] = Field(max_length=4)
    ISBN: Optional[str] = Field(max_length=50)
    count: Optional[int] = Field(ge=1)