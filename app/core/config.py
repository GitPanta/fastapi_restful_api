from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    PROJECT_NAME: str = "MSA Technical Challenge"
    
    SECRET_KEY: str = "f8951131d9fc2568db80ac4629899daf689f6837053724c0e63b7cacffea8cd2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2  # 60 min * 24 h * 2 = 2 days
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    
    FIRST_ELECTION_SEATS_AMOUNT: int = 7
    
    FIRST_ROSTER_AMOUNT: int = 5


settings = Settings()