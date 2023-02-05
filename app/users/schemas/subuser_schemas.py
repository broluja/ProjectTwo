from pydantic import BaseModel
from pydantic import UUID4
from datetime import datetime


class SubuserSchema(BaseModel):
    id: UUID4
    name: str
    date_subscribed: datetime

    class Config:
        orm_mode = True


class SubuserSchemaIn(BaseModel):
    name: str
    date_subscribed: datetime

    class Config:
        orm_mode = True
