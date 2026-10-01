from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    session_secret_key: str  
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, 
        env_file_encoding="utf-8", 
        extra="ignore",
        # default for deployment, dev environment needs to confogure origin and runtime 
    )
    cors_origins: list[str] = ["https://algorithm-complexity.de"]
    docker_runtime: str | None = "runsc"
        
settings = Settings()