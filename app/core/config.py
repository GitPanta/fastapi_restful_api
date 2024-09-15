import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    PROJECT_NAME: str = "MSA Technical Challenge"
    
    SECRET_KEY: str #= secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2  # 60 min * 24 h * 2 = 2 days
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL: str = "postgresql://user:password@postgresserver/db"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    
    FIRST_ELECTION_SEATS_AMOUNT: int
    
    FIRST_ROSTER_AMOUNT: int


settings = Settings()