from pathlib import Path
from .dev import PRJ_PATH

class ProConfig:
    # mode
    # DEBUG: bool = False
    INSTANCE: bool = True
    ACCESS_LOG: bool = False

    # secret related
    SECRET_KEY: str = "Q5Vl39OD8CQ93/pgY3k1wJrPpbnaP5EIYvxzruRAnxo="
    ECC_PRIVATE_KEY = None  # In instance.
    ECC_PUBLIC_KEY = None

    # database
    # sqlalchemy
    SQLALCHEMY_DATABASE_URI: str = ""
    SQLALCHEMY_DATABASE_ENCODING: str = "utf8"
    SQLALCHEMY_DATABASE_ECHO: bool = False

    # redis
    REDIS: bool = False
    REDIS_URI: str = ""
    REDIS_ENCODING: str = "utf8"

    # connect
    KEEP_ALIVE_TIMEOUT: int = 15

    # file related
    RAW_CONTENT_PATH: Path = Path(PRJ_PATH / "raw")
    AVATAR_PATH: Path = Path(RAW_CONTENT_PATH / "avatar")
