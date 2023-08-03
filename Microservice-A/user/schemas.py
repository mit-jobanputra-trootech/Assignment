import uuid
from typing import NewType, List
from core.dependencies import get_db
from pydantic import BaseModel, Field, validator, EmailStr
from user.models import User as UserDBModel
from fastapi import Query


ID = NewType("ID", uuid.UUID)

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserBaseModel(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=100)


class UserRegistrationRequestData(UserBaseModel):
    password: str = Field(..., regex=password_regex)

    @validator("email", always=True)
    def validate_email(cls, value):
        db = next(get_db())
        if db.query(UserDBModel).filter(UserDBModel.email == value.lower()).first():
            raise ValueError("User already exists with this email")
        return value

    @validator("username", always=True)
    def validate_username(cls, value):
        db = next(get_db())
        if db.query(UserDBModel).filter(UserDBModel.username == value).first():
            raise ValueError("User already exists with this username")
        return value

    @validator('password', always=True)
    def validate_password(cls, value):
        min_length = 8
        errors = ''
        if len(value) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if errors:
            raise ValueError(errors)
        return value


class UserRegistrationResponseData(UserBaseModel):
    id: ID

    class Config:
        orm_mode = True


class UserRegistrationCRUDData(UserBaseModel):
    id: ID
    password: str
    salt_password: str

    class Config:
        orm_mode = True


class FilterRequestData(BaseModel):
    page_number: int = Query(default=1, description="Page Number", gt=0)
    page_size: int = Query(default=10, description="Page Size", gt=0)

