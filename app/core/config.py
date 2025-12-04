from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str
    DB_SERVER: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATABASE_URL(self) -> str:
        password_encoded = quote_plus(self.DB_PASSWORD)
        driver_encoded = quote_plus(self.DB_DRIVER)
        
        return (
            f"mssql+aioodbc://{self.DB_USER}:{password_encoded}"
            f"@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"
            f"?driver={driver_encoded}&TrustServerCertificate=yes"
        )

settings = Settings()
