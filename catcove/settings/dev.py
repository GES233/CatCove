from pathlib import Path

PRJ_PATH = Path(__file__).cwd()


class DevConfig:
    # mode and setting
    DEBUG: bool = True
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

    # connect
    KEEP_ALIVE_TIMEOUT: int = 10
