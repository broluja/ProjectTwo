"""User Schemas module"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr

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


class UserLoginSchema(BaseModel):
    """Login User Schema"""
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


class AdminLoginSchema(BaseModel):
    """Login Admin Schema"""
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


class ChangePasswordSchema(BaseModel):
    code: int
    new_password: str
    repeat_password: str

    class Config:
        """Configuration Class"""
        schema_extra = {
            "example": {
                "code": 12345,
                "new_password": "new_password",
                "repeat_password": "repeat_password"
            }
        }
