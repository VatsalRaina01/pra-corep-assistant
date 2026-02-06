import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # GitHub Models Configuration
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_endpoint: str = "https://models.github.ai/inference"
    model_name: str = "gpt-4o-mini"
    
    # Application Settings
    debug: bool = True
    log_level: str = "INFO"
    
    # Vector Database
    chroma_persist_directory: str = "./data/chroma_db"
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    
    # Model Parameters
    temperature: float = 0.1
    max_tokens: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
