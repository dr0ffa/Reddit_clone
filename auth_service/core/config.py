from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
import logging
from typing import Literal
import redis




class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class JWTConfig(BaseModel):
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_expire_days: int = 7

class KafkaConfig(BaseModel):
    bootstrap_servers: str  # Например: "localhost:9092,localhost:9093"
    group_id: str = "auth-service-group"

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    db: DatabaseConfig
    jwt: JWTConfig
    kafka: KafkaConfig 
    redis: RedisConfig = RedisConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()

settings = Settings()
redis_client = redis.Redis(
    host=settings.redis.host, 
    port=settings.redis.port, 
    db=settings.redis.db
)

settings = Settings()