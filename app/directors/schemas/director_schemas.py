"""Director Schemas module"""
from pydantic import BaseModel, UUID4


class DirectorSchema(BaseModel):
    """Base Director schema"""
    id: UUID4
    first_name: str
    last_name: str
    country: str

    class Config:
        """Configuration Class"""
        orm_mode = True


class DirectorSchemaIn(BaseModel):
    """Director schema for input"""
    first_name: str
    last_name: str
    country: str

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "country": "USA"
            }
        }
