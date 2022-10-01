import aioredis

# Load application's path to package
import sys
from pathlib import Path

app_path = Path(Path(__file__).cwd() / "catcove")
sys.path.append(app_path)
# Load setting from app

from catcove.web.app import create_config_app

app = create_config_app()

redis = aioredis.from_url(
    url=app.config.REDIS_URI,
    encoding=app.config.REDIS_ENCODING,
    decode_responses=True,
)
