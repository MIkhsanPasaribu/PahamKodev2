"""
Konfigurasi aplikasi PahamKode
Mengelola environment variables dan settings aplikasi
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Settings untuk aplikasi PahamKode"""
    
    # Database Configuration
    DATABASE_URL: str
    DATABASE_NAME: str = "pahamkode-db"
    
    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # AI Provider Configuration
    USE_GITHUB_MODELS: bool = True
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_MODEL_NAME: str = "gpt-4o-mini"
    
    # Alternative: Azure OpenAI
    USE_AZURE_OPENAI: bool = False
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    
    # Alternative: Llama (Azure ML)
    USE_LLAMA: bool = False
    LLAMA_ENDPOINT_URL: Optional[str] = None
    LLAMA_API_KEY: Optional[str] = None
    
    # Application Settings
    ENVIRONMENT: str = "development"  # development, production
    LOG_LEVEL: str = "INFO"
    
    # Streamlit Configuration
    STREAMLIT_PORT: int = 8501
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
