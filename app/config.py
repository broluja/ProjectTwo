"""Configuration module"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class for storing settings data."""
    DB_HOST: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_NAME_TEST: str
    USER_SECRET: str
    ALGORYTHM: str
    TOKEN_DURATION_SECONDS: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM: str
    PER_PAGE: int
    MAX_NUMBER_SUBUSERS: int

    class Config:
        """Configuration Class"""
        env_file = './.env'


settings = Settings()
