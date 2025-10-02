import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "staging", "production"] = os.environ['ENVIRONMENT']
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Boilerplate"


settings = Settings()
