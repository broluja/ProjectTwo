"""User Schemas module"""
from datetime import date
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, UUID4, EmailStr, Field

from .subuser_schemas import SubuserSchema


class UserSchema(BaseModel):
    """Base schema for User"""
    id: UUID4 = Field(default_factory=uuid4)
    email: str
    password_hashed: str
    username: str
    date_subscribed: date
    is_active: bool
    is_superuser: bool
    verification_code: Optional[int]

    class Config:
        """Configuration Class"""
        orm_mode = True


class UserSchemaIn(BaseModel):
    """Base User schema for input"""
    email: EmailStr
    password: str
    username: str

    class Config:
        """Configuration Class"""
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
        """Configuration Class"""
        orm_mode = True


class UserWithSubusersSchema(BaseModel):
    """User schema with subusers"""
    id: UUID4
    email: str
    username: str
    date_subscribed: date
    is_active: bool
    is_superuser: bool
    code: Optional[int]
    subusers: list[SubuserSchema]

    class Config:
        """Configuration Class"""
        orm_mode = True


class LoginUserSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        """Configuration Class"""
        schema_extra = {
            "example": {
                "username": "username",
                "email": "dummy@gmail.com",
                "password": "password"
            }
        }


class LoginAdminSchema(BaseModel):
    email: str
    password: str

    class Config:
        """Configuration Class"""
        schema_extra = {
            "example": {
                "email": "dummy@gmail.com",
                "password": "password"
            }
        }


class PasswordResetSchema(BaseModel):
    code: int
    password: str
    repeat_password: str

    class Config:
        """Configuration Class"""
        schema_extra = {
            "example": {
                "code": 12345,
                "password": "password",
                "repeat_password": "password"
            }
        }
