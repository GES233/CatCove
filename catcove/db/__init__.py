from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker  #, scoped_session

import os, sys

app_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir))
sys.path.append(app_path)

from catcove.app import create_config_app

app = create_config_app()

engine_bind = create_async_engine(
    url=app.config.SQLALCHEMY_DATABASE_URL,
    encoding=app.config.SQLALCHEMY_DATABASE_ENCODING,
    echo=app.config.SQLALCHEMY_DATABASE_ECHO,
    future=True,
    )

async_sessoin = sessionmaker(
    bind=engine_bind,
    class_=AsyncSession,
    expire_on_commit=False
)
