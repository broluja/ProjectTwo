from pydantic import BaseModel
from pydantic import UUID4, EmailStr
from datetime import datetime

from .subuser_schemas import SubuserSchema


class UserSchema(BaseModel):
    id: UUID4
    email: str
    password_hashed: str
    username: str
    date_subscribed: datetime
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserSchemaIn(BaseModel):
    email: EmailStr
    password: str
    username: str

    class Config:
        orm_mode = True


class UserSchemaOut(BaseModel):
    id: UUID4
    email: str
    username: str
    date_subscribed: datetime
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserWithSubusersSchema(BaseModel):
    id: UUID4
    email: str
    password_hashed: str
    username: str
    date_subscribed: datetime
    is_active: bool
    is_superuser: bool
    subusers: list[SubuserSchema]

    class Config:
        orm_mode = True
