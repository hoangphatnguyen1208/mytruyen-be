from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    )
    API_V1_STR = '/api/v1'
    PROJECT_NAME: str
    POSTGRE_SERVER: str
    POSTGRE_PORT: int = 5432
    POSTGRE_DB: str
    POSTGRE_USER: str
    POSTGRE_PASSWORD: str
    POSTGRE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str 

settings = Settings()