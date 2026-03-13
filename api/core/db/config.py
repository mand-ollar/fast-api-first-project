from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    host: str = Field(alias="DB_HOST", default="127.0.0.1")
    port: int = Field(alias="DB_PORT", default=3306)
    name: str = Field(alias="DB_NAME", default="fastapi-ca")
    username: str = Field(alias="DB_USERNAME", default="root")
    password: str = Field(alias="DB_PASSWORD", default="test")
    pool_size: int = Field(alias="DB_POOL_SIZE", default=2000)
    max_overflow: int = Field(alias="DB_MAX_OVERFLOW", default=1000)

    model_config = SettingsConfigDict(env_file=".env.db", env_file_encoding="utf-8")

    @property
    def url(self) -> str:
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


db_config: DBConfig = DBConfig()
