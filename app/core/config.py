from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings with environment variables"""
    deepseek_api_key: str
    serper_api_key: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()