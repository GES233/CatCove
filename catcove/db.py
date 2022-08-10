from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Load application's path to package
import os, sys

app_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(app_path)
# Load setting from app

from catcove.app import create_config_app
app = create_config_app()

engine = create_async_engine(
    url=app.config.SQLALCHEMY_DATABASE_URL,
    encoding=app.config.SQLALCHEMY_DATABASE_ENCODING,
    echo=app.config.SQLALCHEMY_DATABASE_ECHO,
    future=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=True
)
