from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://scanner:scanner123@db:5432/token_scanner"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://frontend:3000"]
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


