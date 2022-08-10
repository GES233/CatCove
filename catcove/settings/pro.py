class ProConfig:
    # mode
    DEBUG: bool = False
    INSTANCE: bool = True
    
    # secret related
    SECRET_KEY: str = "Q5Vl39OD8CQ93/pgY3k1wJrPpbnaP5EIYvxzruRAnxo="
    
    # database
    # sqlalchemy
    SQLALCHEMY_DATABASE_URL: str = ""
    SQLALCHEMY_DATABASE_ENCODING: str = "utf8"
    SQLALCHEMY_DATABASE_ECHO: bool = False
    
    # connect
    KEEP_ALIVE_TIMEOUT: int = 6
