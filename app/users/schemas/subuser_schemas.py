from pydantic import BaseModel, UUID4
from datetime import date


class SubuserSchema(BaseModel):
    id: UUID4
    name: str
    date_subscribed: date

    class Config:
        orm_mode = True


class SubuserSchemaIn(BaseModel):
    name: str
    date_subscribed: date

    class Config:
        orm_mode = True
