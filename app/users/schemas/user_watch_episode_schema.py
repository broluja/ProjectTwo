"""UserWatchEpisode schemas module"""
from datetime import date

from pydantic import BaseModel, UUID4, Field


class UserWatchEpisodeSchema(BaseModel):
    """Base schema for UserWatchEpisode model."""
    id: UUID4
    user_id: str
    episode_id: str
    rating: int = None
    date_watched: date

    class Config:
        """Configuration Class"""
        orm_mode = True


class UserWatchEpisodeSchemaIn(BaseModel):
    """Base UserWatchEpisode model schema for input."""
    episode: str
    rating: int = Field(gt=0, lt=11, description='Rating must be between 1-10')

    class Config:
        """Configuration Class"""
        orm_mode = True
        schema_extra = {
            "example": {
                "movie": "Episode One",
                "rating": 8
            }
        }
