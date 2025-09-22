from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    PROJECT_NAME: str

    API_V1_STR: str
    POSTGRE_SERVER: str
    POSTGRE_PORT: int
    POSTGRE_DB: str
    POSTGRE_USER: str
    POSTGRE_PASSWORD: str
    POSTGRE_URL: str
    POSTGRE_SYNC_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str

settings = Settings()