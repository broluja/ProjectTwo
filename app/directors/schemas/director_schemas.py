from pydantic import BaseModel, UUID4


class DirectorSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    country: str

    class Config:
        orm_mode = True


class DirectorSchemaIn(BaseModel):
    first_name: str
    last_name: str
    country: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "country": "USA"
            }
        }