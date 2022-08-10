from sanic import Blueprint

from .dev import api_dev

api = Blueprint.group(
    api_dev,
    # url_prefix="/api"
)
