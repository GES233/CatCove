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


class SanicJWTDevConfig(Configuration):
    debug: bool = True
    secret: str = "SRSGjUV5SNzML4DnU9ibDMYUGyQdo33SZqXi/92VLC8="
    # algorithm: str = "ES256"
    auth_mode: bool = False
    url_prefix: str = "/api/v0.1/auth"
    user_id: str = "id"
    SANIC_JWT_PUBLIC_KEY = ""
    SANIC_JWT_PRIVATE_KEY = ""
