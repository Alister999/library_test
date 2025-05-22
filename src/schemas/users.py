from pydantic import BaseModel, Field, EmailStr, ConfigDict


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True


class UserLogin(BaseUser):
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)


class UserCreate(UserLogin):
    name: str = Field(max_length=50)


class UserResponse(BaseUser):
    id: int
    name: str
    email: str
    password_hash: str


class RefreshToken(BaseUser):
    refresh_token: str