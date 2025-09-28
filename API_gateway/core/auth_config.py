from authx import AuthX, AuthXConfig
from datetime import timedelta

def get_auth_config() -> AuthXConfig:
    config = AuthXConfig()
    config.JWT_SECRET_KEY = "super-secret-key"
    config.JWT_ACCESS_COOKIE_NAME = "access_token"
    config.JWT_REFRESH_COOKIE_NAME = "refresh_token"
    config.JWT_TOKEN_LOCATION = ["cookies"]
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    return config

security: AuthX = AuthX(config=get_auth_config())