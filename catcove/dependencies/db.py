from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Load application's path to package
import sys
from pathlib import Path

app_path = Path(Path(__file__).cwd() / "catcove")
sys.path.append(app_path)
# Load setting from app

from catcove.web.app import create_config_app

app = create_config_app()

engine = create_async_engine(
    url=app.config.SQLALCHEMY_DATABASE_URI,
    encoding=app.config.SQLALCHEMY_DATABASE_ENCODING,
    echo=app.config.SQLALCHEMY_DATABASE_ECHO,
    future=True,
)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)
