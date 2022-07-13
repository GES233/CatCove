import os, sys

app_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(app_path)

from app import create_app

def app_with_env_mode():
    mode = "dev" if not os.environ.get("SANIC_ENV") else os.environ.get("SANIC_ENV")
    return create_app(mode)
