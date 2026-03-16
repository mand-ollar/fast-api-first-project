from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    auth_secret_key: str = Field(alias="AUTH_SECRET_KEY", default="TEST_KEY")
    auth_token_life_day: int = Field(alias="AUTH_TOKEN_LIFE_DAY", default=1825)
    admin_email: str = Field(alias="ADMIN_EMAIL", default="oms991112@gmail.com")
    admin_email_password: str = Field(alias="ADMIN_EMAIL_PASSWORD", default="uvrd qeei milb msen")


config: Config = Config()
