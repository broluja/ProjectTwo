from pydantic import BaseModel
from pydantic import UUID4


class AdminSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    address: str
    country: str
    user_id: str

    class Config:
        orm_mode = True


class AdminSchemaIn(BaseModel):
    first_name: str
    last_name: str
    address: str
    country: str
    user_id: str

    class Config:
        orm_mode = True
