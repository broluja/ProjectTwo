from pydantic import BaseModel, UUID4


class GenreSchema(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True


class GenreSchemaIn(BaseModel):
    name: str

    class Config:
        orm_mode = True
