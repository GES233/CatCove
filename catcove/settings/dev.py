from pathlib import Path

PRJ_PATH = Path(__file__).cwd()


class DevConfig:
    # mode and setting
    # DEBUG: bool = True
    INSTANCE: bool = False

    # secret related

    SECRET_KEY: str = "1RXHzLNwVjgYgrLa0RNgyki39N2cYnCD/nCqHyOiFRs="
    ECC_PRIVATE_KEY: Path = Path(PRJ_PATH / "catcove/settings/eckey.pem")
    ECC_PUBLIC_KEY: Path = Path(PRJ_PATH / "catcove/settings/ecpubkey.pem")

    # database
    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///tinycat.db"
    SQLALCHEMY_DATABASE_ENCODING: str = "utf8"
    SQLALCHEMY_DATABASE_ECHO: bool = True

    # redis
    REDIS: bool = False
    REDIS_URI: str = ""
    REDIS_ENCODING: str = "utf8"

    # connect
    KEEP_ALIVE_TIMEOUT: int = 10

    # file related
    RAW_CONTENT_PATH: Path = Path(PRJ_PATH / "raw")
    AVATAR_PATH: Path = Path(RAW_CONTENT_PATH / "avatar")
