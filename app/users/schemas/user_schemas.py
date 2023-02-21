"""User Schemas module"""
from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr
from datetime import date

from .subuser_schemas import SubuserSchema


class UserSchema(BaseModel):
    """Base schema for User"""
    id: UUID4
    email: str
    password_hashed: str
    username: str
    date_subscribed: date
    is_active: bool
    is_superuser: bool
    verification_code: Optional[int]

    class Config:
        orm_mode = True


class UserSchemaIn(BaseModel):
    """Base User schema for input"""
    email: EmailStr
    password: str
    username: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "dummy@gmail.com",
                "password": "password",
                "username": "username"
            }
        }


class UserSchemaOut(BaseModel):
    """Base User schema for output"""
    id: UUID4
    email: str
    username: str
    date_subscribed: date
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserWithSubusersSchema(BaseModel):
    """User schema with subusers"""
    id: UUID4
    email: str
    password_hashed: str
    username: str
    date_subscribed: date
    is_active: bool
    is_superuser: bool
    code: Optional[int]
    subusers: list[SubuserSchema]

    class Config:
        orm_mode = True
