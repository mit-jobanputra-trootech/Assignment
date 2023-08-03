from pydantic import BaseModel, Field, EmailStr
from fastapi import Query


class FilterRequestData(BaseModel):
    page_number: int = Query(default=1, description="Page Number", gt=0)
    page_size: int = Query(default=10, description="Page Size", gt=0)


class UserLogin(BaseModel):
    username: str
    password: str


class UserBaseModel(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=100)


class UserRegistrationRequestData(UserBaseModel):
    password: str