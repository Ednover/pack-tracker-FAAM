from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mail_username: str
    mail_password: str
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()