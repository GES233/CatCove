from sanic_jwt import Configuration


class DevelopmentConfig:
    # mode
    DEBUG: bool = True

    # Errors.
    FALLBACK_ERROR_FORMAT: str = "auto"


    # SECRET related
    SECRET_KEY: str = "SRSGjUV5SNzML4DnU9ibDMYUGyQdo33SZqXi/92VLC8="

    # DATABASE
    DB_DIALECT: str = "sqlite"
    DB_DRIVER: str = "aiosqlite"
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_ADDR: str | None = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    DB_LOCATION: str = "catcove.db"
    if DB_DIALECT != "sqlite":
        SQLALCHEMY_DATABASE_URL: str = f"{DB_DIALECT}+{DB_DRIVER}://{DB_ADDR}/{DB_LOCATION}"
    else:
        SQLALCHEMY_DATABASE_URL: str = f"{DB_DIALECT}+{DB_DRIVER}:///{DB_LOCATION}"
    SQLALCHEMY_DATABASE_ENCODING: str = "utf8"
    SQLALCHEMY_DATABASE_ECHO: bool = True

    # Connect
    KEEP_ALIVE_TIMEOUT: int = 10

    # Sanic_JWT

    SANIC_JWT_DEBUG: bool = True
    SANIC_JWT_SECRET: str = "SRSGjUV5SNzML4DnU9ibDMYUGyQdo33SZqXi/92VLC8="
    SANIC_JWT_ALGORITHM: str = "ES256"
    SANIC_JWT_AUTH_MODE: bool = False
    SANIC_JWT_URL_PREFIX: str = "/api/v0.1/auth"
    SANIC_JWT_USER_ID: str = "id"
