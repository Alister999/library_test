from pydantic import BaseModel, Field, EmailStr, ConfigDict


class BaseReader(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True


class ReaderCreate(BaseReader):
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)


class ReaderResponse(BaseReader):
    id: int
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)