from sanic_jwt import Configuration
from pathlib import Path


class ProductionConfig:
    # mode
    DEBUG: bool = False

    # SECRET related
    # Using: `$ openssl rand -base64 32` to get.
    SECRET_KEY: str = "Uh3rtb4Eca1nF1rnjMOfpMX+ZFuGepmYzEdup/5YebU="

    # DATABASE
    DB_DIALECT: str = ""
    DB_DRIVER: str = ""
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_ADDR: str | None = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}" if DB_DIALECT == "sqlite" else None
    DB_LOCATION: str = ""
    SQLALCHEMY_DATABASE_URL: str = f"{DB_DIALECT}+{DB_DRIVER}://{DB_ADDR}/{DB_LOCATION}"
    SQLALCHEMY_DATABASE_ENCODING: str = "utf8"
    SQLALCHEMY_DATABASE_ECHO: bool = True

class SanicJWTProConfig(Configuration):
    algorithm: str = "ES256"
    auth_mode: bool = False
    user_id: str = "id"
    def get_url():
        ...
