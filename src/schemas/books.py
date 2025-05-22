from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BaseBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True


class BookCreate(BaseBook):
    name: str = Field(max_length=50)
    author: str = Field(max_length=50)
    year: int | None = Field(ge=0, le=2050)
    ISBN: str | None = Field(max_length=50)
    count: int | None = Field(ge=1)


class BookResponse(BaseBook):
    id: int
    name: str = Field(max_length=50)
    author: str = Field(max_length=50)
    year: Optional[int] = Field(ge=0, le=2050)
    ISBN: Optional[str] = Field(max_length=50)
    count: Optional[int] = Field(ge=1)