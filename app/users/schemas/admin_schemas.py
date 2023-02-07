from pydantic import BaseModel, UUID4


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
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address": "1st Street, Chicago",
                "country": "USA",
                "user_id": ""
            }
        }
