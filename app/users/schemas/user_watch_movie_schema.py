"""UserWatchMovie schemas module"""
from datetime import date
from pydantic import BaseModel, UUID4, Field


class UserWatchMovieSchema(BaseModel):
    """Base schema for UserWatchMovie model."""
    id: UUID4
    user_id: str
    movie_id: str
    rating: int = None
    date_watched: date

    class Config:
        """Configuration Class"""
        orm_mode = True


class UserWatchMovieSchemaIn(BaseModel):
    """Base UserWatchMovie schema for input."""
    movie: str
    rating: int = Field(gt=0, lt=11, description='Rating must be between 1-10')

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "movie": "Pulp Fiction",
                "rating": 8
            }
        }
